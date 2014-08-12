from dateutil.rrule import DAILY, rrule, SA, SU, MO, TU, WE, TH, FR, YEARLY

DATE_EXCLUSION_RULES_MAP = {

    "weekends": {"exclude": (SA, SU)},
    "weekdays": {"exclude": (MO, TU, WE, TH, FR)}

}




