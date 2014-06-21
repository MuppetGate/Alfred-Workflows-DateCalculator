
import sys

from datetime import date, datetime
from workflow import Workflow
from date_format_mappings import DEFAULT_DATE_FORMAT, DEFAULT_WORKFLOW_SETTINGS

def main (wf):
    
    args = wf.args
    
    wf.settings['date-format'] = args[0]

    print "Date format set to {dformat}".format(dformat = args[0])

if __name__ == '__main__':
    wf = Workflow(default_settings = DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(wf.run(main))