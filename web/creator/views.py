from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from dateutil.relativedelta import relativedelta
from datetime import datetime
from creator.fotocalendar.creator import create_for_format, create_from_request, create_preview_from_request


def index(request):
    template = loader.get_template('creator/start.html')
    return HttpResponse(template.render({"page": "start"}, request))


def options(request):
    calendar = create_for_format(request.GET.get('format', ''))
    first_month = datetime.now() + relativedelta(months=1)
    context = {
        "page": "options",
        "table_borders": calendar._table_border,
        "center_month": False,
        "first_month": first_month.strftime("%Y-%m-01"),
        "table_background_transparency": "70"
    }
    template = loader.get_template('creator/options.html')
    return HttpResponse(template.render(context, request))


def month(request):
    calendar = create_for_format(request.POST.get('format', ''))

    start = request.POST.get('start', '1970-01-01')
    firstMonth = datetime.strptime(start, '%Y-%m-%d')
    months = []
    for month in range(12):
        months.append({
            "id": month,
            "date": firstMonth.strftime("%Y-%m-01"),
            "name": calendar.get_month_name(firstMonth)
        })
        firstMonth += relativedelta(months=1)
    aspectRatio = calendar.get_image_aspect_ratio()

    template = loader.get_template('creator/months.html')
    return HttpResponse(template.render({"page": "months", "months": months, "aspectRatio": aspectRatio}, request))


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
