from collections import Counter
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, \
    DATE_MAPPINGS, \
    TIME_CALCULATION, VALID_FORMAT_OPTIONS
from date_formatters import DATE_FORMATTERS_MAP
from date_parser import DateParser
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, rruleset
from utils import convert_date_time
from versioning import update_settings
from workflow import Workflow, ICON_ERROR
from humanfriendly import *


class FormatError(Exception):
    """
    Throw this when there are
    repeated characters in the
    format field.
    """
    pass


def do_functions(command, date_format, settings):
    date_time, _ = convert_date_time(command.dateTime, date_format, settings)

    if command.functionName.lower() in DATE_FORMATTERS_MAP:
        # noinspection PyCallingNonCallable
        return DATE_FORMATTERS_MAP[command.functionName.lower()](date_time)
    else:
        return "Invalid function . . . "


def delta_arithmetic(date_time, operand):
    delta_date_time = date_time

    for timespan in operand.timeSpans:
        delta_operand = relativedelta(seconds=int(timespan.amount) if timespan.span == "s" else 0,
                                      minutes=int(timespan.amount) if timespan.span == "M" else 0,
                                      hours=int(timespan.amount) if timespan.span == "h" else 0,
                                      days=int(timespan.amount) if timespan.span == "d" else 0,
                                      weeks=int(timespan.amount) if timespan.span == "w" else 0,
                                      months=int(timespan.amount) if timespan.span == "m" else 0,
                                      years=int(timespan.amount) if timespan.span == "y" else 0)

        if operand.operator == "+":
            delta_date_time += delta_operand
        else:
            delta_date_time -= delta_operand

    return delta_date_time


def do_timespans(command, date_format, settings):
    date_time, output_format = convert_date_time(command.dateTime, date_format, settings)

    for operand in command.operandList:
        date_time = delta_arithmetic(date_time, operand)

    return date_time.strftime(output_format)


def do_subtraction(command, date_format, settings):
    date_time_1, output_format_1 = convert_date_time(command.dateTime1, date_format, settings)
    date_time_2, output_format_2 = convert_date_time(command.dateTime2, date_format, settings)

    # In a moment of madness, we've decided to allow operands in a date from date
    # subtraction. It's much easier to process these first.
    if hasattr(command, "operandList1"):
        for operand in command.operandList1:
            date_time_1 = delta_arithmetic(date_time_1, operand)

    if hasattr(command, "operandList2"):
        for operand in command.operandList2:
            date_time_2 = delta_arithmetic(date_time_2, operand)

    return normalised_days(command, date_time_1, date_time_2)


def valid_command_format(command_format):
    """
    This returns true if the format option entered
    by the user is valid. The parser will take care
    of most of the validation except for repeated
    characters, which is what we're testing for here.
    :param command_format:
    :return: true if valid
    """
    repeats_search = Counter(command_format)
    repeated_items = filter(lambda x: x > 1, repeats_search.values())

    if len(repeated_items) == 0:
        return True
    else:
        return False


def calculate_time_interval(interval, start_datetime, end_datetime):
    """
    So how does this work. Well, as it turns out, trying use division by seconds to get
    the intervals is the wrong way to do it. The problem is the uneven months and leapyears
    leads to inaccuracies. So this is the new way of doing it.
    Use the rrule to get a list of all the dates that fall inside the given range. If you count
    the dates (whether the frequency is YEARLY, MONTHLY, WEEKLY etc.) then the count will tell
    you how many intervals fall inside the range. Here's the clever bit: the last date inside
    the range is kind of your remainder. Set that to the start date for the next calculation and
    you pick up at the starting poing where the last count ended!
    Note. We knock one of the count because rrule includes the date you're counting from in the list,
    which you don't really want.
    :param interval: YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY or SECONDLY
    :param start_datetime: When you're counting from
    :param end_datetime:  When you're counting to.
    :return:
    """
    rules = rruleset()
    rules.rrule(rrule(freq=interval, dtstart=start_datetime, until=end_datetime))
    datetime_list = list(rules)
    return len(datetime_list) - 1, datetime_list[-1]


def later_date_first(date_time_1, date_time_2):
    """
    The rrule is fussy about the order of the dates: the lower one
    has to go first. But we don't force our users to always put the
    higher date first, so this method will flip them if expression
    is entered incorrectly.
    :param date_time_1:
    :param date_time_2:
    :return:
    """
    if date_time_1 < date_time_2:
        start_date_time = date_time_1
        end_date_time = date_time_2
    else:
        start_date_time = date_time_2
        end_date_time = date_time_1
    return end_date_time, start_date_time


def normalised_days(command, date_time_1, date_time_2):
    # If the user selected long then he wants the full
    # date, so fill in the format before carrying on.

    if not valid_command_format(command.format):
        raise FormatError

    if not command.format:
        # default to days
        end_date_time, start_date_time = later_date_first(date_time_1, date_time_2)
        count, _ = calculate_time_interval(TIME_CALCULATION['d']['interval'], start_date_time, end_date_time)
        return "{days}".format(days=pluralize(count, TIME_CALCULATION['d']['singular'],
                                              TIME_CALCULATION['d']['plural']))

    if command.format == "long":

        difference = relativedelta(date_time_1, date_time_2)

        return "{years}, {months}, {days}, {hours}, {minutes}, {seconds}".format(
            years=pluralize(abs(difference.years), TIME_CALCULATION['y']['singular'], TIME_CALCULATION['y']['plural']),
            months=pluralize(abs(difference.months), TIME_CALCULATION['m']['singular'], TIME_CALCULATION['m']['plural']),
            days=pluralize(abs(difference.days), TIME_CALCULATION['d']['singular'], TIME_CALCULATION['d']['plural']),
            hours=pluralize(abs(difference.hours), TIME_CALCULATION['h']['singular'], TIME_CALCULATION['h']['plural']),
            minutes=pluralize(abs(difference.minutes), TIME_CALCULATION['M']['singular'], TIME_CALCULATION['M']['plural']),
            seconds=pluralize(abs(difference.seconds), TIME_CALCULATION['s']['singular'], TIME_CALCULATION['s']['plural']))

    # Python gotcha. They keys in the map are not guaranteed
    # to come out in the same order you put then; so we have
    # to scan them specifically in the order we want them to
    # appear in the calculation. If they're out of sequence
    # then the calculation will return the wrong result.

    # This time it does matter which way around the dates go.

    end_date_time, start_date_time = later_date_first(date_time_1, date_time_2)

    normalised_elements = []

    for x in VALID_FORMAT_OPTIONS:

        if x in command.format:
            count, start_date_time = calculate_time_interval(TIME_CALCULATION[x]['interval'],
                                                             start_date_time, end_date_time)
            normalised_elements.append(pluralize(count,
                                                 TIME_CALCULATION[x]['singular'], TIME_CALCULATION[x]['plural']))
    # We put each part of the calculation in a list
    # so that Python can handle comma-separating them later on
    return ', '.join(normalised_elements)


def main(wf):
    # Get the date format from the configuration

    update_settings(wf)

    key = wf.settings['date-format']
    args = wf.args

    date_mapping = DATE_MAPPINGS[key]

    command_parser = DateParser(date_mapping['regex'], wf.settings)

    try:

        command = command_parser.parse_command(args[0])

        if hasattr(command, "dateTime"):
            output = do_timespans(command, date_mapping['date-format'], wf.settings)

            if hasattr(command, "functionName"):
                setattr(command, "dateTime", output)
                # and run it through the functions function
                output = do_functions(command, date_mapping['date-format'], wf.settings)

        elif hasattr(command, "dateTime1") and hasattr(command, "dateTime2"):
            output = do_subtraction(command, date_mapping['date-format'], wf.settings)

        else:
            output = "Invalid Expression"

    except SyntaxError:
        output = "Invalid Command"

    except ValueError:
        output = "Invalid Date"

    except FormatError:
        output = "Invalid format"

    if output.startswith("Invalid"):
        wf.add_item(title=". . .", subtitle=output, valid=False, arg=args[0], icon=ICON_ERROR)
    else:
        wf.add_item(title=output, subtitle="Copy to clipboard", valid=True, arg=output)

    wf.send_feedback()

# ## Python calling routine. Will only run this app if it is the main program
# ## Otherwise it won't run because it is an included module -- clever!

if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))
