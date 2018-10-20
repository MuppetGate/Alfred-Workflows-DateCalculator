# This file contains all the functions that the workflow
# uses for specialised dates.
from math import floor

from arrow.arrow import datetime, timedelta
# The DAY_MAP is specific to relative delta
from date_format_mappings import DATE_MAPPINGS, TIME_MAPPINGS, DATE_TIME_MAPPINGS
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from dateutil.rrule import rrule, YEARLY, DAILY

DAY_MAP = {

    "mon": relativedelta(days=+1, weekday=MO(+1)),
    "tue": relativedelta(days=+1, weekday=TU(+1)),
    "wed": relativedelta(days=+1, weekday=WE(+1)),
    "thu": relativedelta(days=+1, weekday=TH(+1)),
    "fri": relativedelta(days=+1, weekday=FR(+1)),
    "sat": relativedelta(days=+1, weekday=SA(+1)),
    "sun": relativedelta(days=+1, weekday=SU(+1)),

    "prev mon": relativedelta(days=-1, weekday=MO(-1)),
    "prev tue": relativedelta(days=-1, weekday=TU(-1)),
    "prev wed": relativedelta(days=-1, weekday=WE(-1)),
    "prev thu": relativedelta(days=-1, weekday=TH(-1)),
    "prev fri": relativedelta(days=-1, weekday=FR(-1)),
    "prev sat": relativedelta(days=-1, weekday=SA(-1)),
    "prev sun": relativedelta(days=-1, weekday=SU(-1)),
}

DAYS_OF_WEEK_ABBREVIATIONS = {

    "mon": "monday",
    "tue": "tuesday",
    "wed": "wednesday",
    "thu": "thursday",
    "fri": "friday",
    "sat": "saturday",
    "sun": "sunday"
}


def get_date_format(settings):
    return DATE_MAPPINGS[settings['date-format']]['date-format']


def get_time_format(settings):
    return TIME_MAPPINGS[settings['time-format']]['time-format']


def get_full_format(settings):
    return DATE_TIME_MAPPINGS[settings['date-time-format']]['date-time-format'](
        DATE_MAPPINGS[settings['date-format']]['date-format'],
        TIME_MAPPINGS[settings['time-format']]['time-format'])


def get_date_format_regex(settings):
    return DATE_MAPPINGS[settings['date-format']]['regex']


def get_time_format_regex(settings):
    return TIME_MAPPINGS[settings['time-format']]['regex']


def get_full_format_regex(settings):
    return DATE_TIME_MAPPINGS[settings['date-time-format']]['date-time-format'](
        DATE_MAPPINGS[settings['date-format']]['regex'],
        TIME_MAPPINGS[settings['time-format']]['regex'])


def get_time_preprocessor(settings):
    return TIME_MAPPINGS[settings['time-format']]['pre-process']


def _get_current_date():
    return datetime.combine(datetime.today(), datetime.max.time())


def _get_current_time():
    return datetime.combine(datetime.today(), datetime.now().time())


def current_date(settings):
    return _get_current_date(), get_date_format(settings)


def current_time(settings):
    return _get_current_time(), get_time_format(settings)


def now(settings):
    return datetime.now(), get_full_format(settings)


def yesterday(settings):
    return _get_current_date() - timedelta(days=1), get_date_format(settings)


def tomorrow(settings):
    return _get_current_date() + timedelta(days=1), get_date_format(settings)


def weekday(day_of_week_str):
    """
    This one one is a little bit trickier. We don't want a separate
    function for each day of the week, so we need to use a bit of
    currying to return a function that can handle the mapping.
    :param day_of_week_str: The day of the week as a string, which we will use to map into a table for the
    calculation.
    :return: a function that will calculate the day of week and return it along with the format
    """

    def _weekday(settings):
        return _get_current_date() + DAY_MAP[day_of_week_str.lower()], get_date_format(settings)

    return _weekday


def next_easter(settings):
    easter_rule = rrule(freq=YEARLY, byeaster=0)
    return easter_rule.after(_get_current_date(), inc=False), get_date_format(settings)


def start_of_year(settings):
    return datetime(year=_get_current_date().year, day=1, month=1), get_date_format(settings)


def end_of_year(settings):
    return datetime(year=_get_current_date().year, day=31, month=12), get_date_format(settings)


def next_month(settings):
    return datetime(year=_get_current_date().year, day=1, month=_get_current_date().month + 1), \
           get_date_format(settings)


def next_passover(settings):
    """
    Credit goes to programmingpraxis.com for supplying
    the function for working out the date of the passover
    """

    def calc_passover_year(year):
        return datetime(year, 3, 21) + timedelta(rosh_hashanah(year))

    def rosh_hashanah(year):

        g = year % 19 + 1
        r = 12 * g % 19

        v = (floor(year / 100.0) - floor(year / 400.0) - 2)
        v += 765433.0 * r / 492480
        v += (year % 4) / 4.0
        v -= (313.0 * year + 89081) / 98496

        n = int(v)
        f = v - n

        # Monday .. Sunday = 0..6
        dow = (datetime(year, 8, 31).weekday() + n) % 7

        if dow in (2, 4, 6):
            n += 1
        elif dow == 0 and f >= 23269.0 / 25920 and r > 11:
            n += 1
        elif dow == 1 and f >= 1367.0 / 2160 and r > 6:
            n += 2

        return n

    # Just need the year of the current date
    passover_date = calc_passover_year(_get_current_date().year)

    # if we've already gone past it then we need to try for the following year.
    if passover_date >= _get_current_date():
        return passover_date, get_date_format(settings)
    else:
        return calc_passover_year(_get_current_date().year + 1), get_date_format(settings)


def bst(month_number):
    """
    Use the rather clever dateutils functions
    to give us the last Sunday in March/October
    And currying rocks!
    :param month_number:
    :return:
    """

    def _bst(settings):
        bst_rule = rrule(freq=YEARLY, bymonth=month_number, byweekday=SU(-1))
        return bst_rule.after(_get_current_date(), inc=False), get_date_format(settings)

    return _bst


def around_easter(days):
    """
    We're being clever again. This is a function that returns a function
    that returns dates as an offset of Easter. Mainly so we can find
    Pancake Day
    :param days:
    :return:
    """

    def _easter_offset(settings):
        easters = list(rrule(freq=YEARLY, byeaster=0, count=2))
        offset_date = easters[0] + timedelta(days=days)

        if _get_current_date() > offset_date:
            offset_date = easters[1] + timedelta(days=days)

        return offset_date, get_date_format(settings)

    return _easter_offset


def mothers_day_us(settings):
    """
    Yes, Mother's day in the US is different to the UK one. It is
    always the second Sunday in May.
    :param settings:
    :return:
    """

    mothers_day_rule = rrule(freq=YEARLY, bymonth=5, byweekday=SU(2))
    return mothers_day_rule.after(_get_current_date()), get_date_format(settings)


def martin_luther_king_day(settings):
    mlk_day_rule = rrule(freq=YEARLY, bymonth=1, byweekday=MO(3))
    return mlk_day_rule.after(_get_current_date()), get_date_format(settings)


DATE_FUNCTION_MAP = {

    "date": current_date,
    "today": current_date,
    "*": current_date,
    "time": current_time,
    "&": current_time,
    "now": now,
    "#": now,
    "yesterday": yesterday,
    "<": yesterday,
    "tomorrow": tomorrow,
    ">": tomorrow,
    "easter": next_easter,
    "next mon": weekday('mon'),
    "next tue": weekday('tue'),
    "next wed": weekday('wed'),
    "next thu": weekday('thu'),
    "next fri": weekday('fri'),
    "next sat": weekday('sat'),
    "next sun": weekday('sun'),
    "prev mon": weekday('prev mon'),
    "prev tue": weekday('prev tue'),
    "prev wed": weekday('prev wed'),
    "prev thu": weekday('prev thu'),
    "prev fri": weekday('prev fri'),
    "prev sat": weekday('prev sat'),
    "prev sun": weekday('prev sun'),
    "start bst": bst(3),
    "end bst": bst(10),
    "start year": start_of_year,
    "end year": end_of_year,
    "next month": next_month,
    "passover": next_passover,
    "pancake day": around_easter(-47),
    "lent": around_easter(-46),
    "mlk": martin_luther_king_day,
    "mum": around_easter(-21),
    "mom": mothers_day_us,
    "mutter": mothers_day_us
}

# Note that the 'days' are not arrays; they're sets --> curly braces
EXCLUSION_MAP = {

    "weekdays":

        {'days': {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(MO, TU, WE, TH, FR))},

    "weekends":
        {'days': {'Saturday', 'Sunday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(SA, SU))},

    "mondays":
        {'days': {'Monday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=MO)},

    "tuesdays":
        {'days':{'Tuesday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=TU)},

    "wednesdays":
        {'days': {'Wednesday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=WE)},

    "thursdays":
        {'days': {'Thursday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=TH)},

    "fridays":
        {'days': {'Friday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=FR)},

    "saturdays":
        {'days': {'Saturday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=SA)},

    "sundays":
        {'days': {'Sunday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=SU)},

    "all except weekdays":
        {'days': {'Saturday', 'Sunday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(SA, SU))},

    "all except weekends":
        {'days': {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(MO, TU, WE, TH, FR))},

    "all except mondays":
        {'days': {'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(TU, WE, TH, FR, SA, SU))},

    "all except tuesdays":
        {'days': {'Monday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(MO, WE, TH, FR, SA, SU))},

    "all except wednesdays":
        {'days': {'Monday', 'Tuesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(MO, TU, TH, FR, SA, SU))},

    "all except thursdays":
        {'days': {'Monday', 'Tuesday', 'Wednesday', 'Friday', 'Saturday', 'Sunday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(MO, TU, WE, FR, SA, SU))},

    "all except fridays":
        {'days': {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(MO, TU, WE, TH, SA, SU))},

    "all except saturdays":
        {'days': {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(MO, TU, WE, TH, FR, SU))},

    "all except sundays":
        {'days': {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday'},
         'rule': lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(MO, TU, WE, TH, FR, SA))}
}
