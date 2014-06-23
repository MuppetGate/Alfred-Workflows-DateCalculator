import sys

from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from pyparsing import *
import pyparsing

# Some utility functions that don't really
# belong anywhere else


def convert_to_date(date_string, time_string, date_format):
    # If you cannot convert the date here then
    # exit and send back an error message 

    if date_string and date_string != "today":
        converted_date = datetime.strptime(date_string, date_format)
    else:
        converted_date = datetime.today()

    if time_string and time_string != "now":
        converted_time = datetime.strptime(time_string, "%H:%M").time()
    else:
        converted_time = datetime.now().time()

    converted_datetime = datetime.combine(converted_date, converted_time)

    return converted_datetime


def int_or_empty(int_or_empty_str):
    if int_or_empty_str:
        return int(int_or_empty_str)
    else:
        return 0

    # Using pyparsing, we're going to build a grammar parseString
    # for parsing the date command coming in from Alfred. Trick is
    # to accept the options paramaters in any order


def get_date_grammar(date_expression, time_expression):
    date_parse_expression = pyparsing.Regex(date_expression)
    time_parse_expression = pyparsing.Regex(time_expression)

    date_template = Combine(date_parse_expression ^ oneOf("today", caseless=True))
    time_template = Combine(time_parse_expression ^ oneOf("now", caseless=True))

    date_1 = date_template.setResultsName("date_1")
    date_2 = date_template.setResultsName("date_2")
    time_1 = time_template.setResultsName("time_1")
    time_2 = time_template.setResultsName("time_2")

    datetime_1 = date_1 ^ time_1 ^ (date_1 + "@" + time_1)
    datetime_2 = date_2 ^ time_2 ^ (date_2 + "@" + time_2)

    plus_operator = oneOf("+").setResultsName("operator")
    minus_operator = oneOf("-").setResultsName("operator")
    week_operator = oneOf("^").setResultsName("operator")

    add_years = Word(nums, min=1).setResultsName("years_to_add")
    add_months = Word(nums, min=1).setResultsName("months_to_add")
    add_weeks = Word(nums, min=1).setResultsName("weeks_to_add")
    add_days = Word(nums, min=1).setResultsName("days_to_add")
    add_hours = Word(nums, min=1).setResultsName("hours_to_add")
    add_minutes = Word(nums, min=1).setResultsName("minutes_to_add")
    add_seconds = Word(nums, min=1).setResultsName("seconds_to_add")

    years_option = Optional(add_years + CaselessLiteral("y"))
    months_option = Optional(add_months + Literal("m"))
    weeks_option = Optional(add_weeks + CaselessLiteral("w"))
    days_option = Optional(add_days + CaselessLiteral("d"))
    hours_option = Optional(add_hours + CaselessLiteral("h"))
    minutes_option = Optional(add_minutes + Literal("M"))
    seconds_option = Optional(add_seconds + CaselessLiteral("s"))

    addition_options = (Each(
        [years_option, months_option, days_option, weeks_option, days_option, hours_option, minutes_option,
         seconds_option])).setResultsName("options")

    format_options = Word(alphanums, min=1)
    long_format = Optional("long").setResultsName("long_format")

    format_expression = Optional(format_options ^ long_format).setResultsName("format_expression")

    date_addition = datetime_1 + plus_operator + addition_options
    date_substraction = datetime_1 + minus_operator + datetime_2 + format_expression
    date_substraction_by_numbers = datetime_1 + minus_operator + addition_options
    week_number_command = week_operator + datetime_1

    date_calculation_grammar = date_addition ^ date_substraction ^ date_substraction_by_numbers ^ week_number_command
    return date_calculation_grammar