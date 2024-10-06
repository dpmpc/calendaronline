from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from creator.fotocalendar.creator import create_from_request, create_preview_from_request, create_options_context_for_request, create_months_context_for_request


def index(request):
    template = loader.get_template('creator/start.html')
    return HttpResponse(template.render({"page": "start"}, request))


def options(request):
    context = create_options_context_for_request(request)
    template = loader.get_template('creator/options.html')
    return HttpResponse(template.render(context, request))


def month(request):
    context = create_months_context_for_request(request)
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
