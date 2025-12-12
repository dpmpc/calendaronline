from fpdf.drawing import color_from_hex_string
from datetime import datetime
import json
import base64


def color_to_hex(color):
    return "#" + "".join(hex(int(val))[2:].rjust(2, "0") for val in color.colors255)


class CalendarConfig:
    def __init__(self, format: str, title=None, months=None, first_month=None):
        self.format = format
        self.title = title
        self.first_month = first_month if first_month else datetime.now()
        self.months = months if months else []

    def to_context(self):
        return {
            'format': self.format,
            'title': self.title,
            'first_month': self.first_month.strftime("%Y-%m-01"),
            'months': [item.to_context() for item in self.months]
        }

    @classmethod  # decorator
    def create_from_request(cls, request, calendar): 
        config = cls(request.POST.get('format'))
        lenght = int(request.POST.get('lenght'))
        for i in range(lenght):
            id = '_' + str(i)
            month = calendar.get_default_config()
            month.update_from_request(request, id)
            config.months.append(month)

        return config

    def __str__(self):
        return json.dumps(self.to_context(), indent=4)


class MonthConfig:
    def __init__(self, image_aspect_ratio=1, date=None, font_family=""):
        self.id = 0
        self.date = datetime.now() if date is None else date
        self.name = ""

        self.month_align = 'L'
        self.month_show_year = True

        # self.first_month = first_month.strftime("%Y-%m-01")
        self.show_weeks = True
        self.image_aspect_ratio = image_aspect_ratio

        self.events = {}
        self.event_separator = ' • '
        self.eventlist_align = 'C'

        self.table_border = False
        self.table_background_color = "#ffffff"
        self.table_background_transparency = 0.7
        self.table_background_round_corners = True
        self.table_background_corner_radius = 2

        self.background_type = "N"
        self.background_color = "#ffffff"
        self.background_color_b = "#aaaaaa"

        self.image = None
        self.image_border = False
        self.image_border_color = '#000000'
        self.image_border_width = 3
        self.image_x = None
        self.image_y = None
        self.image_width = None
        self.image_height = None

        self.fonts = FontsConfig(font_family)

    @property
    def background_color(self):
        return self.__background_color

    @background_color.setter
    def background_color(self, var):
        if var is not None:
            self.__background_color = color_from_hex_string(var)

    @property
    def background_color_b(self):
        return self.__background_color_b

    @background_color_b.setter
    def background_color_b(self, var):
        if var is not None:
            self.__background_color_b = color_from_hex_string(var)

    @property
    def table_background_color(self):
        return self.__table_background_color

    @table_background_color.setter
    def table_background_color(self, var):
        if var is not None:
            self.__table_background_color = color_from_hex_string(var)

    @property
    def image_border_color(self):
        return self.__image_border_color

    @image_border_color.setter
    def image_border_color(self, var):
        if var is not None:
            self.__image_border_color = color_from_hex_string(var)

    def add_event(self, event=None, date=None, text=None, is_holiday=False):
        if date and text:
            event = Event(date, text, is_holiday)
        key = event.date.day
        if key not in self.events:
            self.events[key] = []
        self.events[key].append(event)

    def events_for_date(self, date):
        key = date.day if isinstance(date, datetime) else int(date)
        return self.events[key] if key in self.events else []

    def to_context(self, include_images=False):
        events = []
        for key in self.events:
            events = events + self.events[key]
        if self.image and include_images:
            image = base64.b64encode(self.image.read()).decode('utf-8')
        else:
            image = None
        return {
            'id': self.id,
            'date': self.date.strftime("%Y-%m-01"),
            'name': self.name,
            'center_month': True if self.month_align == 'C' else False,
            'month_show_year': self.month_show_year,
            'table_border': self.table_border,
            'show_weeks': self.show_weeks,
            'image_aspect_ratio': self.image_aspect_ratio,

            'event_separator': self.event_separator,
            'eventlist_align': self.eventlist_align,

            'table_background_color': color_to_hex(self.table_background_color),
            'table_background_transparency': int(self.table_background_transparency * 255),
            'table_background_round_corners': self.table_background_round_corners,
            'table_background_corner_radius': self.table_background_corner_radius,

            'background_type': self.background_type,
            'background_color': color_to_hex(self.__background_color),
            'background_color_b': color_to_hex(self.__background_color_b),

            'image_border': self.image_border,
            'image_border_color': color_to_hex(self.image_border_color),
            'image_border_width': self.image_border_width,
            'image_x': self.image_x,
            'image_y': self.image_y,
            'image_width': self.image_width,
            'image_height': self.image_height,
            'image': image,

            'fonts': self.fonts.to_context(),
            'events': [event.to_context() for event in events]
        }

    def update_from_request(self, request, postfix=""):
        if request.POST.get('id' + postfix, '') != '':
            self.id = int(request.POST.get('id' + postfix))
        if request.POST.get('date' + postfix, '') != '':
            self.date = datetime.strptime(request.POST.get('date' + postfix), '%Y-%m-%d')
        self.name = request.POST.get('name' + postfix, '')
        self.background_type = request.POST.get('background_type' + postfix, self.background_type)
        if request.POST.get('background_color' + postfix, '') != '':
            self.background_color = request.POST.get('background_color' + postfix) 
        if request.POST.get('background_color_b' + postfix, '') != '':
            self.background_color_b = request.POST.get('background_color_b' + postfix)
        if request.POST.get('center_month' + postfix, False):
            self.month_align = 'C'
        self.show_weeks = request.POST.get('show_weeks' + postfix, self.show_weeks)
        self.table_border = request.POST.get('table_border' + postfix, self.table_border)
        if request.POST.get('table_background_color' + postfix, '') != '':
            self.table_background_color = request.POST.get('table_background_color' + postfix)
        if request.POST.get('table_background_transparency' + postfix, '') != '':
            self.table_background_transparency = float(request.POST.get('table_background_transparency' + postfix)) / 255
        self.image_border = request.POST.get('image_border' + postfix, self.image_border)
        if request.POST.get('image_border_color' + postfix, '') != '':
            self.image_border_color = request.POST.get('image_border_color' + postfix)
        self.image_border_width = request.POST.get('image_border_width' + postfix, self.image_border_width)
        self.fonts.update_from_request(request, "font_", postfix)
        if request.FILES.get('image' + postfix):
            self.image = request.FILES.get('image' + postfix)
        self.image_x = request.POST.get('image_x' + postfix)
        self.image_y = request.POST.get('image_y' + postfix)
        self.image_width = request.POST.get('image_width' + postfix)
        self.image_height = request.POST.get('image_height' + postfix)

        self.events = {}
        date_list = request.POST.getlist('event-date' + postfix)
        text_list = request.POST.getlist('event-text' + postfix)
        for i in range(len(date_list)):
            date = datetime.strptime(date_list[i], '%Y-%m-%d')
            self.add_event(date=date, text=text_list[i], is_holiday=False)

    def __str__(self):
        return json.dumps(self.to_context(), indent=4)


class DefaultConfig(MonthConfig):
    def __init__(self, image_aspect_ratio, date=None, font_family=""):
        super().__init__(image_aspect_ratio, date, font_family)
        self.supports_events = True
        self.supports_weeks = True
        self.supports_fonts = True
        self.supports_italic = True

    def to_context(self):
        result = super().to_context()
        result['supports_events'] = self.supports_events
        result['supports_weeks'] = self.supports_weeks
        result['supports_fonts'] = self.supports_fonts
        result['supports_italic'] = self.supports_italic
        return result

    def __str__(self):
        return json.dumps(self.to_context(), indent=4)


class FontsConfig:
    def __init__(self, font_family=""):
        self.weekday = FontConfig(size=15, family=font_family)
        self.saturday = FontConfig(size=15, family=font_family, bold=True)
        self.sunday = FontConfig(size=15, family=font_family, bold=True)
        self.event = FontConfig(size=8, family=font_family)
        self.month = FontConfig(size=20, family=font_family)
        self.week = FontConfig(size=8, family=font_family)
        self.dayname = FontConfig(size=8, family=font_family)

    def to_context(self):
        return {
            'weekday': self.weekday.to_context(),
            'saturday': self.saturday.to_context(),
            'sunday': self.sunday.to_context(),
            'event': self.event.to_context(),
            'month': self.month.to_context(),
            'week': self.week.to_context(),
            'dayname': self.dayname.to_context()
        }

    def update_from_request(self, request, prefix="", postfix=""):
        self.weekday.update_from_request(request, prefix + "weekday_", postfix)
        self.saturday.update_from_request(request, prefix + "saturday_", postfix)
        self.sunday.update_from_request(request, prefix + "sunday_", postfix)
        self.event.update_from_request(request, prefix + "event_", postfix)
        self.month.update_from_request(request, prefix + "month_", postfix)
        self.dayname.update_from_request(request, prefix + "dayname_", postfix)

    def __str__(self):
        return json.dumps(self.to_context(), indent=4)


class FontConfig:
    def __init__(self, bold=False, italic=False, underline=False, color='#000000', size=8, family=""):
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.color = color
        self.size = size
        self.family = family

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, var):
        if var is not None:
            self.__color = color_from_hex_string(var)

    def to_context(self):
        return {
            'bold': self.bold,
            'italic': self.italic,
            'underline': self.underline,
            'color': color_to_hex(self.color),
            'size': self.size,
            'family': self.family
        }

    def update_from_request(self, request, prefix="", postfix=""):
        self.bold = request.POST.get(prefix + 'bold' + postfix, self.bold)
        self.italic = request.POST.get(prefix + 'italic' + postfix, self.italic)
        self.underline = request.POST.get(prefix + 'underline' + postfix, self.underline)
        if request.POST.get(prefix + 'color' + postfix, "") != "":
            self.color = request.POST.get(prefix + 'color' + postfix)
        self.size = request.POST.get(prefix + 'size' + postfix, self.size)
        self.family = request.POST.get(prefix + 'family' + postfix, self.family)

    def __str__(self):
        return json.dumps(self.to_context(), indent=4)


class DayConfig:
    def __init__(self, day, day_of_week, week, events=[], is_holiday=False):
        self.day = day
        self.day_of_week = day_of_week
        self.week = week
        self.events = events
        self.is_saturday = day_of_week == 6
        self.is_sunday = day_of_week == 7
        self.is_holiday = is_holiday

    def to_context(self):
        return {
            'day': self.day,
            'day_of_week': self.day_of_week,
            'week': self.week,
            'events': self.events,
            'is_sunday': self.is_sunday,
            'is_saturday': self.is_saturday,
            'is_holiday': self.is_holiday,
        }

    def __str__(self):
        return json.dumps(self.to_context(), indent=4)


class Event:

    def __init__(self, date: datetime, text, is_holiday=True):
        self.date = date
        self.text = text
        self.is_holiday = is_holiday

    def to_context(self):
        return {
            "date": str(self.date),
            "text": self.text,
            "is_holiday": self.is_holiday
        }