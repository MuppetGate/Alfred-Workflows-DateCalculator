from __future__ import unicode_literals, print_function
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, WN_FUNCTION_REGEX
from date_formatters import DATE_FORMATTERS_MAP
from date_functions import DATE_FUNCTION_MAP, get_date_format_regex, get_time_format_regex, get_full_format_regex, \
    DAYS_OF_WEEK_ABBREVIATIONS, EXCLUSION_MAP

from pypeg2 import *


class DateParser:
    def __init__(self, settings):
        self.date_expression = get_date_format_regex(settings)
        self.time_expression = get_time_format_regex(settings)
        self.full_date_time_expression = get_full_format_regex(settings)
        self.settings = settings
        self.date_re = re.compile(self.date_expression, re.IGNORECASE)
        self.time_re = re.compile(self.time_expression, re.IGNORECASE)
        self.date_time_re = re.compile(self.full_date_time_expression, re.IGNORECASE)
        self.date_functions_re = re.compile(self._get_date_functions(), re.IGNORECASE)
        self.user_macros_re = re.compile(self._get_anniversaries(self.settings), re.IGNORECASE)
        self.operator_re = re.compile(r'[+-]')
        self.time_span_re = re.compile(r'[ymwdhMs]')
        self.time_digits_re = re.compile(r'[0-9]+')
        self.format_re = re.compile(r'[ymwdhMs]+|long')
        self.date_formatters_re = re.compile(self._get_date_formatters(), re.IGNORECASE)

        # This is for the exclusions
        self.exclusion_keyword_re = re.compile(r'exclude|ex|x')
        self.exclusion_macro_re = re.compile(self._get_exclusion_macros(), re.IGNORECASE)
        self.exclusion_range_operator_re = re.compile(r'to|until', re.IGNORECASE)

        # The money shot
        self.parseable_date_re = re.compile(r'\"[^\"]+\"', re.IGNORECASE)

        # Week number calculation
        self.wn_command_re = WN_FUNCTION_REGEX

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
        later on. Note that we escape the strings during concatenation
        so that we can use symbols like '*' for abbreviated keywords.
        :return: a regex string of allowable function names
        """
        return '|'.join(re.escape(str(x)) for x in DATE_FORMATTERS_MAP.keys())

    @staticmethod
    def _get_date_functions():
        return '|'.join(re.escape(str(x)) for x in DATE_FUNCTION_MAP.keys())

    @staticmethod
    def _get_week_days():
        return '|'.join(re.escape(str(x)) for x in DAYS_OF_WEEK_ABBREVIATIONS.keys())

    @staticmethod
    def _get_exclusion_macros():
        return '|'.join(re.escape(str(x)) for x in EXCLUSION_MAP.keys())

    def parse_command(self, command_string):
        class Operator(str):
            grammar = self.operator_re

        class TimeSpans(str):
            grammar = attr("amount", self.time_digits_re), attr("span", self.time_span_re)

        class Operand(str):
            grammar = attr("operator", Operator), attr("timeSpans", some(TimeSpans))

        class OperandList(List):
            grammar = maybe_some(Operand)

        class DateFormat(str):
            grammar = self.date_formatters_re

        class DateTime(str):
            grammar = [self.date_time_re, self.date_re, self.time_re, self.date_functions_re, self.user_macros_re,
                       self.parseable_date_re, self.wn_command_re]

        class Format(str):
            grammar = optional(self.format_re)

        class ExclusionKeyword(str):
            grammar = self.exclusion_keyword_re

        class ExclusionRange(str):
            grammar = attr("fromDateTime", DateTime), self.exclusion_range_operator_re, attr("toDateTime", DateTime)

        class ExclusionType(List):
            grammar = [attr("exclusionRange", ExclusionRange),
                       attr("exclusionDateTime", DateTime), attr("exclusionMacro", self.exclusion_macro_re)]

        class ExclusionList(List):
            grammar = some(ExclusionType)

        class ExclusionCommands(str):
            grammar = attr("exclusionKeyword", ExclusionKeyword), attr("exclusionList", ExclusionList)

        class Commands(str):
            grammar = [

                (attr("dateTime1", DateTime), attr("operandList1", OperandList), "-", attr("dateTime2", DateTime),
                 attr("operandList2", OperandList),
                 attr("format", Format)),

                (attr("dateTime", DateTime), attr("operandList", OperandList),
                 attr("dateFormat", DateFormat)),

                (attr("dateTime", DateTime), attr("operandList", OperandList),
                 attr("exclusionCommands", ExclusionCommands),
                 attr("dateFormat", DateFormat)),

                (attr("dateTime", DateTime), attr("operandList", OperandList),
                 attr("exclusionCommands", ExclusionCommands)),

                (attr("dateTime", DateTime), attr("dateFormat", DateFormat)),

                (attr("dateTime", DateTime), attr("operandList", OperandList))

            ]

        return parse(command_string, Commands)


if __name__ == '__main__':
    command_parser = DateParser(DEFAULT_WORKFLOW_SETTINGS)
    command = command_parser.parse_command("27.01.14 - 01.01.14 + 1d")
    print(command.dateTime)
    print(command.operandList[0].operator)
    print(command.operandList[0].timeSpans[0].amount)
    print(command.operandList[0].timeSpans[0].span)
