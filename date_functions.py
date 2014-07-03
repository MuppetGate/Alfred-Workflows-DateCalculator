DAYS_OF_WEEK = {
    1: "MON",
    2: "TUE",
    3: "WED",
    4: "THU",
    5: "FRI",
    6: "SAT",
    7: "SUN"
}


def week_number(date_time):
    return "{week_number}".format(week_number=date_time.strftime("%V"))


def week_day(date_time):
    return DAYS_OF_WEEK[date_time.isoweekday()]


def week_day_in_isoformat(date_time):
    return str(date_time.isoweekday())

# Regular expression matched as a list of optionals
# will always match the first one they find in the list,
# so if your function names start with the same characters,
# then always put the longer ones at the top of the list
# so they are matched first. In this case we have put
# 'wdi' in front of 'wd'. If you don't then the wrong
# function might get matched by mistake.
DATE_FUNCTION_MAP = {

    "wdi": week_day_in_isoformat,
    "wn": week_number,
    "wd": week_day,
    "!": week_number,

}