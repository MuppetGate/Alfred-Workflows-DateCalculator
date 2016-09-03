# The date formats array
import re


def no_process(date_time_str):
    return date_time_str


def fill_minutes(date_time_str):
    return re.sub(r"(?<![:\d])(\d{1,2})(AM|PM)", r"\1:00\2", date_time_str, 0, re.IGNORECASE)

WN_FUNCTION_REGEX = re.compile(r'wn(\s+(?P<year>\d{4}))?'
                               r'(\s+(?P<week_number>\d{1,2}))?'
                               r'(\s+(?P<day>mon|tue|wed|thu|fri|sat|sun))?', re.IGNORECASE)

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
    'yyyy-mm-dd': {'name': 'international (-)', 'date-format': '%Y-%m-%d', 'regex': '\d{4}-\d{2}-\d{2}'},
    'dd mmm yyyy': {'name': 'wordy date format', 'date-format': '%d %b %Y', 'regex': '\d{2} [a-zA-Z]{3} \d{4}'}
}

TIME_MAPPINGS = {

    '24-hour': {'name': '24-hour format', 'time-format': '%H:%M', 'regex': '\d{1,2}\:\d{2}', 'pre-process': no_process},
    '12-hour': {'name': '12-hour format', 'time-format': '%I:%M%p', 'regex': '\d{1,2}(\:\d{2})?(AM|PM)',
                'pre-process': fill_minutes}
}

# Note that the regex and formatting for the full date/time format is
# calculated at runtime using the settings for date format and time format
DATE_TIME_MAPPINGS = {

    '@': {'date-time-format': lambda date, time: '{date}@{time}'.format(date=date, time=time)},
    'at': {'date-time-format': lambda date, time: '{date} at {time}'.format(date=date, time=time)},
    'on': {'date-time-format': lambda date, time: time + ' on ' + date},
    'arrow': {'date-time-format': lambda date, time: 'DATE ==> {date} TIME ==> {time}'.format(date=date, time=time)}
}

DEFAULT_DATE_FORMAT = 'dd.mm.yy'
DEFAULT_TIME_FORMAT = '24-hour'
DEFAULT_DATE_TIME_FORMAT = '@'

VALID_FORMAT_OPTIONS = ["y", "m", "w", "d", "h", "M", "s"]
VALID_WORD_FORMAT_OPTIONS = ["long"]

TIME_CALCULATION = {

    'y': {'interval': 'year', 'singular': 'year', 'plural': 'years', 'seconds': 1 * 60 * 60 * 24 * 7 * 4 * 12},
    'm': {'interval': 'month', 'singular': 'month', 'plural': 'months', 'seconds': 1 * 60 * 60 * 24 * 7 * 4},
    'w': {'interval': 'week', 'singular': 'week', 'plural': 'weeks', 'seconds': 1 * 60 * 60 * 24 * 7},
    'd': {'interval': 'day', 'singular': 'day', 'plural': 'days', 'seconds': 1 * 60 * 60 * 24},
    'h': {'interval': 'hour', 'singular': 'hour', 'plural': 'hours', 'seconds': 1 * 60 * 60},
    'M': {'interval': 'minute', 'singular': 'minute', 'plural': 'minutes', 'seconds': 1 * 60},
    's': {'interval': 'second', 'singular': 'second', 'plural': 'seconds', 'seconds': 1}

}

DEFAULT_ANNIVERSARIES = {'christmas': '1900-12-25T00:30:00',
                         'alfred': '2010-02-28T00:00:00',
                         'leap': '2012-02-29T00:00:00',
                         'future': '2072-01-01T00:00:00'}

DEFAULT_WORKFLOW_SETTINGS = {

    'date-format': DEFAULT_DATE_FORMAT,
    'anniversaries': DEFAULT_ANNIVERSARIES,
    'time-format': DEFAULT_TIME_FORMAT,
    'date-time-format': DEFAULT_DATE_TIME_FORMAT

}
