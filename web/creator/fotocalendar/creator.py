from creator.fotocalendar.templates.landscape import LandscapeFotoCalendar
from creator.fotocalendar.templates.portrait import PortraitFotoCalendar
from creator.fotocalendar.templates.design1 import Design1FotoCalendar
from PIL import Image
from datetime import datetime


def create_for_format(format):
    if format == 'L':
        print("Creating LandscapeFotoCalendar for format", format)
        return LandscapeFotoCalendar()
    elif format == '1':
        print("Creating Design1FotoCalendar for format", format)
        return Design1FotoCalendar()
    else:
        print("Creating PortraitFotoCalendar for format", format)
        return PortraitFotoCalendar()


def create_from_request(request):
    calendar = create_for_format(request.POST.get('format', ''))
    calendar.set_center_month(request.POST.get('center_month', '') == '1')
    calendar.set_table_border(request.POST.get('table_border', '') == '1')
    calendar.set_ics_url(request.POST.get('ics_url', ''))

    calendar.addTitle()

    lenght = int(request.POST.get('lenght'))
    for i in range(lenght):
        id = '_' + str(i)
        month = datetime.strptime(request.POST.get('date' + id), '%Y-%m-%d')
        background = request.POST.get('background_color' + id, '#ffffff')
        calendar.set_page_background(background)
        image = None
        if request.FILES.get('image' + id):
            image = Image.open(request.FILES.get('image' + id))
            left = float(request.POST.get('crop_x' + id, '0'))
            upper = float(request.POST.get('crop_y' + id, '0'))
            right = left + float(request.POST.get('crop_width' + id, '0'))
            lower = upper + float(request.POST.get('crop_height' + id, '0'))
            box = (int(left), int(upper), int(right), int(lower))
            print("Cropping image to ", box)
            image = image.crop(box)
        calendar.addMonth(month, image)

    return calendar


def create_preview(format):
    calendar = create_for_format(format)
    calendar.set_center_month(False)
    calendar.set_table_border(True)
    month = datetime.now()
    image = Image.open('files/images/example.jpg')
    if format == 'P':
        image = image.crop((352, 9, 1343, 1107))
    elif format == '1':
        image = image.crop((389, 24, 1596, 1031))
    elif format == 'L':
        image = image.crop((367, 255, 1763, 1040))
    calendar.addMonth(month, image)
    return calendar
