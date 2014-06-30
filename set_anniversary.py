from __future__ import unicode_literals, print_function
import sys

from date_format_mappings import DATE_MAPPINGS, DEFAULT_WORKFLOW_SETTINGS, ANN_CACHE
from utils import convert_date_time
from versioning import update_settings
from workflow import Workflow
from macros_parser import MacrosParser


__author__ = 'raymond'


def go_to_step(parameters):

    def send_params():
            return parameters

    return send_params


def main(wf):
    # Get the date format from the configuration

    update_settings(wf)

    key = wf.settings['date-format']
    args = wf.args

    date_mapping = DATE_MAPPINGS[key]
    anniversaries = wf.settings["anniversaries"]

    command_parser = MacrosParser(date_mapping['regex'], wf.settings)

    command = command_parser.parse_command(args[0])

    if hasattr(command, "anniversaryName") and hasattr(command, "add") and hasattr(command, "dateTime"):

        date_time, output_format = convert_date_time(command.dateTime, date_mapping['date-format'], wf.settings)
        anniversary_date = date_time.isoformat()
        anniversaries[command.anniversaryName.lower()] = anniversary_date
        wf.settings["anniversaries"] = anniversaries
        output = "{anniversaryName} added".format(anniversaryName=command.anniversaryName)

    elif hasattr(command, "anniversaryName") and hasattr(command, "edit") and hasattr(command, "dateTime"):

        date_time, output_format = convert_date_time(command.dateTime, date_mapping['date-format'], wf.settings)
        anniversary_date = date_time.isoformat()
        anniversaries[command.anniversaryName.lower()] = anniversary_date
        wf.settings["anniversaries"] = anniversaries
        output = "{anniversaryName} changed".format(anniversaryName=command.anniversaryName)

    elif hasattr(command, "anniversaryName") and hasattr(command, "delete") and not hasattr(command, "dateTime"):

        del anniversaries[command.anniversaryName]
        wf.settings["anniversaries"] = anniversaries
        output = "{anniversaryName} deleted".format(anniversaryName=command.anniversaryName)

    else:

        output = "Invalid expression"

    print(output)

# ## Python calling routine. Will only run this app if it is the main program
# ## Otherwise it won't run because it is an included module -- clever!

if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))

