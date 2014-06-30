from __future__ import unicode_literals, print_function
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, DEFAULT_TIME_RE

from pypeg2 import *


class DateParser:

    def __init__(self, date_expr, settings):
        self.date_expression = date_expr
        self.settings = settings
        self.date_re = re.compile(self.date_expression)
        self.time_re = re.compile(DEFAULT_TIME_RE)
        self.date_time_re = re.compile(self.date_expression + '@' + DEFAULT_TIME_RE)
        self.date_macro_re = re.compile('date|today', re.IGNORECASE)
        self.time_macro_re = re.compile('time', re.IGNORECASE)
        self.now_macro_re = re.compile('now', re.IGNORECASE)
        self.yesterday_macro_re = re.compile('yesterday', re.IGNORECASE)
        self.tomorrow_macro_re = re.compile('tomorrow', re.IGNORECASE)
        self.days_of_week_re = re.compile('mon|tue|wed|thu|fri|sat|sun', re.IGNORECASE)
        self.easter_macro_re = re.compile('easter', re.IGNORECASE)
        self.user_macros_re = re.compile(self._get_anniversaries(self.settings), re.IGNORECASE)
        self.operator_re = re.compile('[+-]')
        self.time_span_re = re.compile('[ymwdhMs]')
        self.time_digits_re = re.compile('[0-9]+')
        self.format_re = re.compile('[ymwdhMs]+|long')
        self.functions_re = re.compile('wn|!', re.IGNORECASE)

    @staticmethod
    def _get_anniversaries(settings):
        """
        This method gets the anniversaries from the settings
        file and builds them into a regex string for the
        parser. This allows us to accept user-defined
        anniversaries as macros.
        :param settings:
        """
        # Nothing complicated. We're just creating a | separated string
        # by looping through keys and joining them.
        # Those funny characters we're prepending to the string are so we
        # can match an options "^" which we use to denote an absolute macro
        # invocation:
        # mybirthday ====> returns the date of my next birthday
        # ^mybirthday ===> the date I was born
        return '|'.join('\^?' + str(x) for x in settings['anniversaries'].keys())

    def parse_command(self, command_string):

        class Operator(str):
            grammar = self.operator_re

        class TimeSpans(str):
            grammar = attr("amount", self.time_digits_re), attr("span", self.time_span_re)

        class Operand(str):
            grammar = attr("operator", Operator), attr("timeSpans", some(TimeSpans))

        class OperandList(List):
            grammar = maybe_some(Operand)

        class DateFunction(str):
            grammar = self.functions_re

        class DateTime(str):
            grammar = [self.date_time_re, self.date_re, self.time_re,
                       self.date_macro_re, self.time_macro_re, self.now_macro_re,
                       self.yesterday_macro_re, self.days_of_week_re, self.tomorrow_macro_re,
                       self.easter_macro_re, self.user_macros_re]

        class Format(str):
            grammar = optional(self.format_re)

        class Commands(List):
            grammar = [
                (attr("functionName", DateFunction), attr("dateTime1", DateTime)),

                (attr("dateTime1", DateTime), attr("operandList1", OperandList), "-", attr("dateTime2", DateTime),
                 attr("operandList2", OperandList), attr("format", Format)),

                (attr("dateTime", DateTime), attr("operandList", OperandList))
            ]

        return parse(command_string, Commands)


if __name__ == '__main__':
    command_parser = DateParser("\d{2}\.\d{2}\.\d{2}", DEFAULT_WORKFLOW_SETTINGS)

    command = command_parser.parse_command("21.03.13 + 1y")
    print(command.dateTime)
    print(command.operandList[0].operator)
    print(command.operandList[0].timeSpans[0].amount)
    print(command.operandList[0].timeSpans[0].span)
