import sys
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS
from workflow import Workflow

__author__ = 'raymond'


def main(wf):

    wf.send_feedback()

# ## Python calling routine. Will only run this app if it is the main program
# ## Otherwise it won't run because it is an included module -- clever!

if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))

