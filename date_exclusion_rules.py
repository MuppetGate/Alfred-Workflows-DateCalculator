from dateutil.rrule import DAILY, rrule, SA, SU, MO, TU, WE, TH, FR

DATE_EXCLUSION_RULES_MAP = {

    "weekends": rrule(freq=DAILY, byweekday=(SA, SU)),
    "weekdays": rrule(freq=DAILY, byweekday=(MO, TU, WE, TH, FR))

}
