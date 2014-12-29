from datetime import datetime

from date_functions import DATE_FUNCTION_MAP
from dateutil.rrule import rrule, YEARLY
from date_format_mappings import DATE_MAPPINGS, TIME_MAPPINGS
import dateutil.parser


# package for general utility stuff
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


def english_parser(date_time, full_format):
    """
    This is a bit clever. We've found a python lib that can translate
    """
    # remove the first character and send attempt to translate it
    date_time_to_parse = date_time[1:-1]
    cal = parsedatetime.Calendar()
    date_time_parsed = cal.parse(date_time_to_parse)
    new_date = datetime(date_time_parsed[0][0], date_time_parsed[0][1], date_time_parsed[0][2],
                        date_time_parsed[0][3], date_time_parsed[0][4], date_time_parsed[0][5])
    return new_date, full_format


def convert_date_time(date_time, settings):
    # first of all, what format are we using.
    # We use the longer format if the date contains an ampersand
    # Remember at this point we know that the format is correct.
    date_format = DATE_MAPPINGS[settings['date-format']]['date-format']
    time_format = TIME_MAPPINGS[settings['time-format']]['time-format']
    full_format = date_format + "@" + time_format

    #Okay, Does the date command start with a ' symbol?
    if date_time[0] == "\"":
        return english_parser(date_time, full_format)

    date_time_str = str(date_time)

    if date_time_str.lower() in DATE_FUNCTION_MAP.keys():
        return DATE_FUNCTION_MAP[date_time_str.lower()](settings)

    anniversary_date = process_macros(date_time_str.lower(), settings['anniversaries'])
    if anniversary_date is not None:
        return datetime.combine(anniversary_date, datetime.max.time()), date_format

    # Now try each in turn to see if we get anything
    try:

        date_and_time = datetime.strptime(date_time_str, full_format)
        return date_and_time, full_format

    except ValueError:

        try:

            process_date = datetime.strptime(date_time_str, date_format)
            date_and_time = datetime.combine(process_date, datetime.max.time())
            return date_and_time, date_format

        except ValueError:

            try:

                # Should throw an error all on its own.
                process_time = datetime.strptime(date_time_str, time_format).time()
                date_and_time = datetime.combine(datetime.today(), process_time)
                return date_and_time, time_format

            except:

                raise ValueError

