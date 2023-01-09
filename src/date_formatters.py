from bisect import bisect

DAYS_OF_WEEK = {
    1: "MON",
    2: "TUE",
    3: "WED",
    4: "THU",
    5: "FRI",
    6: "SAT",
    7: "SUN"
}

# The functions must all take a datetime object and they must all
# return a string


def week_number(date_time):
    return "{week_number}".format(week_number=date_time.strftime("%V"))


def week_day(date_time):
    return DAYS_OF_WEEK[date_time.isoweekday()]


def week_day_in_isoformat(date_time):
    return str(date_time.isoweekday())


def iso_format(date_time):
    return date_time.isoformat()


# Just for a laugh we'll add a function to find the star sign
# for a given date
def zodiac_sign(date_time):
    signs = [(1, 20, "Capricorn"), (2, 18, "Aquarius"), (3, 20, "Pisces"), (4, 20, "Aries"),
             (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 22, "Cancer"), (8, 23, "Leo"),
             (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
             (12, 31, "Capricorn")]
    return signs[bisect(signs, (date_time.month, date_time.day))][2]


# Regular expression matched as a list of optionals
# will always match the first one they find in the list,
# so if your function names start with the same characters,
# then always put the longer ones at the top of the list
# so they are matched first. In this case we have put
# 'wdi' in front of 'wd'. If you don't then the wrong
# function might get matched by mistake.
DATE_FORMATTERS_MAP = {

    "wdi": week_day_in_isoformat,
    "wn": week_number,
    "wd": week_day,
    "!": week_number,
    "iso": iso_format,
    "sign": zodiac_sign
}


