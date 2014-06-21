
import sys

from datetime import date, datetime
from workflow import Workflow
from date_format_mappings import DATE_MAPPINGS, DEFAULT_DATE_FORMAT, DEFAULT_WORKFLOW_SETTINGS

def main (wf):
    
    # Get the current setting
    current_setting = wf.settings['date-format']

    # These are the date formats the workflow supports
    for key in sorted(DATE_MAPPINGS.keys()):
        # Indicate the current setting for the user
        if key == current_setting:
            title_setting = key + ' *'
        else:
            title_setting = key

        # You know what? There's not point letting them set the format to the current format. It's 
        # a waste of effort.
        wf.add_item(title = title_setting, subtitle = DATE_MAPPINGS[key]['name'], valid = (key != current_setting), arg = key)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(default_settings = DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(wf.run(main))