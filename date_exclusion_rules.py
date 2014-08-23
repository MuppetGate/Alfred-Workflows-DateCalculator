from dateutil.rrule import SA, SU, MO, TU, WE, TH, FR, DAILY, rrule

DATE_EXCLUSION_RULES_MAP = {

    "weekends": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(SA, SU)),
    "weekdays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(MO, TU, WE, TH, FR)),
    "mondays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=MO),
    "tuesdays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=TU),
    "wednesdays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=WE),
    "thursdays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=TH),
    "fridays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=FR),
    "saturdays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=SA),
    "sundays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=SU),

    "all except weekends": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end,
                                                    byweekday=(MO, TU, WE, TH, FR)),

    "all except weekdays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end, byweekday=(SA, SU)),

    "all except mondays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end,
                                                   byweekday=(TU, WE, TH, FR, SA, SU)),

    "all except tuesdays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end,
                                                    byweekday=(MO, WE, TH, FR, SA, SU)),

    "all except wednesdays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end,
                                                      byweekday=(MO, TU, TH, FR, SA, SU)),

    "all except thursdays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end,
                                                     byweekday=(MO, TU, WE, FR, SA, SU)),

    "all except fridays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end,
                                                   byweekday=(MO, TU, WE, TH, SA, SU)),

    "all except saturdays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end,
                                                     byweekday=(MO, TU, WE, TH, FR, SU)),

    "all except sundays": lambda start, end: rrule(freq=DAILY, dtstart=start, until=end,
                                                   byweekday=(MO, TU, WE, TH, FR, SA))
}





