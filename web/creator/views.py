from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from creator.fotocalendar.bo.config import CalendarConfig
from creator.fotocalendar.creator import get_default_config_for_format, get_default_config_for_request, get_config_for_request, create_from_config, create_preview_from_request
from pdf2image import convert_from_bytes
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError, PopplerNotInstalledError


def index(request):
    template = loader.get_template('creator/start.html')
    return HttpResponse(template.render({"page": "start"}, request))


def options(request):
    config = get_default_config_for_format(request.GET.get("format", 'L'))
    template = loader.get_template('creator/options.html')
    return HttpResponse(template.render(config.asdict(), request))


def month(request):
    config = get_default_config_for_request(request)
    template = loader.get_template('creator/months.html')
    return HttpResponse(template.render(config.asdict(), request))


def load(request):
    content = request.FILES.get('file')
    config = CalendarConfig.loads(content.read())
    
    template = loader.get_template('creator/months.html')
    return HttpResponse(template.render(config.asdict(), request))


def create(request):
    if request.method == 'POST':
        config = get_config_for_request(request)
        if request.POST.get('save_project', '0') == '1':
            content = config.dump()
            return HttpResponse(content, content_type="application/octet-stream")
        else:
            calendar = create_from_config(config)
            return HttpResponse(calendar.output(), content_type="application/pdf")
    else:
        return HttpResponseRedirect('/creator')


def preview(request):
    calendar = create_preview_from_request(request)
    pdf_output = calendar.output()
    if request.GET.get('pdf', '0') == '1':
        return HttpResponse(pdf_output, content_type="application/pdf")
    else:
        try:
            pages = convert_from_bytes(pdf_output, dpi=150, first_page=1, last_page=1)
            img = pages[0]
            response = HttpResponse(content_type="image/png")
            img.save(response, "PNG")
            return response
        except (PDFInfoNotInstalledError, PopplerNotInstalledError, PDFPageCountError, PDFSyntaxError, IndexError):
            # PDF conversion failed - fall back to PDF output
            return HttpResponse(pdf_output, content_type="application/pdf")


def faq(request):
    template = loader.get_template('creator/faq.html')
    return HttpResponse(template.render({"page": "faq"}, request))


def impressum(request):
    template = loader.get_template('creator/impressum.html')
    return HttpResponse(template.render({"page": "impressum"}, request))
