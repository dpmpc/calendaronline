from creator.fotocalendar.templates.landscape import LandscapeFotoCalendar
from creator.fotocalendar.templates.portrait import PortraitFotoCalendar
from creator.fotocalendar.templates.design1 import Design1FotoCalendar
from creator.fotocalendar.icsparser import get_events_from_post, get_events_from_ics
from PIL import Image
from dateutil.relativedelta import relativedelta
from datetime import datetime


def create_for_format(format):
    if format == 'L':
        print("Creating LandscapeFotoCalendar for format", format)
        return LandscapeFotoCalendar(False)
    elif format == '1':
        print("Creating Design1FotoCalendar for format", format)
        return Design1FotoCalendar()
    elif format == 'LF':
        print("Creating LandscapeFotoCalendar (fullscreen) for format", format)
        return LandscapeFotoCalendar(True)
    elif format == 'PF':
        print("Creating PortraitFotoCalendar (fullscreen) for format", format)
        return PortraitFotoCalendar(True)
    elif format == 'PW':
        print("Creating PortraitFotoCalendar (fullwidth) for format", format)
        return PortraitFotoCalendar(False, True)
    else:
        print("Creating PortraitFotoCalendar for format", format)
        return PortraitFotoCalendar()


def create_options_context_for_request(request):
    calendar = create_for_format(request.GET.get('format', ''))
    first_month = datetime.now() + relativedelta(months=1)
    return {
        "page": "options",
        "table_border": calendar._table_border,
        "supports_events": calendar._supports_events,
        "supports_weeks": calendar._supports_weeks,
        "center_month": calendar.is_center_month(),
        "show_weeks": calendar._show_weeks,
        "first_month": first_month.strftime("%Y-%m-01"),
        "table_background_transparency": "70",
        "background_color": "#ffffff",
        "table_background_color": "#ffffff",
        "image_border": False,
        "image_border_color": "#000000",
        "image_border_width": 10
    }


def create_months_context_for_request(request):
    format = request.POST.get('format', '')
    calendar = create_for_format(format)

    start = request.POST.get('start', '2025-01-01')
    firstMonth = datetime.strptime(start, '%Y-%m-%d')
    lastMonth = firstMonth + relativedelta(months=13)

    appointments = get_events_from_ics(request.POST.get('ics_url', ''), firstMonth, lastMonth)

    months = []
    for month in range(12):
        appointments_of_month = []
        datekey = firstMonth.strftime("%Y%m")
        if datekey in appointments:
            appointments_of_month = appointments[datekey]
        months.append({
            "id": month,
            "date": firstMonth.strftime("%Y-%m-01"),
            "name": calendar.get_month_name(firstMonth),
            "appointments": appointments_of_month
        })
        firstMonth += relativedelta(months=1)

    return {
        "page": "months",
        "format": format,
        "supports_events": calendar._supports_events,
        "supports_weeks": calendar._supports_weeks,
        "months": months,
        "aspectRatio": calendar.get_image_aspect_ratio(),
        "background_color": request.POST.get('background_color'),
        "center_month": request.POST.get('center_month'),
        "show_weeks": request.POST.get('show_weeks'),
        "table_border": request.POST.get('table_border'),
        "table_background_color": request.POST.get('table_background_color'),
        "table_background_transparency": request.POST.get('table_background_transparency'),
        "image_border": request.POST.get('image_border'),
        "image_border_color": request.POST.get('image_border_color'),
        "image_border_width": request.POST.get('image_border_width')
    }


def create_from_request(request):
    calendar = create_for_format(request.POST.get('format'))
    calendar.addTitle()

    eventlist = get_events_from_post(request.POST.getlist('event-date'), request.POST.getlist('event-text'), [])
    calendar.set_events(eventlist)

    lenght = int(request.POST.get('lenght'))
    for i in range(lenght):
        id = '_' + str(i)
        month = datetime.strptime(request.POST.get('date' + id), '%Y-%m-%d')
        _set_options_from_request(calendar, request, id)
        if request.FILES.get('image' + id):
            calendar.addMonth(date=month, image=request.FILES.get('image' + id))

    return calendar


def _set_options_from_request(calendar, request, postfix=''):
    calendar.set_background_color(request.POST.get('background_color' + postfix))
    calendar.set_center_month(request.POST.get('center_month' + postfix))
    calendar.set_show_weeks(request.POST.get('show_weeks' + postfix))

    calendar.set_table_border(request.POST.get('table_border' + postfix))
    calendar.set_table_background_color(request.POST.get('table_background_color' + postfix))
    calendar.set_table_background_tansparency(request.POST.get('table_background_tansparency' + postfix))

    calendar.set_image_border(request.POST.get('image_border' + postfix))
    calendar.set_image_border_color(request.POST.get('image_border_color' + postfix))
    calendar.set_image_border_widht(request.POST.get('image_border_width' + postfix))


def create_preview_from_request(request):
    if request.method == 'POST':
        format = request.POST.get('format', 'P')
        month = datetime.strptime(request.POST.get('start'), '%Y-%m-%d')
        calendar = create_for_format(format)
        _set_options_from_request(calendar, request)
    else:
        format = request.GET.get('format', 'P')
        month = datetime.now()
        calendar = create_for_format(format)

    image = Image.open('files/images/example.jpg')
    if format == 'P':
        image = image.crop((352, 34, 1343, 999))
    elif format == '1':
        image = image.crop((389, 24, 1596, 1031))
    elif format == 'LF':
        image = image.crop((307, 335, 1703, 1120))
    elif format == 'PF':
        image = image.crop((350, 115, 1200, 1320))
    elif format == 'PW':
        image = image.crop((312, 0, 1303, 1060))
    elif format == 'L':
        image = image.crop((304, 290, 1700, 1000))
    calendar.addMonth(month, image)
    return calendar
