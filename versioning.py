from __future__ import unicode_literals, print_function
from date_format_mappings import DEFAULT_ANNIVERSARIES


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

