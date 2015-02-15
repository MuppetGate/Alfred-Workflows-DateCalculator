from datetime import datetime, date
import re
from date_format_mappings import WN_FUNCTION_REGEX

from date_functions import DATE_FUNCTION_MAP, get_date_format, get_time_format, get_full_format, get_time_preprocessor, \
    DAYS_OF_WEEK_ABBREVIATIONS
from dateutil.rrule import rrule, YEARLY
import dateutil.parser


# package for general utility stuff
from isoweek import Week
from parsedatetime import parsedatetime


def get_anniversary(date_object):

    anniversary_rule = rrule(bymonthday=date_object.day, bymonth=date_object.month, freq=YEARLY, dtstart=date_object)
    current_date = datetime.today()
    anniversary_date = anniversary_rule.after(current_date, inc=False)
    return datetime.combine(anniversary_date, datetime.min.time())


def process_macros(date_time_str, anniversaries):
    """
    This method will look through the settings
    and return a date for an anniversary, if
    it finds one.
    :return:
    """

    absolute = False

    if date_time_str.startswith("^"):
        date_time_str = date_time_str.lstrip("^")
        absolute = True

    for anniversary in anniversaries.keys():

        if date_time_str.lower() == anniversary:
            anniversary_date_str = anniversaries[anniversary]
            # We're storing in ISO format. How do you get that back?
            anniversary_date = dateutil.parser.parse(anniversary_date_str)

            if absolute:
                return anniversary_date
            else:
                return get_anniversary(anniversary_date)

    return None


def natural_parser(date_time, settings):
    """
    This is a bit clever. We've found a python lib that can translate
    """
    # This is a list of the error codes and matching formats that will be used
    # depending on what is returned by the parser
    format_map = {
        1: get_date_format(settings),
        2: get_time_format(settings),
        3: get_full_format(settings)
    }

    # remove the first character and send attempt to translate it
    date_time_to_parse = date_time[1:-1]
    cal = parsedatetime.Calendar()
    date_time_parsed = cal.parseDT(date_time_to_parse)

    # This parser handily sends back an error code, just in case
    error_code = date_time_parsed[1]

    if error_code == 0:
        raise ValueError
    else:
        return date_time_parsed[0], format_map[error_code]


def get_date_from_week_number(date_time):

    week_day_map = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}

    current_date = date.today()

    match = re.match(WN_FUNCTION_REGEX, date_time)

    if match.group('year') is not None:
        year = int(match.group('year'))
    else:
        year = current_date.year

    if match.group('week_number') is not None:
        week_number = int(match.group('week_number'))
    else:
        week_number = int(current_date.strftime("%U"))

    if match.group('day') is not None:
        day = match.group('day')
    else:
        day = week_day_map[current_date.weekday()]

    w = Week(year, week_number)

    func = getattr(w, DAYS_OF_WEEK_ABBREVIATIONS[day], "sunday")
    return func()


def convert_date_time(date_time, settings):
    # first of all, what format are we using.
    # We use the longer format if the date contains an ampersand
    # Remember at this point we know that the format is correct.
    date_format = get_date_format(settings)
    time_format = get_time_format(settings)
    full_format = get_full_format(settings)

    #Okay, Does the date command start with a " symbol?
    if date_time[0] == "\"":
        return natural_parser(date_time, settings)

    #How about a date from a week number and a year
    if date_time.startswith("wn"):
        return get_date_from_week_number(date_time), date_format

    date_time_str = str(date_time)

    if date_time_str.lower() in DATE_FUNCTION_MAP.keys():
        return DATE_FUNCTION_MAP[date_time_str.lower()](settings)

    anniversary_date = process_macros(date_time_str.lower(), settings['anniversaries'])
    if anniversary_date is not None:
        return datetime.combine(anniversary_date, datetime.max.time()), date_format

    # Now try each in turn to see if we get anything. Note that we have to convert
    # each one to uppercase before we attempt the conversion. Why? Because if the
    # user is using the 12-hour format then the AM/PM indicators must be in upper case
    # to get translated correctly. We don't want to force the user to enter the indicators
    # in upper case, so we'll do the conversion for them.
    try:

        time_preprocessor = get_time_preprocessor(settings)

        if time_preprocessor:
            date_time_str = time_preprocessor(date_time_str)

        date_and_time = datetime.strptime(date_time_str.upper(), full_format)
        return date_and_time, full_format

    except ValueError:

        try:

            process_date = datetime.strptime(date_time_str.upper(), date_format)
            date_and_time = datetime.combine(process_date, datetime.max.time())
            return date_and_time, date_format

        except ValueError:

            try:
                # Should throw an error all on its own.
                process_time = datetime.strptime(date_time_str.upper(), time_format).time()
                date_and_time = datetime.combine(datetime.today(), process_time)
                return date_and_time, time_format

            except:
                raise ValueError
