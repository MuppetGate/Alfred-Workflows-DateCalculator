from __future__ import unicode_literals, print_function

import sys

from workflow import Workflow
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS


def main(wf):

    print("Date format is {format}".format(format=wf.settings['date-format']))

if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))