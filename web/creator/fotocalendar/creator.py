from creator.fotocalendar.fotocalendar import FotoCalendar
from creator.fotocalendar.templates.landscape import LandscapeFotoCalendar
from creator.fotocalendar.templates.portrait import PortraitFotoCalendar
from creator.fotocalendar.templates.design1 import Design1FotoCalendar
from creator.fotocalendar.templates.vintage import VintageFotoCalendar
from creator.fotocalendar.templates.design2026 import Design2026FotoCalendar
from creator.fotocalendar.templates.landscape_modern import LandscapeModernFotoCalendar
from creator.fotocalendar.bo.config import CalendarConfig
from creator.fotocalendar.icsparser import get_events_from_ics
from PIL import Image
from dateutil.relativedelta import relativedelta
from datetime import datetime
from copy import deepcopy


def create_for_format(format: str) -> FotoCalendar:
    if format == "L":
        print("Creating LandscapeFotoCalendar for format", format)
        return LandscapeFotoCalendar(False)
    elif format == "1":
        print("Creating Design1FotoCalendar for format", format)
        return Design1FotoCalendar()
    elif format == "LF":
        print("Creating LandscapeFotoCalendar (fullscreen) for format", format)
        return LandscapeFotoCalendar(True)
    elif format == "PF":
        print("Creating PortraitFotoCalendar (fullscreen) for format", format)
        return PortraitFotoCalendar(True)
    elif format == "PW":
        print("Creating PortraitFotoCalendar (fullwidth) for format", format)
        return PortraitFotoCalendar(False, True)
    elif format == "V":
        print("Creating HandmadeFotoCalendar for format", format)
        return VintageFotoCalendar()
    elif format == "LM":
        print("Creating LandscapeModernFotoCalendar for format", format)
        return LandscapeModernFotoCalendar()
    elif format == "26":
        print("Creating Design2026FotoCalendar for format", format)
        return Design2026FotoCalendar()
    else:
        print("Creating PortraitFotoCalendar for format", format)
        return PortraitFotoCalendar()


def get_default_config_for_format(format: str) -> CalendarConfig:
    first_month = datetime.now()
    if first_month.month > 10:
        first_month = first_month + relativedelta(years=1, month=1, day=1)
    else:
        first_month = first_month + relativedelta(months=1, day=1)
    calendar = create_for_format(format)

    config = CalendarConfig(format, first_month=first_month)
    config.months.append(calendar.get_default_config(first_month))
    return config


def get_default_config_for_request(
    request, number_of_months: int = 12
) -> CalendarConfig:
    config = get_default_config_for_format(request.POST.get("format", "P"))
    defaut_config = config.months[0]
    defaut_config.update_from_request(request)
    config.months = []

    start = request.POST.get("start")
    firstMonth = datetime.strptime(start, "%Y-%m-%d")
    lastMonth = firstMonth + relativedelta(months=number_of_months + 1, day=31)

    events = get_events_from_ics(request.POST.get("ics_url", ""), firstMonth, lastMonth)

    for month in range(number_of_months):
        month_config = deepcopy(defaut_config)
        month_config.id = month
        month_config.date = firstMonth
        month_config.name = FotoCalendar._monthNames[firstMonth.month - 1]
        datekey = firstMonth.strftime("%Y%m")
        if datekey in events:
            month_config.events = events[datekey]
        config.months.append(month_config)
        firstMonth += relativedelta(months=1, day=1)

    return config


def get_config_for_request(request) -> CalendarConfig:
    config = get_default_config_for_format(request.POST.get("format", "P"))
    defaut_config = config.months[0]
    config.months = []
    number_of_months = int(request.POST.get("lenght", 1))
    ids = request.POST.get("ids")
    ids_list = ids.split(",") if ids else range(number_of_months)

    for month in ids_list:
        if month != "":
            month_config = deepcopy(defaut_config)
            month_config.update_from_request(request, "_" + str(month))
            config.months.append(month_config)

    return config


def create_calendar_for_request(request) -> FotoCalendar:
    format = request.POST.get("format", "P")
    calendar = create_for_format(format)
    config = CalendarConfig.create_for_request(request, calendar)
    return create_from_config(config)


def create_from_config(config: CalendarConfig) -> FotoCalendar:
    calendar = create_for_format(config.format)

    for month in config.months:
        calendar.add_month(month)

    return calendar


def create_preview_from_request(request) -> FotoCalendar:

    if request.method == "POST":
        config = get_default_config_for_request(request, 1)
        format = config.format
    else:
        format = request.GET.get("format", "P")
        config = get_default_config_for_format(format)

    if not config.months[0].image:
        image = Image.open("files/images/example.jpg")
        if format == "P":
            x = 352
            y = 34
            w = 1000
        if format == "V":
            x = 320
            y = 350
            w = 1000
        elif format == "1":
            x = 389
            y = 24
            w = 1200
        elif format == "LF":
            x = 307
            y = 335
            w = 1400
        elif format == "PF":
            x = 350
            y = 115
            w = 850
        elif format == "PW":
            x = 312
            y = 0
            w = 1000
        elif format == "L" or format == "LM":
            x = 304
            y = 290
            w = 1400
        elif format == "26":
            x = 352
            y = 180
            w = 1000

        h = w / float(config.months[0].image_aspect_ratio)
        config.months[0].set_image(image.crop((x, y, x + w, y + h)))

    return create_from_config(config)
