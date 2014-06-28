from datetime import datetime
from dateutil.easter import easter

__author__ = 'raymond'

# package for general utility stuff


def get_easter():
    current_date = datetime.today()
    this_easter = datetime.combine(easter(current_date.year), datetime.min.time())
    if current_date < this_easter:
        return this_easter
    else:
        # We've already had easter this year
        next_year = datetime(current_date.year + 1, 1, 1)
        return datetime.combine(easter(next_year.year), datetime.min.time())


def get_anniversary(date_object):
    current_date = datetime.today()
    this_anniversary = datetime(current_date.year, date_object.month, date_object.day)
    if current_date < this_anniversary:
        return this_anniversary
    else:
        # We've already had Crimbo this year
        return datetime(current_date.year + 1, date_object.month, date_object.day)