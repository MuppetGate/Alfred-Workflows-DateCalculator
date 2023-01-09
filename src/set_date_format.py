from __future__ import unicode_literals, print_function

import sys
from workflow import Workflow
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS


def main(wf):
    args = wf.args

    wf.settings['date-format'] = args[0]

    print("Date format set to {format}".format(format=args[0]))


if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))