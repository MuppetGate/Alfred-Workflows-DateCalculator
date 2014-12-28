from __future__ import unicode_literals, print_function
from date_exclusion_rules import DATE_EXCLUSION_RULES_MAP
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, DEFAULT_TIME_RE, TIME_MAPPINGS
from date_formatters import DATE_FORMATTERS_MAP
from date_functions import DATE_FUNCTION_MAP

from pypeg2 import *


class DateParser:

    def __init__(self, date_expr, time_expr, settings):
        self.date_expression = date_expr
        self.time_expression = time_expr
        self.settings = settings
        self.date_re = re.compile(self.date_expression)
        self.time_re = re.compile(self.time_expression)
        self.date_time_re = re.compile(self.date_expression + '@' + self.time_expression)
        self.date_functions_re = re.compile(self._get_date_functions(), re.IGNORECASE)
        self.user_macros_re = re.compile(self._get_anniversaries(self.settings), re.IGNORECASE)
        self.operator_re = re.compile('[+-]')
        self.time_span_re = re.compile('[ymwdhMs]')
        self.time_digits_re = re.compile('[0-9]+')
        self.format_re = re.compile('[ymwdhMs]+|long')
        self.date_formatters_re = re.compile(self._get_date_formatters(), re.IGNORECASE)

        # Exclusions from date subtraction calculations.
        self.exclusion_keyword_re = re.compile('exclude|ex|x', re.IGNORECASE)
        self.exclusion_macros_re = re.compile(self._get_exclusion_macros(), re.IGNORECASE)
        self.exclusion_range_operator_re = re.compile('to|until', re.IGNORECASE)

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

    @staticmethod
    def _get_date_formatters():
        """
        This method will get the list of defnined functions and build
        a regular expression from them so that they can be interpreted
        later on
        :return: a regex string of allowable function names
        """
        return '|'.join(str(x) for x in DATE_FORMATTERS_MAP.keys())

    @staticmethod
    def _get_date_functions():
        return '|'.join(str(x) for x in DATE_FUNCTION_MAP.keys())

    @staticmethod
    def _get_exclusion_macros():
        return '|'.join(str(x) for x in DATE_EXCLUSION_RULES_MAP.keys())

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
            grammar = self.date_formatters_re

        class DateTime(str):
            grammar = [self.date_time_re, self.date_re, self.time_re, self.date_functions_re, self.user_macros_re]

        class Format(str):
            grammar = optional(self.format_re)

        class ExclusionKeyword(str):
            grammar = self.exclusion_keyword_re

        class ExclusionRange(str):
            grammar = attr("fromDateTime", DateTime), self.exclusion_range_operator_re, attr("toDateTime", DateTime)

        class ExclusionType(List):
            grammar = [attr("exclusionRange", ExclusionRange),
                       attr("exclusionDateTime", DateTime), attr("exclusionMacro", self.exclusion_macros_re)]

        class ExclusionList(List):
            grammar = some(ExclusionType)

        class ExclusionCommand(str):
            grammar = attr("exclusionKeyword", ExclusionKeyword), attr("exclusionList", ExclusionList)

        class ExclusionCommands(List):
            grammar = maybe_some(ExclusionCommand)

        class Commands(str):
            grammar = [
                (attr("dateTime", DateTime), attr("operandList", OperandList), attr("functionName", DateFunction)),

                (attr("dateTime", DateTime), attr("functionName", DateFunction)),

                (attr("dateTime1", DateTime), attr("operandList1", OperandList), "-", attr("dateTime2", DateTime),
                 attr("operandList2", OperandList),
                 attr("exclusionCommands", ExclusionCommands), attr("format", Format)),

                (attr("dateTime", DateTime), attr("operandList", OperandList))
            ]

        return parse(command_string, Commands)


if __name__ == '__main__':

    command_parser = DateParser("\d{2}\.\d{2}\.\d{2}", DEFAULT_WORKFLOW_SETTINGS)
    command = command_parser.parse_command("27.01.14 - 01.01.14 + 1d")
    print(command.dateTime)
    print(command.operandList[0].operator)
    print(command.operandList[0].timeSpans[0].amount)
    print(command.operandList[0].timeSpans[0].span)
