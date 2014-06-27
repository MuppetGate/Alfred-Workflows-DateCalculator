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


def get_christmas():
    current_date = datetime.today()
    this_christmas = datetime(current_date.year, 12, 25)
    if current_date < this_christmas:
        return this_christmas
    else:
        # We've already had Crimbo this year
        return datetime(current_date.year + 1, 12, 25)