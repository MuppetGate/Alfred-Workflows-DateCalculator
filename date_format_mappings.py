# The date formats array
from dateutil.relativedelta import relativedelta, TH, MO, TU, WE, FR, SA, SU

DATE_MAPPINGS = {

    'dd-mm-yy': {'name': 'short UK date (-)', 'date-format': '%d-%m-%y', 'regex': '\d{2}-\d{2}-\d{2}'},
    'dd-mm-yyyy': {'name': 'long UK date (-)', 'date-format': '%d-%m-%Y', 'regex': '\d{2}-\d{2}-\d{4}'},
    'dd/mm/yy': {'name': 'short UK date (/)', 'date-format': '%d/%m/%y', 'regex': '\d{2}/\d{2}/\d{2}'},
    'dd/mm/yyyy': {'name': 'long UK date (/)', 'date-format': '%d/%m/%Y', 'regex': '\d{2}/\d{2}/\d{4}'},
    'dd.mm.yy': {'name': 'short UK date (.)', 'date-format': '%d.%m.%y', 'regex': '\d{2}\.\d{2}\.\d{2}'},
    'dd.mm.yyyy': {'name': 'long UK date (.)', 'date-format': '%d.%m.%Y', 'regex': '\d{2}\.\d{2}\.\d{4}'},
    'mm-dd-yy': {'name': 'short US date (-)', 'date-format': '%m-%d-%y', 'regex': '\d{2}-\d{2}-\d{2}'},
    'mm-dd-yyyy': {'name': 'long US date (-)', 'date-format': '%m-%d-%Y', 'regex': '\d{2}-\d{2}-\d{4}'},
    'mm/dd/yy': {'name': 'short US date (/)', 'date-format': '%m/%d/%y', 'regex': '\d{2}/\d{2}/\d{2}'},
    'mm/dd/yyyy': {'name': 'long US date (/)', 'date-format': '%m/%d/%Y', 'regex': '\d{2}/\d{2}/\d{4}'},
    'mm.dd.yy': {'name': 'short US date (.)', 'date-format': '%m.%d.%y', 'regex': '\d{2}\.\d{2}\.\d{2}'},
    'mm.dd.yyyy': {'name': 'long US date (.)', 'date-format': '%m.%d.%Y', 'regex': '\d{2}\.\d{2}\.\d{4}'}
}

DEFAULT_DATE_FORMAT = 'dd.mm.yy'

DEFAULT_TIME_RE = '\d{2}:\d{2}'

DEFAULT_TIME_EXPR = '%H:%M'

VALID_FORMAT_OPTIONS = ["y", "m", "w", "d", "h", "M", "s"]
VALID_WORD_FORMAT_OPTIONS = ["long"]

# The DAY_MAP is specific to relative delta
DAY_MAP = {"mon": relativedelta(days=+1, weekday=MO(+1)),
           "tue": relativedelta(days=+1, weekday=TU(+1)),
           "wed": relativedelta(days=+1, weekday=WE(+1)),
           "thu": relativedelta(days=+1, weekday=TH(+1)),
           "fri": relativedelta(days=+1, weekday=FR(+1)),
           "sat": relativedelta(days=+1, weekday=SA(+1)),
           "sun": relativedelta(days=+1, weekday=SU(+1))}


TIME_MAP = {"seconds_in_a_day": 86400,
            "seconds_in_a_week": 604800,
            "seconds_in_a_month": 2592000,
            "seconds_in_a_year": 31556952,
            "seconds_in_an_hour": 3600,
            "seconds_in_a_minute": 60}


DEFAULT_ANNIVERSARIES = {'christmas': '2014-12-25T00:30:00',
                         'alfred': '2011-12-08T00:00:00'}

DEFAULT_WORKFLOW_SETTINGS = {

    'date-format': DEFAULT_DATE_FORMAT,

    'anniversaries': DEFAULT_ANNIVERSARIES

}

## This is the cache used to operate the anniversaries workflows
ANN_CACHE = "anniversary_cache"