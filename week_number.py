# week_number.py
# MuppetGate

import sys

from datetime import date, datetime
from workflow import Workflow
from date_format_mappings import DATE_MAPPINGS, DEFAULT_DATE_FORMAT, DEFAULT_WORKFLOW_SETTINGS

def main (wf):
    
    args = wf.args

    key = wf.settings['date-format']
    
    if args[0] == "":

        print "You are in week {weekNumber}".format(weekNumber = date.today().strftime("%V"))

    else:

        try:
            query_date = datetime.strptime(args[0], DATE_MAPPINGS[key]['date-format'])
            print "The date {date} was in week {weekNumber}".format(date = query_date.strftime(DATE_MAPPINGS[key]['date-format']), 
                weekNumber = query_date.strftime("%V"))
        
        except:
            print "Invalid date!"

if __name__ == '__main__':
    wf = Workflow(default_settings = DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(wf.run(main))