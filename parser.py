from __future__ import unicode_literals, print_function

__author__ = 'raymond'

from pypeg2 import *


class DateParser:

    def __init__(self, date_expr):
        self.date_expression = date_expr

    def parse_command(self, command_string):

        date_re = re.compile(self.date_expression)
        time_re = re.compile('\d{2}:\d{2}')
        date_time_re = re.compile(self.date_expression + '@' + '\d{2}:\d{2}')
        date_macro_re = re.compile('date|today', re.IGNORECASE)
        time_macro_re = re.compile('time', re.IGNORECASE)
        now_macro_re = re.compile('now', re.IGNORECASE)
        yesterday_macro_re = re.compile('yesterday', re.IGNORECASE)
        tomorrow_macro_re = re.compile('tomorrow', re.IGNORECASE)
        days_of_week_re = re.compile('mon|tue|wed|thu|fri|sat|sun', re.IGNORECASE)

        operator_re = re.compile('[+-]')
        time_span_re = re.compile('[ymwdhMs]')
        time_digits_re = re.compile('[0-9]+')
        format_re = re.compile('[ymwdhMs]+|long')
        functions_re = re.compile('wn|!', re.IGNORECASE)

        class Operator(str):
            grammar = operator_re

        class TimeSpans(str):
            grammar = attr("amount", time_digits_re), attr("span", time_span_re)

        class Operand(str):
            grammar = attr("operator", Operator), attr("timeSpans", some(TimeSpans))

        class OperandList(List):
            grammar = maybe_some(Operand)

        class DateFunction(str):
            grammar = functions_re

        class DateTime(str):
            grammar = [date_time_re, date_re, time_re,
                       date_macro_re, time_macro_re, now_macro_re,
                       yesterday_macro_re, days_of_week_re, tomorrow_macro_re]

        class Format(str):
            grammar = optional(format_re)

        class Commands(List):
            grammar = [(attr("functionName", DateFunction), attr("dateTime1", DateTime)),
                       (attr("dateTime1", DateTime), "-", attr("dateTime2", DateTime), attr("format", Format)),
                       (attr("dateTime", DateTime), attr("operandList", OperandList))]

        return parse(command_string, Commands)

if __name__ == '__main__':

    command_parser = DateParser("\d{2}\.\d{2}\.\d{2}")

    command = command_parser.parse_command("21.03.13 + 1y")
    print(command.dateTime)
    print(command.operandList[0].operator)
    print(command.operandList[0].timeSpans[0].amount)
    print(command.operandList[0].timeSpans[0].span)
