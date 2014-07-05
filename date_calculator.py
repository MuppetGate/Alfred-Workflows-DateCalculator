from collections import Counter
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, \
    DATE_MAPPINGS, \
    TIME_MAP
from date_formatters import DATE_FORMATTERS_MAP
from date_parser import DateParser
from dateutil.relativedelta import relativedelta
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

    date_time, output_format = convert_date_time(command.dateTime, date_format, settings)

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


def normalised_days(command, date_time_1, date_time_2):
    # If the user selected long then he wants the full
    # date, so fill in the format before carrying on.

    if not valid_command_format(command.format):
        raise FormatError

    if command.format == "long":

        difference = relativedelta(date_time_1, date_time_2)

        return "{years}, {months}, {days}, {hours}, {minutes}, {seconds}".format(
            years=pluralize(abs(difference.years), "year", "years"),
            months=pluralize(abs(difference.months), "month", "months"),
            days=pluralize(abs(difference.days), "day", "days"),
            hours=pluralize(abs(difference.hours), "hour", "hours"),
            minutes=pluralize(abs(difference.minutes), "minute", "minutes"),
            seconds=pluralize(abs(difference.seconds), "second", "seconds")
        )

    else:

        seconds_left = abs((date_time_2 - date_time_1).total_seconds())

        if not command.format:
            return pluralize(int(seconds_left / TIME_MAP["seconds_in_a_day"]), "day", "days")

        normalised_string = ""

        if "y" in command.format:
            years, seconds_left = divmod(seconds_left, TIME_MAP["seconds_in_a_year"])
            normalised_string += pluralize(int(years), "year", "years")

        if "m" in command.format:

            if normalised_string:
                normalised_string += ", "

            months, seconds_left = divmod(seconds_left, TIME_MAP["seconds_in_a_month"])
            normalised_string += pluralize(int(months), "month", "months")

        if "w" in command.format:

            if normalised_string:
                normalised_string += ", "

            weeks, seconds_left = divmod(seconds_left, TIME_MAP["seconds_in_a_week"])
            normalised_string += pluralize(int(weeks), "week", "weeks")

        if "d" in command.format:

            if normalised_string:
                normalised_string += ", "

            days, seconds_left = divmod(seconds_left, TIME_MAP["seconds_in_a_day"])
            normalised_string += pluralize(int(days), "day", "days")

        if "h" in command.format:

            if normalised_string:
                normalised_string += ", "

            hours, seconds_left = divmod(seconds_left, TIME_MAP["seconds_in_an_hour"])
            normalised_string += pluralize(int(hours), "hour", "hours")

        if "M" in command.format:

            if normalised_string:
                normalised_string += ", "

            minutes, seconds_left = divmod(seconds_left, TIME_MAP["seconds_in_a_minute"])
            normalised_string += pluralize(int(minutes), "minute", "minutes")

        if "s" in command.format:

            if normalised_string:
                normalised_string += ", "

            normalised_string += pluralize(int(seconds_left), "second", "seconds")

        return normalised_string


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
