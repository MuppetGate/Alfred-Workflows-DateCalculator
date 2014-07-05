from __future__ import unicode_literals, print_function
import re
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS
from date_parser import DateParser
from pypeg2 import List, attr, parse, optional


class MacrosParser(DateParser):
    def __init__(self, date_expr, settings):
        # Call super constructor in an oddly clumsy way.

        DateParser.__init__(self, date_expr, settings)

        self.anniversary_name_re = re.compile('[a-z_]{2,}', re.IGNORECASE)
        self.add_command_re = re.compile('add', re.IGNORECASE)
        self.delete_command_re = re.compile('delete', re.IGNORECASE)
        self.edit_command_re = re.compile('edit', re.IGNORECASE)

    def parse_command(self, command_string=None):

        class DateTime(str):
            grammar = optional([self.date_time_re, self.date_re, self.time_re, self.date_functions_re, self.user_macros_re])

        class AnniversaryName(str):
            grammar = self.anniversary_name_re

        class Add(str):
            grammar = self.add_command_re

        class Delete(str):
            grammar = self.delete_command_re

        class Edit(str):
            grammar = self.edit_command_re

        class Commands(List):
            grammar = [
                (attr("delete", Delete), attr("anniversaryName", AnniversaryName)),
                (attr("edit", Edit), attr("anniversaryName", AnniversaryName), attr("dateTime", DateTime)),
                (attr("add", Add), attr("anniversaryName", AnniversaryName), attr("dateTime", DateTime))
            ]

        return parse(command_string, Commands)


if __name__ == '__main__':
    command_parser = MacrosParser("\d{2}\.\d{2}\.\d{2}", DEFAULT_WORKFLOW_SETTINGS)

    command = command_parser.parse_command("helen del")
    print(command.anniversaryName)
    #print(command.dateTime)


