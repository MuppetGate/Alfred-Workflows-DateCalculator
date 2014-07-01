# -- coding: utf-8 --

from __future__ import unicode_literals, print_function
import sys

from date_format_mappings import DATE_MAPPINGS, DEFAULT_WORKFLOW_SETTINGS
from versioning import update_settings
from workflow import Workflow, MATCH_STARTSWITH
from dateutil import parser


def filter_names(name):
    """
    This is just the filter function
    for the framework search
    :param name:
    :return:
    """
    return name.lower()


def main(wf):
    # Get the date format from the configuration

    update_settings(wf)
    args = wf.args

    key = wf.settings['date-format']

    date_mapping = DATE_MAPPINGS[key]
    anniversaries = wf.settings["anniversaries"]

    if args[0]:
        filtered_keys = wf.filter(query=args[0], items=anniversaries.keys(),
                                  key=filter_names, match_on=MATCH_STARTSWITH)
    else:
        filtered_keys = anniversaries.keys()

    for anniversary in sorted(filtered_keys):
        anniversary_date_str = anniversaries[anniversary]
        date_object = parser.parse(anniversary_date_str)
        entry = "{anniversary} ➤ {date}".format(anniversary=anniversary,
                                                  date=date_object.strftime(date_mapping['date-format']))

        wf.add_item(title=entry, subtitle="Press alt to change, ctrl to delete", arg=anniversary, valid=True)

    wf.send_feedback()

# ## Python calling routine. Will only run this app if it is the main program
# ## Otherwise it won't run because it is an included module -- clever!

if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))


