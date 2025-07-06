from creator.fotocalendar.templates.landscape import LandscapeFotoCalendar
from creator.fotocalendar.templates.portrait import PortraitFotoCalendar
from creator.fotocalendar.templates.design1 import Design1FotoCalendar
from creator.fotocalendar.templates.vintage import VintageFotoCalendar
from creator.fotocalendar.templates.landscape_modern import LandscapeModernFotoCalendar

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
    elif format == 'V':
        print("Creating HandmadeFotoCalendar for format", format)
        return VintageFotoCalendar()
    elif format == 'LM':
        print("Creating LandscapeModernFotoCalendar for format", format)
        return LandscapeModernFotoCalendar()
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
        "supports_fonts": calendar._supports_fonts,
        "supports_italic": calendar._supports_italic,
        "center_month": calendar.is_center_month(),
        "show_weeks": calendar._show_weeks,
        "first_month": first_month.strftime("%Y-%m-01"),
        "table_background_transparency": "70",
        "background_type": calendar._background_type,
        "background_color": "#ffffff",
        "background_color_b": "#aaaaaa",
        "table_background_color": "#ffffff",
        "image_border": False,
        "image_border_color": "#000000",
        "image_border_width": 10,
        "font_weekday_bold": calendar._font_style_bold_weekday,
        "font_weekday_italic": calendar._font_style_italic_weekday,
        "font_weekday_underline": calendar._font_style_underline_weekday,
        "font_weekday_color": calendar._font_color_weekday,
        "font_saturday_bold": calendar._font_style_bold_saturday,
        "font_saturday_italic": calendar._font_style_italic_saturday,
        "font_saturday_underline": calendar._font_style_underline_saturday,
        "font_saturday_color": calendar._font_color_saturday,
        "font_sunday_bold": calendar._font_style_bold_sunday,
        "font_sunday_italic": calendar._font_style_italic_sunday,
        "font_sunday_underline": calendar._font_style_underline_sunday,
        "font_sunday_color": calendar._font_color_sunday,
        "font_event_bold": calendar._font_style_bold_event,
        "font_event_italic": calendar._font_style_underline_event,
        "font_event_underline": calendar._font_style_underline_event,
        "font_event_color": calendar._font_color_event
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
        "supports_fonts": calendar._supports_fonts,
        "months": months,
        "aspectRatio": calendar.get_image_aspect_ratio(),
        "background_type": request.POST.get('background_type'),
        "background_color": request.POST.get('background_color'),
        "background_color_b": request.POST.get('background_color_b'),
        "center_month": request.POST.get('center_month'),
        "show_weeks": request.POST.get('show_weeks'),
        "table_border": request.POST.get('table_border'),
        "table_background_color": request.POST.get('table_background_color'),
        "table_background_transparency": request.POST.get('table_background_transparency'),
        "image_border": request.POST.get('image_border'),
        "image_border_color": request.POST.get('image_border_color'),
        "image_border_width": request.POST.get('image_border_width'),
        "font_weekday_bold": request.POST.get('font_weekday_bold'),
        "font_weekday_italic": request.POST.get('font_weekday_italic'),
        "font_weekday_underline": request.POST.get('font_weekday_underline'),
        "font_weekday_color": request.POST.get('font_weekday_color'),
        "font_saturday_bold": request.POST.get('font_saturday_bold'),
        "font_saturday_italic": request.POST.get('font_saturday_italic'),
        "font_saturday_underline": request.POST.get('font_saturday_underline'),
        "font_saturday_color": request.POST.get('font_saturday_color'),
        "font_sunday_bold": request.POST.get('font_sunday_bold'),
        "font_sunday_italic": request.POST.get('font_sunday_italic'),
        "font_sunday_underline": request.POST.get('font_sunday_underline'),
        "font_sunday_color": request.POST.get('font_sunday_color'),
        "font_event_bold": request.POST.get('font_event_bold'),
        "font_event_italic": request.POST.get('font_event_italic'),
        "font_event_underline": request.POST.get('font_event_underline'),
        "font_event_color": request.POST.get('font_event_color')
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
    calendar.set_background_type(request.POST.get('background_type' + postfix))
    calendar.set_background_color(request.POST.get('background_color' + postfix))
    calendar.set_background_color_b(request.POST.get('background_color_b' + postfix))
    calendar.set_center_month(request.POST.get('center_month' + postfix))
    calendar.set_show_weeks(request.POST.get('show_weeks' + postfix))

    calendar.set_table_border(request.POST.get('table_border' + postfix))
    calendar.set_table_background_color(request.POST.get('table_background_color' + postfix))
    calendar.set_table_background_tansparency(request.POST.get('table_background_tansparency' + postfix))

    calendar.set_image_border(request.POST.get('image_border' + postfix))
    calendar.set_image_border_color(request.POST.get('image_border_color' + postfix))
    calendar.set_image_border_widht(request.POST.get('image_border_width' + postfix))

    calendar._font_style_bold_weekday = True if request.POST.get('font_weekday_bold' + postfix) else False
    calendar._font_style_italic_weekday = True if request.POST.get('font_weekday_italic' + postfix) else False
    calendar._font_style_underline_weekday = True if request.POST.get('font_weekday_underline' + postfix) else False
    calendar._font_color_weekday = request.POST.get('font_weekday_color' + postfix, calendar._font_color_weekday)
    calendar._font_style_bold_saturday = True if request.POST.get('font_saturday_bold' + postfix) else False
    calendar._font_style_italic_saturday = True if request.POST.get('font_saturday_italic' + postfix) else False
    calendar._font_style_underline_saturday = True if request.POST.get('font_saturday_underline' + postfix) else False
    calendar._font_color_saturday = request.POST.get('font_saturday_color' + postfix, calendar._font_color_saturday)
    calendar._font_style_bold_sunday = True if request.POST.get('font_sunday_bold' + postfix) else False
    calendar._font_style_italic_sunday = True if request.POST.get('font_sunday_italic' + postfix) else False
    calendar._font_style_underline_sunday = True if request.POST.get('font_sunday_underline' + postfix) else False
    calendar._font_color_sunday = request.POST.get('font_sunday_color' + postfix, calendar._font_color_sunday)
    calendar._font_style_bold_event = True if request.POST.get('font_event_bold' + postfix) else False
    calendar._font_style_underline_event = True if request.POST.get('font_event_italic' + postfix) else False
    calendar._font_style_underline_event = True if request.POST.get('font_event_underline' + postfix) else False
    calendar._font_color_event = request.POST.get('font_event_color' + postfix, calendar._font_color_event)


def create_preview_from_request(request):
    if request.method == 'POST':
        format = request.POST.get('format', 'P')
        month = datetime.strptime(request.POST.get('start'), '%Y-%m-%d')
        calendar = create_for_format(format)
        _set_options_from_request(calendar, request)
    else:
        format = request.GET.get('format', 'P')
        month = datetime.now()
        monthOverride = int(request.GET.get('month', '0'))
        month = month + relativedelta(months=monthOverride)
        calendar = create_for_format(format)

    image = Image.open('files/images/example.jpg')
    if format == 'P':
        x = 352
        y = 34
        w = 1000
    if format == 'V':
        x = 320
        y = 350
        w = 1000
    elif format == '1':
        x = 389
        y = 24
        w = 1200
    elif format == 'LF':
        x = 307
        y = 335
        w = 1400
    elif format == 'PF':
        x = 350
        y = 115
        w = 850
    elif format == 'PW':
        x = 312
        y = 0
        w = 1000
    elif format == 'L' or format == 'LM':
        x = 304
        y = 290
        w = 1400

    h = w / float(calendar.get_image_aspect_ratio())
    image = image.crop((x, y, x + w, y + h))
    calendar.addMonth(month, image)
    return calendar
