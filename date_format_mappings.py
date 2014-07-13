# The date formats array
from collections import OrderedDict

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

DEFAULT_DATE_FORMAT = 'dd.mm.yy'

DEFAULT_TIME_RE = '\d{2}:\d{2}'

DEFAULT_TIME_EXPR = '%H:%M'

VALID_FORMAT_OPTIONS = ["y", "m", "w", "d", "h", "M", "s"]
VALID_WORD_FORMAT_OPTIONS = ["long"]


TIME_CALCULATION = {

    'y': {'seconds': 31540000, 'singular': 'year', 'plural': 'years'},
    'm': {'seconds': 2628000, 'singular': 'month', 'plural': 'months'},
    'w': {'seconds': 604800, 'singular': 'week', 'plural': 'weeks'},
    'd': {'seconds': 86400, 'singular': 'day', 'plural': 'days'},
    'h': {'seconds': 3600, 'singular': 'hour', 'plural': 'hours'},
    'M': {'seconds': 60, 'singular': 'minute', 'plural': 'minutes'},
    's': {'seconds': 1, 'singular': 'second', 'plural': 'seconds'}

}


DEFAULT_ANNIVERSARIES = {'christmas': '1900-12-25T00:30:00',
                         'alfred': '2010-02-28T00:00:00',
                         'leap': '2012-02-29T00:00:00',
                         'future': '2072-01-01T00:00:00'}

DEFAULT_WORKFLOW_SETTINGS = {

    'date-format': DEFAULT_DATE_FORMAT,

    'anniversaries': DEFAULT_ANNIVERSARIES

}

