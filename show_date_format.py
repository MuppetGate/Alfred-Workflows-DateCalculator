# This file is for displaying the user's
# currently selected time format
from __future__ import unicode_literals, print_function

import sys
from versioning import update_settings

from workflow import Workflow
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS


def main(wf):

    update_settings(wf)

    print("Time format is {format}".format(format=wf.settings['time-format']))

if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))