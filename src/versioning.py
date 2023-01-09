from __future__ import unicode_literals, print_function
from date_format_mappings import DEFAULT_ANNIVERSARIES, DEFAULT_TIME_FORMAT, DEFAULT_DATE_TIME_FORMAT, \
    DEFAULT_DATE_FORMAT


def update_settings(wf):
    """
    So what's this all about?
    Well, as we add new stuff to the workflow, the user's settings
    file might need some upgrades. They could just delete the settings
    file, but this might be much easier
    :return:
    """
    if "anniversaries" not in wf.settings:
        wf.settings['anniversaries'] = DEFAULT_ANNIVERSARIES

    if "date-format" not in wf.settings:
        wf.settings['date-format'] = DEFAULT_DATE_FORMAT

    if "time-format" not in wf.settings:
        wf.settings['time-format'] = DEFAULT_TIME_FORMAT

    if "date-time-format" not in wf.settings:
        wf.settings['date-time-format'] = DEFAULT_DATE_TIME_FORMAT