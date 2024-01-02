from creator.fotocalendar.templates.landscape import LandscapeFotoCalendar
from creator.fotocalendar.templates.portrait import PortraitFotoCalendar
from creator.fotocalendar.templates.design1 import Design1FotoCalendar
from PIL import Image, ImageOps

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
    else:
        print("Creating PortraitFotoCalendar for format", format)
        return PortraitFotoCalendar()


def create_from_request(request):
    calendar = create_for_format(request.POST.get('format'))
    calendar.set_ics_url(request.POST.get('ics_url', ''))

    calendar.addTitle()

    lenght = int(request.POST.get('lenght'))
    for i in range(lenght):
        id = '_' + str(i)
        month = datetime.strptime(request.POST.get('date' + id), '%Y-%m-%d')
        calendar.set_options_from_request(request, id)
        image = None
        if request.FILES.get('image' + id):
            image = Image.open(request.FILES.get('image' + id))
            image = ImageOps.exif_transpose(image)

            x = int(float(request.POST.get('crop_x' + id, '0')))
            y = int(float(request.POST.get('crop_y' + id, '0')))
            w = int(float(request.POST.get('crop_width' + id, '0')))
            h = int(float(request.POST.get('crop_height' + id, '0')))
            box = (x, y, x + w, y + h)

            print("Cropping image to ", box)
            image = image.crop(box)

            calendar.addMonth(date=month, image=image)

    return calendar


def create_preview_from_request(request):
    if request.method == 'POST':
        format = request.POST.get('format', 'P')
        month = datetime.strptime(request.POST.get('start'), '%Y-%m-%d')
        calendar = create_for_format(format)
        calendar.set_options_from_request(request)
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
    elif format == 'L':
        image = image.crop((304, 290, 1700, 1000))
    calendar.addMonth(month, image)
    return calendar
