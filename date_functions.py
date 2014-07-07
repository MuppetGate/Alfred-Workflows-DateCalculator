# This file contains all the functions that the workflow
# uses for specialised dates.
from datetime import datetime, date, timedelta
from date_format_mappings import DEFAULT_TIME_EXPR
from dateutil.easter import easter

# The DAY_MAP is specific to relative delta
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from dateutil.rrule import rrule, YEARLY

DAY_MAP = {"mon": relativedelta(days=+1, weekday=MO(+1)),
           "tue": relativedelta(days=+1, weekday=TU(+1)),
           "wed": relativedelta(days=+1, weekday=WE(+1)),
           "thu": relativedelta(days=+1, weekday=TH(+1)),
           "fri": relativedelta(days=+1, weekday=FR(+1)),
           "sat": relativedelta(days=+1, weekday=SA(+1)),
           "sun": relativedelta(days=+1, weekday=SU(+1))}


def _get_current_date():
    return datetime.combine(date.today(), datetime.max.time())


def _get_current_time():
    return datetime.combine(date.today(), datetime.now().time())


def current_date(date_format):
    return _get_current_date(), date_format


def current_time(date_format):
    del date_format # delete it because we're not using it.
    return _get_current_time(), DEFAULT_TIME_EXPR


def now(date_format):
    return datetime.now(), date_format + "@" + DEFAULT_TIME_EXPR


def yesterday(date_format):
    return _get_current_date() - timedelta(days=1), date_format


def tomorrow(date_format):
    return _get_current_date() + timedelta(days=1), date_format


def weekday(day_of_week_str):
    """
    This one one is a little bit trickier. We don't want a separate
    function for each day of the week, so we need to use a bit of
    currying to return a function that can handle the mapping.
    :param day: The day of the week as a string, which we will use to map into a table for the
    calculation.
    :param date_map: the format of the result
    :return: a function that will calculate the day of week and return it along with the format
    """
    def _weekday(date_format):
        return _get_current_date() + DAY_MAP[day_of_week_str.lower()], date_format

    return _weekday


def get_easter():
    this_date = _get_current_date()
    this_easter = datetime.combine(easter(this_date.year), datetime.min.time())
    if this_date < this_easter:
        return this_easter
    else:
        # We've already had easter this year
        next_year = datetime(this_date.year + 1, 1, 1)
        return datetime.combine(easter(next_year.year), datetime.min.time())


def next_easter(date_format):
    return get_easter(), date_format


def bst(month_number):
    """
    Use the rather clever dateutils functions
    to give us the last Sunday in March/October
    And currying rocks!
    :param date_format:
    :return:
    """
    def _bst(date_format):
        bst_rule = rrule(freq=YEARLY, bymonth=month_number, byweekday=SU(-1))
        return bst_rule.after(_get_current_date(), inc=False), date_format

    return _bst


DATE_FUNCTION_MAP = {

    "date": current_date,
    "today": current_date,
    "time": current_time,
    "now": now,
    "yesterday": yesterday,
    "tomorrow": tomorrow,
    "easter": next_easter,
    "mon": weekday('mon'),
    "tue": weekday('tue'),
    "wed": weekday('wed'),
    "thu": weekday('thu'),
    "fri": weekday('fri'),
    "sat": weekday('sat'),
    "sun": weekday('sun'),
    "start_bst": bst(3),
    "end_bst": bst(10)
}


