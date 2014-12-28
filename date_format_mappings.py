# The date formats array
from collections import OrderedDict
from dateutil.rrule import YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY

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
    'mm.dd.yyyy': {'name': 'long US date (.)', 'date-format': '%m.%d.%Y', 'regex': '\d{2}\.\d{2}\.\d{4}'},
    'yyyy-mm-dd': {'name': 'international (-)', 'date-format': '%Y-%m-%d', 'regex': '\d{4}-\d{2}-\d{2}'}
}

TIME_MAPPINGS = {

    '24-hour': {'name': '24-hour format', 'time-format': '%H:%M', 'regex': '\d{2}\:\d{2}'},
    '12-hour': {'name': '12-hour format', 'time-format': '%I:%M%p', 'regex': '\d{2}\:\d{2}(AM|PM)'}
}

DEFAULT_DATE_FORMAT = 'dd.mm.yy'
DEFAULT_TIME_FORMAT = '24-hour'

DEFAULT_TIME_RE = '\d{2}:\d{2}'

DEFAULT_TIME_EXPR = '%H:%M'

VALID_FORMAT_OPTIONS = ["y", "m", "w", "d", "h", "M", "s"]
VALID_WORD_FORMAT_OPTIONS = ["long"]


TIME_CALCULATION = {

    'y': {'interval': YEARLY, 'singular': 'year', 'plural': 'years', 'seconds': 1 * 60 * 60 * 24 * 7 * 4 * 12},
    'm': {'interval': MONTHLY, 'singular': 'month', 'plural': 'months', 'seconds': 1 * 60 * 60 * 24 * 7 * 4},
    'w': {'interval': WEEKLY, 'singular': 'week', 'plural': 'weeks', 'seconds': 1 * 60 * 60 * 24 * 7},
    'd': {'interval': DAILY, 'singular': 'day', 'plural': 'days', 'seconds': 1 * 60 * 60 * 24},
    'h': {'interval': HOURLY, 'singular': 'hour', 'plural': 'hours', 'seconds': 1 * 60 * 60},
    'M': {'interval': MINUTELY, 'singular': 'minute', 'plural': 'minutes', 'seconds': 1 * 60},
    's': {'interval': SECONDLY, 'singular': 'second', 'plural': 'seconds', 'seconds': 1}

}


DEFAULT_ANNIVERSARIES = {'christmas': '1900-12-25T00:30:00',
                         'alfred': '2010-02-28T00:00:00',
                         'leap': '2012-02-29T00:00:00',
                         'future': '2072-01-01T00:00:00'}

DEFAULT_WORKFLOW_SETTINGS = {

    'date-format': DEFAULT_DATE_FORMAT,
    'anniversaries': DEFAULT_ANNIVERSARIES,
    'time_format': DEFAULT_TIME_FORMAT

}

