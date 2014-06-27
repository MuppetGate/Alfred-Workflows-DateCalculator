from datetime import *

from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, DATE_MAPPINGS, DEFAULT_TIME_EXPR, DAY_MAP
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta
from parser import DateParser
from workflow import Workflow, ICON_ERROR
from humanfriendly import *


TIME_MAP = {"seconds_in_a_day": 86400,
            "seconds_in_a_week": 604800,
            "seconds_in_a_month": 2592000,
            "seconds_in_a_year": 31556952,
            "seconds_in_an_hour": 3600,
            "seconds_in_a_minute": 60}

# We've used the Gregorian average


def get_easter(date_format):
    current_date = datetime.today()
    this_easter = datetime.combine(easter(current_date.year), datetime.min.time())
    if current_date < this_easter:
        return this_easter, date_format
    else:
        # We've already had easter this year
        next_year = datetime(current_date.year + 1, 1, 1)
        return datetime.combine(easter(next_year.year), datetime.min.time()), date_format


def get_christmas(date_format):
    current_date = datetime.today()
    this_christmas = datetime(current_date.year, 12, 25)
    if current_date < this_christmas:
        return this_christmas, date_format
    else:
        # We've already had Crimbo this year
        return datetime(current_date.year + 1, 12, 25), date_format


def convert_date_time(date_time_str, date_format):
    # first of all, what format are we using.
    # We use the longer format if the date contains an ampersand
    # Remember at this point we know that the format is correct.

    full_format = date_format + "@" + DEFAULT_TIME_EXPR

    if date_time_str.lower() == "date" or date_time_str.lower() == "today":
        return datetime.today(), date_format

    if date_time_str.lower() == "time":
        return datetime.today(), DEFAULT_TIME_EXPR

    if date_time_str.lower() == "now":
        return datetime.today(), full_format

    if date_time_str.lower() == "yesterday":
        return datetime.today() - timedelta(days=1), date_format

    if date_time_str.lower() == "tomorrow":
        return datetime.today() + timedelta(days=1), date_format

    if date_time_str.lower() in DAY_MAP.keys():
        return datetime.today() + DAY_MAP[date_time_str.lower()], date_format

    if date_time_str.lower() == "easter":
        return get_easter(date_format)

    if date_time_str.lower() == "christmas":
        return get_christmas(date_format)

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


def do_functions(command, date_format):
    date_time, output_format = convert_date_time(command.dateTime1, date_format)

    if command.functionName.lower() == "wn" or command.functionName == "!":
        return "{week_number}".format(week_number=date_time.strftime("%V"))
    return None


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


def do_timespans(command, date_format):
    date_time, output_format = convert_date_time(command.dateTime, date_format)

    for operand in command.operandList:
        date_time = delta_arithmetic(date_time, operand)

    return date_time.strftime(output_format)


def do_subtraction(command, date_format):
    date_time_1, output_format_1 = convert_date_time(command.dateTime1, date_format)
    date_time_2, output_format_2 = convert_date_time(command.dateTime2, date_format)

    return normalised_days(command, date_time_1, date_time_2)


def normalised_days(command, date_time_1, date_time_2):
    # If the user selected long then he wants the full
    # date, so fill in the format before carrying on.

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

    key = wf.settings['date-format']
    args = wf.args

    date_mapping = DATE_MAPPINGS[key]

    command_parser = DateParser(date_mapping['regex'])

    try:

        command = command_parser.parse_command(args[0])

        if hasattr(command, "functionName"):
            output = do_functions(command, date_mapping['date-format'])

        elif hasattr(command, "dateTime"):
            output = do_timespans(command, date_mapping['date-format'])

        elif hasattr(command, "dateTime1") and hasattr(command, "dateTime2"):
            output = do_subtraction(command, date_mapping['date-format'])

        else:
            output = "Invalid Expression"

    except SyntaxError:
        output = "Invalid Command"

    except ValueError:
        output = "Invalid Date"

    if output.startswith("Invalid"):
        wf.add_item(title=output, subtitle="", valid=False, arg=args[0], icon=ICON_ERROR)
    else:
        wf.add_item(title=output, subtitle="Copy to clipboard", valid=True, arg=output)

    wf.send_feedback()

# ## Python calling routine. Will only run this app if it is the main program
# ## Otherwise it won't run because it is an included module -- clever!

if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))

