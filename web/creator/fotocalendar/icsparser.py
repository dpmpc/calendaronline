from icalevents.icalevents import events


def get_events_from_ics(ics_url, start, end):
    print("Setting ics_url: ", ics_url)
    eventlist = {}
    if ics_url != "":
        evts = events(url=ics_url, start=start, end=end)
        for evt in evts:
            datekey = evt.start.strftime("%Y%m")
            if datekey not in eventlist:
                eventlist[datekey] = []
            eventlist[datekey].append(_create_event(evt.start.strftime("%Y-%m-%d"), evt.summary, False))

    return eventlist


def _create_event(date, text, isHoliday):
    return {
        "date": date,
        "text": text,
        "isHoliday": isHoliday
    }


def get_events_from_post(date_list, text_list, is_holiday_list):
    eventlist = {}
    print(date_list, is_holiday_list)
    for i in range(len(date_list)):
        datekey = date_list[i]
        if datekey not in eventlist:
            eventlist[datekey] = []
        eventlist[datekey].append(_create_event(date_list[i], text_list[i], False))

    return eventlist
