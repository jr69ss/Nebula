from termcolor import colored
import sys
import json
from datetime import datetime
from pydoc import pipepager

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "iam",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "INSTANCEPROFILE": {
        "value": "",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    }
}

description = "Get info on the policy provided"

aws_command = "aws iam get-instance-profile --instance-profile-name <instance profile name> --region <region> --profile <profile>"

colors = [
    "not-used",
    "red",
    "blue",
    "yellow",
    "green",
    "magenta",
    "cyan",
    "white"
]

output = ""


def list_dictionary(d, n_tab):
    global output
    if isinstance(d, list):
        n_tab += 1
        for i in d:
            if not isinstance(i, list) and not isinstance(i, dict):
                output += ("{}{}\n".format("\t" * n_tab, colored(i, colors[n_tab])))
            else:
                list_dictionary(i, n_tab)
    elif isinstance(d, dict):
        n_tab += 1
        for key, value in d.items():
            if not isinstance(value, dict) and not isinstance(value, list):
                output += ("{}{}: {}\n".format("\t" * n_tab, colored(key, colors[n_tab], attrs=['bold']),
                                               colored(value, colors[n_tab + 1])))
            else:
                output += ("{}{}:\n".format("\t" * n_tab, colored(key, colors[n_tab], attrs=['bold'])))
                list_dictionary(value, n_tab)


def exploit(profile, workspace):
    global output
    n_tab = 0
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_get_instance_profile".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    instanceprofilename = variables['INSTANCEPROFILE']['value']

    try:
        response = profile.get_instance_profile(
            InstanceProfileName=instanceprofilename
        )

        json_data = response['InstanceProfile']
        title_name = instanceprofilename

        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile, indent=4, default=str)
            print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

        """
        if isinstance(json_data, list):
            output += colored("------------------------------------------------------------------\n", "yellow", attrs=['bold'])
            for data in json_data:
                output += colored("{}: {}\n".format("InstanceProfileName", title_name), "yellow", attrs=['bold'])
                list_dictionary(data, n_tab)
                output += colored("------------------------------------------------------------------\n", "yellow", attrs=['bold'])
        else:
        """

        output += colored("------------------------------------------------------------------\n", "yellow",
                          attrs=['bold'])
        output += colored("{}: {}\n".format("InstanceProfileName", title_name), "yellow", attrs=['bold'])
        list_dictionary(json_data, n_tab)
        output += colored("------------------------------------------------------------------\n", "yellow",
                          attrs=['bold'])

        print(output)
        output = ""

    except:
        print(colored("[*] Does your IAM have the right permissions to use 'GetUserPolicy' API call? ", "red"))
        e = sys.exc_info()[0]
        print(colored("[*] {}".format(e), "red"))
