from __future__ import unicode_literals, print_function

__author__ = 'raymond'

from pypeg2 import *

DATE_RE = re.compile(r'\d{2}\.\d{2}\.\d{2}')
TIME_RE = re.compile(r'\d{2}:\d{2}')
DATE_TIME_RE = re.compile(r'\d{2}\.\d{2}\.\d{2}@\d{2}:\d{2}')
TODAY_RE = re.compile(r'today')
NOW_RE = re.compile(r'now')

OPERATOR_RE = re.compile(r'[+-]')
TIMESPAN_RE = re.compile(r'[ymwdhMs]')
TIME_DIGITS_RE = re.compile(r'[0-9]+')


class Operator(str):
    grammar = OPERATOR_RE


class TimeSpans(str):
    grammar = attr("amount", TIME_DIGITS_RE), attr("timeSpan", TIMESPAN_RE)


class Operand(str):
    grammar = attr("operator", Operator), attr("timeSpans", some(TimeSpans))


class OperandList(List):
    grammar = maybe_some(Operand)


class DateFunction(Keyword):
    grammar = Enum(K("wn"))


class DateTime(str):
    grammar = [DATE_TIME_RE, DATE_RE, TIME_RE, TODAY_RE, NOW_RE]


class FunctionCall(str):
    grammar = attr("functionName", DateFunction), attr("dateTime", DateTime)


class Commands(List):
    grammar = [(attr("functionName", DateFunction), attr("dateTime", DateTime)),
               (attr("dateTime1", DateTime), "-", attr("dateTime2", DateTime)),
               (attr("dateTime", DateTime), attr("operandList", OperandList))]


def command_parse(command_str):
    return parse(command_str, Commands)


if __name__ == '__main__':
    command = parse("wn 11:35", Commands)

    print(command.functionName)
    print(command.dateTime)

    command = parse("21.03.13@12:15 + 6y 3d 2d - 10w 4h - 3d + 9h", Commands)
    print(command.dateTime)
    print(command.operandList[0].operator)
    print(command.operandList[0].timeSpans[0].amount)
    print(command.operandList[0].operator)
    print(command.operandList[0].timeSpans[1].amount)

    command = parse("now - 23.01.14@06:35", Commands)
    print(command.dateTime1)