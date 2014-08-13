from dateutil.rrule import SA, SU, MO, TU, WE, TH, FR

DATE_EXCLUSION_RULES_MAP = {

    "weekends": {"exclude": (SA, SU)},
    "weekdays": {"exclude": (MO, TU, WE, TH, FR)},
    "mondays": {"exclude": MO},
    "tuesdays": {"exclude": TU},
    "wednesdays": {"exclude": WE},
    "thursdays": {"exclude": TH},
    "fridays": {"exclude": FR},
    "saturdays": {"exclude": SA},
    "sundays": {"exclude": SU}

}




