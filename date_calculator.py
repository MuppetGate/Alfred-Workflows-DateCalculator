import calendar
from collections import Counter
from datetime import timedelta

import arrow
from arrow.arrow import datetime
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, \
    TIME_CALCULATION, VALID_FORMAT_OPTIONS, MAX_LOOKAHEAD_IN_DAYS
from date_formatters import DATE_FORMATTERS_MAP
from date_functions import EXCLUSION_MAP, DATE_EXCLUSION_RULES_MAP
from date_parser import DateParser
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rruleset, rrule, DAILY
from humanfriendly import *
from utils import convert_date_time
from versioning import update_settings
from workflow import Workflow, ICON_ERROR


class FormatError(Exception):
    """
    Throw this when there are
    repeated characters in the
    format field.
    """
    pass


class IncompatibleFunctionError(Exception):
    """
    Throw this bad boy when someone attempts
    to use the exclusions with the formatting.
    """
    pass


class UnknownExclusionTypeError(Exception):
    """
    This exception is thrown when we encounter an exclusion type that
    somehow makes it through the checking list. Shouldn't occur really,
    but if it does then we want to know about it.
    """
    pass


class ExclusionTooFarAheadError(Exception):
    """
    We'll throw this bad boy if the exclusion calculations goes
    further than a preset value. We don't want the process running years into the future
    """
    pass


class ExclusionNoDaysFoundError(Exception):
    """
    We're going to check to make sure that the user doesn't
    enter an exclusion clause that blocks out all the days in the
    week. Should be easy to find. If the exclusion set has seven
    items in it, then that's all the days in the week!
    """
    pass


def do_formats(command, settings):
    date_time, _ = convert_date_time(command.dateTime, settings)

    if command.dateFormat.lower() in DATE_FORMATTERS_MAP:
        # noinspection PyCallingNonCallable
        return DATE_FORMATTERS_MAP[command.dateFormat.lower()](date_time)
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


def do_timespans(command, settings):
    date_time, output_format = convert_date_time(command.dateTime, settings)
    original_date_time = date_time

    for operand in command.operandList:
        date_time = delta_arithmetic(date_time, operand)

    # TODO this is where you're going to slot in the exclusion check
    date_time = exclusion_check(original_date_time, date_time, command, settings)

    return date_time.strftime(output_format)


def do_subtraction(command, settings):
    date_time_1, output_format_1 = convert_date_time(command.dateTime1, settings)
    date_time_2, output_format_2 = convert_date_time(command.dateTime2, settings)

    # In a moment of madness, we've decided to allow operands in a date from date
    # subtraction. It's much easier to process these first.
    if hasattr(command, "operandList1"):
        for operand in command.operandList1:
            date_time_1 = delta_arithmetic(date_time_1, operand)

    if hasattr(command, "operandList2"):
        for operand in command.operandList2:
            date_time_2 = delta_arithmetic(date_time_2, operand)

    return normalised_days(command, date_time_1, date_time_2)


def exclusion_check(original_date_time, date_time, command, settings):
    if not hasattr(command, "exclusionCommands"):
        return date_time

    extra_days = calculate_rrule_exclusions(original_date_time, date_time, command.exclusionCommands, settings)

    lookahead_date = date_time + timedelta(days=extra_days)

    exclusion_day_set = build_exclusion_day_set(command.exclusionCommands)

    # if there are seven elements in the exclusion day set then there is no way
    # we can calculate the exclusions, so throw an error

    if len(exclusion_day_set) >= 7:
        raise ExclusionNoDaysFoundError

    exclusion_dates = build_exclusion_date_set(command.exclusionCommands, settings)
    exclusion_dates.update(build_exclusion_range_set(command.exclusionCommands, settings))

    lookahead_count = 0

    while (calendar.day_name[lookahead_date.weekday()] in exclusion_day_set
           or lookahead_date in exclusion_dates):

        lookahead_date = lookahead_date + timedelta(days=1)
        lookahead_count = lookahead_count + 1

        if lookahead_count >= MAX_LOOKAHEAD_IN_DAYS:
            raise ExclusionTooFarAheadError

    return lookahead_date


def build_exclusion_day_set(exclusion_commands):
    excluded_days = set()

    exclusion_types = exclusion_commands.exclusionList

    for exclusionType in exclusion_types:

        if hasattr(exclusionType, "exclusionMacro"):
            excluded_days.update(EXCLUSION_MAP[exclusionType.exclusionMacro])

    return excluded_days


def build_exclusion_date_set(exclusion_commands, settings):
    excluded_dates = set()

    exclusion_types = exclusion_commands.exclusionList

    for exclusionType in exclusion_types:

        if hasattr(exclusionType, "exclusionDateTime"):
            real_date, _ = convert_date_time(exclusionType.exclusionDateTime, settings)
            excluded_dates.add(real_date)

    return excluded_dates


def build_exclusion_range_set(exclusion_commands, settings):
    exclusion_range_set = set()

    exclusion_types = exclusion_commands.exclusionList

    for exclusionType in exclusion_types:

        if hasattr(exclusionType, "exclusionRange"):

            from_date, _ = convert_date_time(exclusionType.exclusionRange.fromDateTime, settings)
            to_date, _ = convert_date_time(exclusionType.exclusionRange.toDateTime, settings)

            while from_date <= to_date:
                exclusion_range_set.add(from_date)
                from_date = from_date + timedelta(days=1)

    return exclusion_range_set


def calculate_rrule_exclusions(start_date, end_date, exclusion_commands, settings):
    exclusion_ruleset = rruleset()

    exclusion_types = exclusion_commands.exclusionList

    for exclusion_type in exclusion_types:

        if hasattr(exclusion_type, "exclusionRange"):
            from_date, _ = convert_date_time(exclusion_type.exclusionRange.fromDateTime, settings)
            to_date, _ = convert_date_time(exclusion_type.exclusionRange.toDateTime, settings)
            exclusion_ruleset.rrule(rrule(freq=DAILY, dtstart=from_date, until=to_date))

        elif hasattr(exclusion_type, "exclusionDateTime"):
            real_date, _ = convert_date_time(exclusion_type.exclusionDateTime, settings)
            exclusion_ruleset.rrule(rrule(freq=DAILY, dtstart=real_date, until=real_date))

        elif hasattr(exclusion_type, "exclusionMacro"):
            macro_value = exclusion_type.exclusionMacro
            exclusion_rule = DATE_EXCLUSION_RULES_MAP[macro_value](start=start_date, end=end_date)
            exclusion_ruleset.rrule(exclusion_rule)
        else:
            # in that case, I have no idea what this is (the parser should have caught it) so just
            # raise an error or something
            raise UnknownExclusionTypeError

    matched_dates = list(exclusion_ruleset.between(after=start_date, before=end_date, inc=True))

    return len(matched_dates)


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


def tack_on_time(date_time):
    return datetime.combine(date_time, datetime.max.time())


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
    :param interval: The interval we're calculating over: year, month, week, day, hour, minute or second.
    :param start_datetime: When you're counting from
    :param end_datetime:  When you're counting to.
    :return:
    """

    datetime_list = arrow.Arrow.range(interval, start_datetime, end_datetime)

    if datetime_list:
        return len(datetime_list) - 1, datetime_list[-1]
    else:
        return 0, start_datetime


def later_date_last(date_time_1, date_time_2):
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

    return start_date_time, end_date_time


def normalised_days(command, date_time_1, date_time_2):
    # If the user selected long then he wants the full
    # date, so fill in the format before carrying on.

    # First off, do we have any exclusions to worry about?
    if not valid_command_format(command.format):
        raise FormatError

    if command.format == "long":
        difference = relativedelta(date_time_1, date_time_2)

        return "{years}, {months}, {days}, {hours}, {minutes}, {seconds}".format(
            years=pluralize(abs(difference.years), TIME_CALCULATION['y']['singular'], TIME_CALCULATION['y']['plural']),
            months=pluralize(abs(difference.months), TIME_CALCULATION['m']['singular'],
                             TIME_CALCULATION['m']['plural']),
            days=pluralize(abs(difference.days), TIME_CALCULATION['d']['singular'], TIME_CALCULATION['d']['plural']),
            hours=pluralize(abs(difference.hours), TIME_CALCULATION['h']['singular'], TIME_CALCULATION['h']['plural']),
            minutes=pluralize(abs(difference.minutes), TIME_CALCULATION['M']['singular'],
                              TIME_CALCULATION['M']['plural']),
            seconds=pluralize(abs(difference.seconds), TIME_CALCULATION['s']['singular'],
                              TIME_CALCULATION['s']['plural']))

    # Python gotcha. The keys in the map are not guaranteed
    # to come out in the same order you put then; so we have
    # to scan them specifically in the order we want them to
    # appear in the calculation. If they're out of sequence
    # then the calculation will return the wrong result.
    # And it does matter which way round the dates go.
    date_1, date_2 = later_date_last(date_time_1, date_time_2)

    start_date_time = arrow.get(date_1)
    end_date_time = arrow.get(date_2)

    if command.format:
        ordered_format_options = [option for option in VALID_FORMAT_OPTIONS if option in command.format]
        show_zero_items = True
    else:
        ordered_format_options = VALID_FORMAT_OPTIONS
        show_zero_items = False

    normalised_elements = []

    for x in ordered_format_options:

        count, start_date_time = calculate_time_interval(TIME_CALCULATION[x]['interval'],
                                                         start_date_time, end_date_time)

        # If this is the last format option in the list, then we need some
        # fractional magic! Remember, the next line only works because the
        # items in the list are unique and sorted into order! If this changes
        # then you should use an enumerate call
        if x == ordered_format_options[-1]:
            fractional = abs((end_date_time - start_date_time).total_seconds()) / TIME_CALCULATION[x]['seconds']
            count += fractional

        # If no format is set then go for a compact display that suppresses all items that are
        # zero. And don't bother showing the seconds calculation under any circumstances. It is pretty
        # useless and prone to error.
        if (show_zero_items or count > 0) and TIME_CALCULATION[x]['interval'] != 'second':
            normalised_elements.append(pluralize(round_number(count), TIME_CALCULATION[x]['singular'],
                                                 TIME_CALCULATION[x]['plural']))

    # We put each part of the calculation in a list
    # so that Python can handle comma-separating them later on
    return ', '.join(normalised_elements)


def main(wf):
    # Get the date format from the configuration

    update_settings(wf)
    args = wf.args
    command_parser = DateParser(wf.settings)

    try:

        command = command_parser.parse_command(args[0])

        if hasattr(command, "dateTime"):
            output = do_timespans(command, wf.settings)

            if hasattr(command, "dateFormat"):
                setattr(command, "dateTime", output)
                # and run it through the functions function
                output = do_formats(command, wf.settings)

        elif hasattr(command, "dateTime1") and hasattr(command, "dateTime2"):
            output = do_subtraction(command, wf.settings)

        else:
            output = "Invalid Expression"

    except SyntaxError:
        output = "Invalid Command"

    except ValueError:
        output = "Invalid Date/time"

    except FormatError:
        output = "Invalid format"

    except IncompatibleFunctionError:
        output = "Invalid command - Don't use exclusions and formats together."

    except UnknownExclusionTypeError:
        output = "Invalid exclusion - Try again."

    except ExclusionNoDaysFoundError:
        output = "All days excluded"

    except ExclusionTooFarAheadError:
        output = "That's too far into the future"

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
