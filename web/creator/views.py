from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from dateutil.relativedelta import relativedelta
from datetime import datetime
from creator.fotocalendar.creator import create_for_format, create_from_request, create_preview


def index(request):
    template = loader.get_template('creator/start.html')
    return HttpResponse(template.render({"page": "start"}, request))


def options(request):
    template = loader.get_template('creator/options.html')
    return HttpResponse(template.render({"page": "options"}, request))


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
            # "name": calendar.get_month_name_with_year(firstMonth)
        })
        firstMonth += relativedelta(months=1)
    aspectRatio = calendar.get_image_aspect_ratio()

    template = loader.get_template('creator/months.html')
    return HttpResponse(template.render({"page": "months", "months": months, "aspectRatio": aspectRatio}, request))


def create(request):
    if request.method == 'POST':
        # print(request.POST)
        calendar = create_from_request(request)
        return HttpResponse(calendar.output(), content_type="application/pdf")
    else:
        return HttpResponseRedirect('/creator')


def preview(request):
    calendar = create_preview(request.GET.get('format', 'L'))
    return HttpResponse(calendar.output(), content_type="application/pdf")


def faq(request):
    template = loader.get_template('creator/faq.html')
    return HttpResponse(template.render({"page": "faq"}, request))


def impressum(request):
    template = loader.get_template('creator/impressum.html')
    return HttpResponse(template.render({"page": "impressum"}, request))
