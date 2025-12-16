from datetime import datetime
import orjson
import base64
from dataclasses import dataclass, field, InitVar, asdict, KW_ONLY
from typing import List, Any
import io
import lzma
from PIL import Image


@dataclass
class FontConfig:
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str = '#000000'
    size: int = 8
    family: str = ""

    @property
    def font_style(self):
        style = ''
        if self.bold:
            style += 'B'
        if self.italic:
            style += 'I'
        if self.underline:
            style += 'U'
        return style

    def update_from_request(self, request, prefix="", postfix=""):
        self.bold = request.POST.get(prefix + 'bold' + postfix, self.bold)
        self.italic = request.POST.get(prefix + 'italic' + postfix, self.italic)
        self.underline = request.POST.get(prefix + 'underline' + postfix, self.underline)
        if request.POST.get(prefix + 'color' + postfix, "") != "":
            self.color = request.POST.get(prefix + 'color' + postfix)
        self.size = request.POST.get(prefix + 'size' + postfix, self.size)
        self.family = request.POST.get(prefix + 'family' + postfix, self.family)


@dataclass
class FontsConfig:
    font_family: InitVar[str]
    _: KW_ONLY
    weekday: FontConfig = field(init=False)
    saturday: FontConfig = field(init=False)
    sunday: FontConfig = field(init=False)
    event: FontConfig = field(init=False)
    month: FontConfig = field(init=False)
    week: FontConfig = field(init=False)
    dayname: FontConfig = field(init=False)

    def __post_init__(self, font_family: str):
        self.weekday = FontConfig(size=15, family=font_family)
        self.saturday = FontConfig(size=15, family=font_family, bold=True)
        self.sunday = FontConfig(size=15, family=font_family, bold=True)
        self.event = FontConfig(size=8, family=font_family)
        self.month = FontConfig(size=20, family=font_family)
        self.week = FontConfig(size=8, family=font_family)
        self.dayname = FontConfig(size=8, family=font_family)

    def update_from_request(self, request, prefix="", postfix=""):
        self.weekday.update_from_request(request, prefix + "weekday_", postfix)
        self.saturday.update_from_request(request, prefix + "saturday_", postfix)
        self.sunday.update_from_request(request, prefix + "sunday_", postfix)
        self.event.update_from_request(request, prefix + "event_", postfix)
        self.month.update_from_request(request, prefix + "month_", postfix)
        self.dayname.update_from_request(request, prefix + "dayname_", postfix)


@dataclass
class Event:
    date: datetime
    text: str
    is_holiday: bool = True


@dataclass
class DayConfig:
    day: int
    day_of_week: int
    week: int
    events: List[Event] = field(default_factory=list)
    is_holiday: bool = False

    @property
    def is_saturday(self):
        return self.day_of_week == 6

    @property
    def is_sunday(self):
        return self.day_of_week == 7


@dataclass
class MonthConfig:
    image_aspect_ratio: str = '1.0'
    date: datetime = field(default_factory=datetime.now)
    font_family: InitVar[str] = ""
    _: KW_ONLY
    id: int = 0
    name: str = ''
    month_align: str = 'L'
    month_show_year: bool = True
    show_weeks: bool = True

    events: dict = field(default_factory=dict)
    event_separator: str = ' • '
    eventlist_align: str = 'C'

    table_border: bool = False
    table_background_color: str = '#ffffff'
    table_background_transparency: float = 0.7
    table_background_round_corners: bool = True
    table_background_corner_radius: int = 2

    background_type: str = 'N'
    background_color: str = '#ffffff'
    background_color_b: str = '#aaaaaa'

    image: bytes = None
    image_border: bool = False
    image_border_color: str = '#000000'
    image_border_width: int = 3
    image_x: Any = None
    image_y: Any = None
    image_width: Any = None
    image_height: Any = None

    fonts: FontsConfig = field(init=False)

    def __post_init__(self, font_family: str):
        self.fonts = FontsConfig(font_family)

    def set_image(self, var):
        if isinstance(var, Image.Image):
            img_byte_arr = io.BytesIO()
            var.save(img_byte_arr, format='jpeg')
            self.image = img_byte_arr.getvalue()
        else:
            self.image = var.read()

    def add_event(self, event=None, date: datetime = None, text: str = None, is_holiday: bool = False):
        if date and text:
            event = Event(date, text, is_holiday)
        key = event.date.day
        if key not in self.events:
            self.events[key] = []
        self.events[key].append(event)

    def events_for_date(self, date) -> Event:
        key = date.day if isinstance(date, datetime) else int(date)
        return self.events[key] if key in self.events else []

    def update_from_request(self, request, postfix: str = ""):
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
            self.table_background_transparency = float(request.POST.get('table_background_transparency' + postfix)) / 100.0
        self.image_border = request.POST.get('image_border' + postfix, self.image_border)
        if request.POST.get('image_border_color' + postfix, '') != '':
            self.image_border_color = request.POST.get('image_border_color' + postfix)
        self.image_border_width = request.POST.get('image_border_width' + postfix, self.image_border_width)
        self.fonts.update_from_request(request, "font_", postfix)
        if request.FILES.get('image' + postfix):
            self.set_image(request.FILES.get('image' + postfix))
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


@dataclass
class DefaultConfig(MonthConfig):
    _: KW_ONLY
    supports_events: bool = True
    supports_weeks: bool = True
    supports_fonts: bool = True
    supports_italic: bool = True


@dataclass
class CalendarConfig:
    format: str
    title: str = None
    months: List[MonthConfig] = field(default_factory=list)
    first_month: datetime = field(default_factory=datetime.now)

    def asdict(self):
        return asdict(self)

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

    def dump(self):
        json = self.to_json()
        content = lzma.compress(json)
        return content

    @classmethod
    def loads(cls, json):
        data = orjson.loads(json)
        return cls(**data)

    def to_json(self, include_images=False):
        return orjson.dumps(self, default=default, option=orjson.OPT_INDENT_2 + orjson.OPT_OMIT_MICROSECONDS)


def default(obj) -> str:
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
