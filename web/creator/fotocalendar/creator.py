from creator.fotocalendar.templates.landscape import LandscapeFotoCalendar
from creator.fotocalendar.templates.portrait import PortraitFotoCalendar
from creator.fotocalendar.templates.design1 import Design1FotoCalendar
from creator.fotocalendar.templates.vintage import VintageFotoCalendar
from creator.fotocalendar.templates.design2026 import Design2026FotoCalendar

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
    elif format == '26':
        print("Creating Design2026FotoCalendar for format", format)
        return Design2026FotoCalendar()
    else:
        print("Creating PortraitFotoCalendar for format", format)
        return PortraitFotoCalendar()


def create_options_context_for_request(request):
    calendar = create_for_format(request.GET.get('format', ''))
    return calendar.create_default_config()


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


def _empty_config(format):
    return {
        'format': format,
        'title': None,
        'events': {},
        'months': []
    }


def _get_config_from_request(request):
    config = _empty_config(request.POST.get('format'))
    config['events'] = get_events_from_post(request.POST.getlist('event-date'), request.POST.getlist('event-text'), [])
    lenght = int(request.POST.get('lenght'))
    for i in range(lenght):
        id = '_' + str(i)
        if request.FILES.get('image' + id):
            config['months'].append(_get_month_config_from_request(request, id))

    return config


def create_from_request(request):
    config = _get_config_from_request(request)
    return create_from_config(config)


def create_from_config(config):
    calendar = create_for_format(config['format'])
    # if 'title' in config:
    #    calendar.addTitle(config['title'])

    if 'events' in config:
        calendar.set_events(config['events'])

    if 'months' in config:
        for month in config['months']:
            calendar.add_month(month)

    return calendar


def _get_month_config_from_request(request, postfix='', date=None):
    return {
        'date': datetime.strptime(request.POST.get('date' + postfix), '%Y-%m-%d') if date is None else date,
        'image': request.FILES.get('image' + postfix, None),
        'background_type': request.POST.get('background_type' + postfix),
        'background_color': request.POST.get('background_color' + postfix),
        'background_color_b': request.POST.get('background_color_b' + postfix),
        'center_month': request.POST.get('center_month' + postfix),
        'show_weeks': request.POST.get('show_weeks' + postfix),
        'table_border': request.POST.get('table_border' + postfix),
        'table_background_color': request.POST.get('table_background_color' + postfix),
        'table_background_transparency': request.POST.get('table_background_transparency' + postfix),
        'image_border': request.POST.get('image_border' + postfix),
        'image_border_color': request.POST.get('image_border_color' + postfix),
        'image_border_width': request.POST.get('image_border_width' + postfix),
        'font_weekday_bold': True if request.POST.get('font_weekday_bold' + postfix) else False,
        'font_weekday_italic': True if request.POST.get('font_weekday_italic' + postfix) else False,
        'font_weekday_underline': True if request.POST.get('font_weekday_underline' + postfix) else False,
        'font_weekday_color': request.POST.get('font_weekday_color' + postfix),
        'font_saturday_bold': True if request.POST.get('font_saturday_bold' + postfix) else False,
        'font_saturday_italic': True if request.POST.get('font_saturday_italic' + postfix) else False,
        'font_saturday_underline': True if request.POST.get('font_saturday_underline' + postfix) else False,
        'font_saturday_color': request.POST.get('font_saturday_color' + postfix),
        'font_sunday_bold': True if request.POST.get('font_sunday_bold' + postfix) else False,
        'font_sunday_italic': True if request.POST.get('font_sunday_italic' + postfix) else False,
        'font_sunday_underline': True if request.POST.get('font_sunday_underline' + postfix) else False,
        'font_sunday_color': request.POST.get('font_sunday_color' + postfix),
        'font_event_bold': True if request.POST.get('font_event_bold' + postfix) else False,
        'font_event_italic': True if request.POST.get('font_event_italic' + postfix) else False,
        'font_event_underline': True if request.POST.get('font_event_underline' + postfix) else False,
        'font_event_color': request.POST.get('font_event_color' + postfix)
    }


def create_preview_from_request(request):

    if request.method == 'POST':
        format = request.POST.get('format', 'P')
        calendar = create_for_format(format)
        month = datetime.strptime(request.POST.get('start'), '%Y-%m-%d')
        month_config = _get_month_config_from_request(request, date=month)
    else:
        format = request.GET.get('format', 'P')
        calendar = create_for_format(format)

        month = datetime.now()
        monthOverride = int(request.GET.get('month', '0'))
        month = month + relativedelta(months=monthOverride)
        month_config = calendar.create_default_config()
        month_config['date'] = month

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
    elif format == '26':
        x = 352
        y = 180
        w = 1000

    h = w / float(calendar.get_image_aspect_ratio())
    month_config['image'] = image.crop((x, y, x + w, y + h))

    config = _empty_config(format)
    config['months'].append(month_config)
    return create_from_config(config)
