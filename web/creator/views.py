from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from dateutil.relativedelta import relativedelta
from datetime import datetime
from creator.fotocalendar.creator import create_for_format, create_from_request, create_preview_from_request

from creator.fotocalendar.icsparser import get_events_from_ics


def index(request):
    template = loader.get_template('creator/start.html')
    return HttpResponse(template.render({"page": "start"}, request))


def options(request):
    calendar = create_for_format(request.GET.get('format', ''))
    first_month = datetime.now() + relativedelta(months=1)
    context = {
        "page": "options",
        "table_borders": calendar._table_border,
        "supports_events": calendar._supports_events,
        "center_month": False,
        "first_month": first_month.strftime("%Y-%m-01"),
        "table_background_transparency": "70"
    }
    template = loader.get_template('creator/options.html')
    return HttpResponse(template.render(context, request))


def month(request):
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

    context = {
        "page": "months",
        "format": format,
        "supports_events": calendar._supports_events,
        "months": months,
        "aspectRatio": calendar.get_image_aspect_ratio(),
        "background_color": request.POST.get('background_color'),
        "center_month": request.POST.get('center_month'),
        "table_border": request.POST.get('table_border'),
        "table_background_color": request.POST.get('table_background_color'),
        "table_background_tansparency": request.POST.get('table_background_tansparency'),
        "image_border": request.POST.get('image_border'),
        "image_border_color": request.POST.get('image_border_color'),
        "image_border_width": request.POST.get('image_border_width')
    }
    template = loader.get_template('creator/months.html')
    return HttpResponse(template.render(context, request))


def create(request):
    if request.method == 'POST':
        calendar = create_from_request(request)
        return HttpResponse(calendar.output(), content_type="application/pdf")
    else:
        return HttpResponseRedirect('/creator')


def preview(request):
    calendar = create_preview_from_request(request)
    return HttpResponse(calendar.output(), content_type="application/pdf")


def faq(request):
    template = loader.get_template('creator/faq.html')
    return HttpResponse(template.render({"page": "faq"}, request))


def impressum(request):
    template = loader.get_template('creator/impressum.html')
    return HttpResponse(template.render({"page": "impressum"}, request))
