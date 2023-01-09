from __future__ import unicode_literals, print_function
import sys

from date_format_mappings import DATE_MAPPINGS, DEFAULT_WORKFLOW_SETTINGS
from utils import convert_date_time
from versioning import update_settings
from workflow import Workflow
from macros_parser import MacrosParser

FOUR_DIGIT_DATE_ERROR = "Please ensure that you have set your date format to one that supports 4-digit years"


def add_anniversary(anniversaries, command, date_mapping, wf):

    if "%Y" not in date_mapping["date-format"]:
        return FOUR_DIGIT_DATE_ERROR

    if command.anniversaryName in anniversaries:
        output = "{anniversaryName} already exists".format(anniversaryName=command.anniversaryName)
    else:
        date_time, output_format = convert_date_time(command.dateTime, wf.settings)
        anniversary_date = date_time.isoformat()
        anniversaries[command.anniversaryName.lower()] = anniversary_date
        wf.settings["anniversaries"] = anniversaries
        output = "{anniversaryName} added".format(anniversaryName=command.anniversaryName)
    return output


def change_anniversary(anniversaries, command, date_mapping, wf):

    if "%Y" not in date_mapping["date-format"]:
        return FOUR_DIGIT_DATE_ERROR

    if command.anniversaryName not in anniversaries:
        output = "{anniversaryName} does not exist".format(anniversaryName=command.anniversaryName)
    else:
        date_time, output_format = convert_date_time(command.dateTime, wf.settings)
        anniversary_date = date_time.isoformat()
        anniversaries[command.anniversaryName.lower()] = anniversary_date
        wf.settings["anniversaries"] = anniversaries
        output = "{anniversaryName} changed".format(anniversaryName=command.anniversaryName)
    return output


def delete_anniversary(anniversaries, command, wf):
    del anniversaries[command.anniversaryName]
    wf.settings["anniversaries"] = anniversaries
    output = "{anniversaryName} deleted".format(anniversaryName=command.anniversaryName)
    return output


def main(wf):
    # Get the date format from the configuration

    update_settings(wf)

    key = wf.settings['date-format']
    args = wf.args

    date_mapping = DATE_MAPPINGS[key]

    # There is no point going any further
    # unless they are set up for a four-digit date.

    anniversaries = wf.settings["anniversaries"]

    command_parser = MacrosParser(wf.settings)

    try:

        command = command_parser.parse_command(args[0])

        if hasattr(command, "anniversaryName") and hasattr(command, "add") and hasattr(command, "dateTime"):

            output = add_anniversary(anniversaries, command, date_mapping, wf)

        elif hasattr(command, "anniversaryName") and hasattr(command, "edit") and hasattr(command, "dateTime"):

            output = change_anniversary(anniversaries, command, date_mapping, wf)

        elif hasattr(command, "anniversaryName") and hasattr(command, "delete") and not hasattr(command, "dateTime"):

            output = delete_anniversary(anniversaries, command, wf)

        else:
            output = "Invalid expression"

    except SyntaxError:
        output = "Invalid Command"

    except ValueError:
        output = "Invalid Date"

    print(output)

# ## Python calling routine. Will only run this app if it is the main program
# ## Otherwise it won't run because it is an included module -- clever!

if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))

