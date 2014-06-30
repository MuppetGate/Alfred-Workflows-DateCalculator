from datetime import datetime, timedelta, date
from date_format_mappings import DEFAULT_TIME_EXPR, DAY_MAP
from dateutil.easter import easter
import dateutil.parser

__author__ = 'raymond'

# package for general utility stuff


def get_easter():
    current_date = datetime.today()
    this_easter = datetime.combine(easter(current_date.year), datetime.min.time())
    if current_date < this_easter:
        return this_easter
    else:
        # We've already had easter this year
        next_year = datetime(current_date.year + 1, 1, 1)
        return datetime.combine(easter(next_year.year), datetime.min.time())


def get_anniversary(date_object):
    current_date = datetime.today()
    this_anniversary = datetime(current_date.year, date_object.month, date_object.day)
    if current_date < this_anniversary:
        return this_anniversary
    else:
        # We've already had Crimbo this year
        return datetime(current_date.year + 1, date_object.month, date_object.day)


def process_macros(date_time_str, anniversaries):
    """
    This method will look through the settings
    and return a date for an anniversary, if
    it finds one.
    :return:
    """
    for anniversary in anniversaries.keys():

        if date_time_str.lower() == anniversary:
            anniversary_date_str = anniversaries[anniversary]
            # We're storing in ISO format. How'd you get that back?
            anniversary_date = dateutil.parser.parse(anniversary_date_str)
            return get_anniversary(anniversary_date)

    return None


def convert_date_time(date_time_str, date_format, settings):
    # first of all, what format are we using.
    # We use the longer format if the date contains an ampersand
    # Remember at this point we know that the format is correct.

    current_date = datetime.combine(date.today(), datetime.max.time())
    current_time = datetime.combine(date.today(), datetime.today().time())

    full_format = date_format + "@" + DEFAULT_TIME_EXPR

    if date_time_str.lower() == "date" or date_time_str.lower() == "today":
        return current_date, date_format

    if date_time_str.lower() == "time":
        return current_time, DEFAULT_TIME_EXPR

    if date_time_str.lower() == "now":
        return datetime.now(), full_format

    if date_time_str.lower() == "yesterday":
        return current_date - timedelta(days=1), date_format

    if date_time_str.lower() == "tomorrow":
        return current_date + timedelta(days=1), date_format

    if date_time_str.lower() in DAY_MAP.keys():
        return current_date + DAY_MAP[date_time_str.lower()], date_format

    if date_time_str.lower() == "easter":
        return get_easter(), date_format

    anniversary_date = process_macros(date_time_str.lower(), settings['anniversaries'])
    if anniversary_date is not None:
        return anniversary_date, date_format

    # Now try each in turn to see if we get anything
    try:

        date_and_time = datetime.strptime(date_time_str, full_format)
        return date_and_time, full_format

    except ValueError:

        try:

            process_date = datetime.strptime(date_time_str, date_format)
            date_and_time = datetime.combine(process_date, datetime.now().time())
            return date_and_time, date_format

        except ValueError:

            # Should throw an error all on its own.
            process_time = datetime.strptime(date_time_str, DEFAULT_TIME_EXPR).time()
            date_and_time = datetime.combine(datetime.today(), process_time)
            return date_and_time, DEFAULT_TIME_EXPR
