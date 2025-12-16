from icalevents.icalevents import events
from creator.fotocalendar.bo.config import Event


def get_events_from_ics(ics_url, start, end):
    print("Setting ics_url: ", ics_url)
    eventlist = {}
    if ics_url != "":
        evts = events(url=ics_url, start=start, end=end)
        for evt in evts:
            datekey = evt.start.strftime("%Y%m")
            if datekey not in eventlist:
                eventlist[datekey] = []
            eventlist[datekey].append(Event(evt.start.strftime, evt.summary, False))

    return eventlist
