# The date formats array

DATE_MAPPINGS = {

    'dd-mm-yy': {'name': 'short UK date (-)', 'date-format': '%d-%m-%y', 'regex': r'\d{2}-\d{2}-\d{2}'},
    'dd-mm-yyyy': {'name': 'long UK date (-)', 'date-format': '%d-%m-%Y', 'regex': r'\d{2}-\d{2}-\d{4}'},
    'dd/mm/yy': {'name': 'short UK date (/)', 'date-format': '%d/%m/%y', 'regex': r'\d{2}/\d{2}/\d{2}'},
    'dd/mm/yy': {'name': 'short UK date (/)', 'date-format': '%d/%m/%y', 'regex': r'\d{2}/\d{2}/\d{2}'},
    'dd/mm/yyyy': {'name': 'long UK date (/)', 'date-format': '%d/%m/%Y', 'regex': r'\d{2}/\d{2}/\d{4}'},
    'dd.mm.yy': {'name': 'short UK date (.)', 'date-format': '%d.%m.%y', 'regex': r'\d{2}\.\d{2}\.\d{2}'},
    'dd.mm.yyyy': {'name': 'long UK date (.)', 'date-format': '%d.%m.%Y', 'regex': r'\d{2}\.\d{2}\.\d{4}'},
    'mm-dd-yy': {'name': 'short US date (-)', 'date-format': '%m-%d-%y', 'regex': r'\d{2}-\d{2}-\d{2}'},
    'mm-dd-yyyy': {'name': 'long US date (-)', 'date-format': '%m-%d-%Y', 'regex': r'\d{2}-\d{2}-\d{4}'},
    'mm/dd/yy': {'name': 'short US date (/)', 'date-format': '%m/%d/%y', 'regex': r'\d{2}/\d{2}/\d{2}'},
    'mm/dd/yyyy': {'name': 'long US date (/)', 'date-format': '%m/%d/%Y', 'regex': r'\d{2}/\d{2}/\d{4}'},
    'mm.dd.yy': {'name': 'short US date (.)', 'date-format': '%m.%d.%y', 'regex': r'\d{2}\.\d{2}\.\d{2}'},
    'mm.dd.yyyy': {'name': 'long US date (.)', 'date-format': '%m.%d.%Y', 'regex': r'\d{2}\.\d{2}\.\d{4}'}
}

DEFAULT_DATE_FORMAT = 'dd-mm-yy'

DEFAULT_TIME_RE = r'\d{2}:\d{2}'

DEFAULT_TIME_EXPR = '%H:%M'

DEFAULT_WORKFLOW_SETTINGS = {

    'date-format': DEFAULT_DATE_FORMAT

}