import sys

from datetime import date, datetime
from workflow import Workflow
from date_format_mappings import DEFAULT_DATE_FORMAT, DEFAULT_WORKFLOW_SETTINGS

def main (wf):


    print "Date format is {dformat}".format(dformat = wf.settings['date-format'])

if __name__ == '__main__':
    wf = Workflow(default_settings = DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(wf.run(main))