from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from creator.fotocalendar.creator import get_default_config_for_format, get_default_config_for_request, get_config_for_request, create_from_config, create_preview_from_request


def index(request):
    template = loader.get_template('creator/start.html')
    return HttpResponse(template.render({"page": "start"}, request))


def options(request):
    config = get_default_config_for_format(request.GET.get("format", 'L'))
    template = loader.get_template('creator/options.html')
    return HttpResponse(template.render(config.to_context(), request))


def month(request):
    config = get_default_config_for_request(request)
    template = loader.get_template('creator/months.html')
    return HttpResponse(template.render(config.to_context(), request))


def load(request):
    # Not yet implemented
    return HttpResponse(status=501)


def create(request):
    if request.method == 'POST':
        config = get_config_for_request(request)
        if request.POST.get('save_project', '0') == '1':
            return HttpResponse(str(config), content_type="application/json")
        else:
            print("Creating Calendar PDF")
            calendar = create_from_config(config)
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
