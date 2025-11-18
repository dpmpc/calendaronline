from fpdf import FPDF
from fpdf.drawing import color_from_hex_string
from fpdf.pattern import LinearGradient, RadialGradient
from calendar import monthrange
from datetime import datetime
from dateutil.relativedelta import relativedelta


class FotoCalendar:
    _dayNamesAbbrev = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    _dayNames = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    _monthNames = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    _month_align = 'L'

    _background_type = 'N'
    _background_color = "#ffffff"
    _background_color_b = "#aaaaaa"

    _table_border = True
    _table_background_color = "#ffffff"
    _table_background_tansparency = 0.7

    _image_border = False
    _image_border_width = 3
    _image_border_color = '#000000'

    _text_background_round_corners = True
    _text_background_corner_radius = 2

    _font_style_bold_weekday = False
    _font_style_italic_weekday = False
    _font_style_underline_weekday = False
    _font_color_weekday = '#000000'

    _font_style_bold_saturday = True
    _font_style_italic_saturday = False
    _font_style_underline_saturday = False
    _font_color_saturday = '#000000'

    _font_style_bold_sunday = True
    _font_style_italic_sunday = False
    _font_style_underline_sunday = False
    _font_color_sunday = '#000000'

    _font_style_bold_event = False
    _font_style_italic_event = False
    _font_style_underline_event = False
    _font_color_event = '#000000'

    _font_color_month = "#000000"

    _supports_events = False
    _supports_weeks = False
    _show_weeks = True
    _supports_fonts = True
    _supports_italic = True

    _font = 'Helveticat'
    _fonts = {
        'Sawasdee': {
            'R': 'files/font/TLWG/Sawasdee.ttf',
            'B': 'files/font/TLWG/Sawasdee-Bold.ttf',
            'I': 'files/font/TLWG/Sawasdee-Oblique.ttf',
            'BI': 'files/font/TLWG/Sawasdee-BoldOblique.ttf'
        },
        'BalsamiqSans': {
            'R': 'files/font/Balsamiq_Sans/BalsamiqSans-Regular.ttf',
            'B': 'files/font/Balsamiq_Sans/BalsamiqSans-Bold.ttf',
            'I': 'files/font/Balsamiq_Sans/BalsamiqSans-Italic.ttf',
            'BI': 'files/font/Balsamiq_Sans/BalsamiqSans-BoldItalic.ttf'
        },
        'Purisa': {
            'R': 'files/font/TLWG/Purisa.ttf',
            'B': 'files/font/TLWG/Purisa-Bold.ttf',
            'I': 'files/font/TLWG/Purisa-Oblique.ttf',
            'BI': 'files/font/TLWG/Purisa-BoldOblique.ttf'
        },
        'Tippa': {
            'R': 'files/font/Tippa/Tippa.ttf',
            'B': 'files/font/Tippa/Tippa.ttf',
            'I': 'files/font/Tippa/Tippa.ttf',
            'BI': 'files/font/Tippa/Tippa.ttf'
        },
        'MonsieurLaDoulaise': {
            'R': 'files/font/Monsieur_La_Doulaise/MonsieurLaDoulaise-Regular.ttf',
            'B': 'files/font/Monsieur_La_Doulaise/MonsieurLaDoulaise-Regular.ttf',
            'I': 'files/font/Monsieur_La_Doulaise/MonsieurLaDoulaise-Regular.ttf',
            'BI': 'files/font/Monsieur_La_Doulaise/MonsieurLaDoulaise-Regular.ttf'
        },
        'Pacifico': {
            'R': 'files/font/Pacifico/Pacifico-Regular.ttf',
            'B': 'files/font/Pacifico/Pacifico-Regular.ttf',
            'I': 'files/font/Pacifico/Pacifico-Regular.ttf',
            'BI': 'files/font/Pacifico/Pacifico-Regular.ttf'
        },
        'NotoSansDisplay': {
            'R': 'files/font/NotoSansDisplay/NotoSansDisplay_Condensed-Regular.ttf',
            'B': 'files/font/NotoSansDisplay/NotoSansDisplay_Condensed-Bold.ttf',
            'I': 'files/font/NotoSansDisplay/NotoSansDisplay_Condensed-Italic.ttf',
            'BI': 'files/font/NotoSansDisplay/NotoSansDisplay_Condensed-BoldItalic.ttf'
        }
    }

    @property
    def fpdf(self):
        if self._fpdf is None:
            self._fpdf = FPDF(orientation=self.orientation, format="A4")
            self._fpdf.set_display_mode(zoom="fullpage")
            self._fpdf.set_auto_page_break(False)
            self._fpdf.set_producer("k51.de - Simple create foto calendars as PDF")
            self._fpdf.set_margin(self.margin)
            self._fpdf.set_top_margin(self.tmargin)
            self._add_font(self._font)
            self._fpdf.set_font(self._font)

        return self._fpdf

    def __init__(self, orientation, margin, image_with, image_height):
        self._fpdf = None

        self.orientation = orientation
        self.margin = margin
        self.tmargin = 20
        self.image_with = image_with
        self.image_height = image_height

        self.eventlist_align = 'C'
        self.eventlist = {}

    def addTitle(self, title='', image=None):
        pdf = self.fpdf
        if title != '':
            pdf.set_subject(title)
            pdf.add_page()
            pdf.set_font(style='B', size=100)
            pdf.cell(txt=title)
            if image:
                pdf.image(image, h=pdf.eph, w=pdf.epw, x=0, y=0)

    def add_month(self, config):
        pdf = self.fpdf
        self._set_options_from_config(config)

        if self._background_type == 'S' and self._background_color is not None:
            pdf.set_page_background(self._background_color)
        else:
            pdf.set_page_background(None)

        pdf.add_page()

        self._createBackgroundGradient()
        pdf.start_section(self.get_month_name_with_year(config['date']), 0)
        if 'image' in config:
            self._addImage(config['image'])
        self._addText(config['date'], self._generateMonthMatrix(config['date']))

    def _createBackgroundGradient(self):
        pdf = self.fpdf
        colors = [self._background_color, self._background_color_b]

        if self._background_type == 'V':
            grad = LinearGradient(pdf, 0, 0, pdf.w, 0, colors)
        elif self._background_type == 'H':
            grad = LinearGradient(pdf, 0, 0, 0, pdf.h, colors)
        elif self._background_type == 'D':
            grad = LinearGradient(pdf, 0, 0, pdf.w, pdf.h, colors)
        elif self._background_type == 'R':
            center_x = pdf.w / 2
            center_y = pdf.h / 2
            if pdf.w > pdf.h:
                r = pdf.w / 2
            else:
                r = pdf.h / 2
            grad = RadialGradient(pdf, center_x, center_y, 0, center_x, center_y, r, colors, self._background_color_b)
        else:
            grad = None

        if grad is not None:
            with pdf.use_pattern(grad):
                # Draw a rectangle that will be filled with the gradient
                pdf.rect(x=0, y=0, w=pdf.w, h=pdf.h, style="FD")

    def _addText(date, matrix):
        pass

    def _addImage(self, image):
        pdf = self.fpdf
        x = self.margin
        y = self.tmargin
        h = self.image_height
        w = self.image_with
        if self._image_border:
            pdf.set_line_width(self._image_border_width)
            pdf.set_draw_color(self._image_border_color)
            pdf.rect(x + self._image_border_width / 2, y + self._image_border_width / 2, w - self._image_border_width, h - self._image_border_width)
            pdf.set_draw_color(0, 0, 0)
            x = self.margin + self._image_border_width
            y = self.tmargin + self._image_border_width
            h = self.image_height - self._image_border_width * 2
            w = self.image_with - self._image_border_width * 2

        if image:
            pdf.image(image, h=h, w=w, x=x, y=y)

    def set_background_color(self, background_color):
        if background_color is not None:
            # Use colors as a fpdf's add_page is (not yet) capabe of handling DeviceGray colors (which is returned when r==g==b)
            self._background_color = color_from_hex_string(background_color).colors255

    def set_background_color_b(self, background_color):
        if background_color is not None:
            # Use colors as a fpdf's add_page is (not yet) capabe of handling DeviceGray colors (which is returned when r==g==b)
            self._background_color_b = color_from_hex_string(background_color).colors255

    def set_background_type(self, background_type):
        self._background_type = background_type

    def set_table_border(self, table_border):
        self._table_border = True if table_border is not None and table_border else False

    def set_table_background_color(self, table_background_color):
        if table_background_color is not None:
            self._table_background_color = color_from_hex_string(table_background_color)

    def set_table_background_transparency(self, table_background_transparency):
        if table_background_transparency is not None:
            self._table_background_tansparency = float(table_background_transparency) / 100

    def set_image_border(self, image_border):
        if image_border is not None:
            self._image_border = 1 if image_border else 0

    def set_image_border_color(self, image_border_color):
        if image_border_color is not None:
            self._image_border_color = color_from_hex_string(image_border_color)

    def set_image_border_widht(self, image_border_width):
        if image_border_width is not None:
            self._image_border_width = float(image_border_width) / 10

    def set_image_shadow(self, shadow):
        self.shadow = True if shadow else False

    def is_center_month(self):
        return self._month_align == 'C'

    def set_center_month(self, center_month):
        if center_month is not None:
            self._month_align = 'C' if center_month else 'L'

    def set_show_weeks(self, show_weeks):
        self._show_weeks = True if show_weeks else False

    def set_events(self, eventlist):
        self.eventlist = eventlist

    def _add_font(self, family):
        if family in self._fonts:
            pdf = self.fpdf
            font = self._fonts[family]
            pdf.add_font(fname=font['R'], family=family)
            pdf.add_font(fname=font['B'], style="B", family=family)
            pdf.add_font(fname=font['I'], style="I", family=family)
            pdf.add_font(fname=font['BI'], style="BI", family=family)
            pdf.set_text_shaping(True)

    def _generateMonthMatrix(self, date):
        matrix = {}
        max_days = monthrange(date.year, date.month)[1]
        for day in range(1, max_days + 1):
            date = date.replace(day=day)
            dayId = date.timetuple().tm_yday
            matrix[dayId] = self._createDay(date)
        return matrix

    def _createDay(self, date):
        dayOfWeek = date.isoweekday()
        isSaturday = dayOfWeek == 6
        isSunday = dayOfWeek == 7
        events = self._get_event_texts(date)
        isHoliday = self._get_is_holiday(date)
        if isHoliday:
            color = color_from_hex_string(self._font_color_event)
            fontStyle = self._toFontStyle(self._font_style_bold_event, self._font_style_italic_event, self._font_style_underline_event)
        elif isSaturday:
            color = color_from_hex_string(self._font_color_saturday)
            fontStyle = self._toFontStyle(self._font_style_bold_saturday, self._font_style_italic_saturday, self._font_style_underline_saturday)
        elif isSunday:
            color = color_from_hex_string(self._font_color_sunday)
            fontStyle = self._toFontStyle(self._font_style_bold_sunday, self._font_style_italic_sunday, self._font_style_underline_sunday)
        else:
            color = color_from_hex_string(self._font_color_weekday)
            fontStyle = self._toFontStyle(self._font_style_bold_weekday, self._font_style_italic_weekday, self._font_style_underline_weekday)

        return {
            "day": str(date.day),
            "dayOfWeek": dayOfWeek,
            "week": date.isocalendar().week,
            "color": color,
            "fontStyle": fontStyle,
            "events": events,
            "isSunday": isSunday,
            "isSaturday": isSaturday,
            "isHoliday": isHoliday
        }

    def get_month_name(self, date):
        return self._monthNames[date.month - 1]

    def get_month_name_with_year(self, date):
        return self.get_month_name(date) + " " + self._year(date)

    def _get_events(self, date):
        datekey = date.strftime("%Y-%m-%d")
        if datekey in self.eventlist:
            return self.eventlist[datekey]
        else:
            return []

    def _get_event_texts(self, date):
        event_text_list = []
        for evt in self._get_events(date):
            event_text_list.append(evt["text"])

        return event_text_list

    def _get_is_holiday(self, date):
        for evt in self._get_events(date):
            if evt['isHoliday']:
                return True
        return False

    def _year(self, date):
        return str(date.year)

    def _dayName(self, dayOfWeek):
        return self._dayNames[dayOfWeek - 1]

    def _dayNameAbbrev(self, dayOfWeek):
        return self._dayNamesAbbrev[dayOfWeek - 1]

    def _font_style_for_day(self, day):
        if day["isSaturday"]:
            return self._toFontStyle(self._font_style_bold_saturday, self._font_style_italic_saturday, self._font_style_underline_saturday)
        elif day["isSunday"]:
            return self._toFontStyle(self._font_style_bold_sunday, self._font_style_italic_sunday, self._font_style_underline_sunday)
        elif day["isHoliday"]:
            return self._toFontStyle(self._font_style_bold_event, self._font_style_italic_event, self._font_style_underline_event)

        return self._toFontStyle(self._font_style_bold_weekday, self._font_style_italic_weekday, self._font_style_underline_weekday)

    def _toFontStyle(self, bold, italic, underline):
        style = ''
        if bold:
            style += 'B'
        if italic:
            style += 'I'
        if underline:
            style += 'U'
        return style

    def _hex_color_to_tuple(self, color):
        if color.startswith('#'):
            color = color.lstrip('#')
        return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

    def _set_fill_color(self, color):
        pdf = self.fpdf
        pdf.set_fill_color(color[0], color[1], color[2])

    def _set_text_color(self, color):
        pdf = self.fpdf
        pdf.set_text_color(color[0], color[1], color[2])

    def _set_draw_color(self, color):
        pdf = self.fpdf
        pdf.set_draw_color(color[0], color[1], color[2])

    def get_image_aspect_ratio(self):
        return "{:.2f}".format(self.image_with / self.image_height)

    def output(self):
        return bytes(self.fpdf.output())

    def create_default_config(self, first_month=None):
        if first_month is None:
            first_month = datetime.now() + relativedelta(months=1)

        return {
            "page": "options",
            "table_border": self._table_border,
            "supports_events": self._supports_events,
            "supports_weeks": self._supports_weeks,
            "supports_fonts": self._supports_fonts,
            "supports_italic": self._supports_italic,
            "center_month": self.is_center_month(),
            "show_weeks": self._show_weeks,
            "months": [],
            "aspectRatio": self.get_image_aspect_ratio(),
            "first_month": first_month.strftime("%Y-%m-01"),
            "table_background_transparency": self._table_background_tansparency * 100,
            "background_type": self._background_type,
            "background_color": self._background_color,
            "background_color_b": self._background_color_b,
            "table_background_color": self._table_background_color,
            "image_border": self._image_border,
            "image_border_color": self._image_border_color,
            "image_border_width": self._image_border_width,
            "font_weekday_bold": self._font_style_bold_weekday,
            "font_weekday_italic": self._font_style_italic_weekday,
            "font_weekday_underline": self._font_style_underline_weekday,
            "font_weekday_color": self._font_color_weekday,
            "font_saturday_bold": self._font_style_bold_saturday,
            "font_saturday_italic": self._font_style_italic_saturday,
            "font_saturday_underline": self._font_style_underline_saturday,
            "font_saturday_color": self._font_color_saturday,
            "font_sunday_bold": self._font_style_bold_sunday,
            "font_sunday_italic": self._font_style_italic_sunday,
            "font_sunday_underline": self._font_style_underline_sunday,
            "font_sunday_color": self._font_color_sunday,
            "font_event_bold": self._font_style_bold_event,
            "font_event_italic": self._font_style_underline_event,
            "font_event_underline": self._font_style_underline_event,
            "font_event_color": self._font_color_event
        }

    def _set_options_from_config(self, config):
        print(config)
        self.set_background_type(config['background_type'])
        self.set_background_color(config['background_color'])
        self.set_background_color_b(config['background_color_b'])
        self.set_center_month(config['center_month'])
        self.set_show_weeks(config['show_weeks'])

        self.set_table_border(config['table_border'])
        self.set_table_background_color(config['table_background_color'])
        self.set_table_background_transparency(config['table_background_transparency'])

        self.set_image_border(config['image_border'])
        self.set_image_border_color(config['image_border_color'])
        self.set_image_border_widht(config['image_border_width'])

        self._font_style_bold_weekday = config['font_weekday_bold']
        self._font_style_italic_weekday = config['font_weekday_italic']
        self._font_style_underline_weekday = config['font_weekday_underline']
        self._font_color_weekday = config['font_weekday_color']
        self._font_style_bold_saturday = config['font_saturday_bold']
        self._font_style_italic_saturday = config['font_saturday_italic']
        self._font_style_underline_saturday = config['font_saturday_underline']
        self._font_color_saturday = config['font_saturday_color']
        self._font_style_bold_sunday = config['font_sunday_bold']
        self._font_style_italic_sunday = config['font_sunday_italic']
        self._font_style_underline_sunday = config['font_sunday_underline']
        self._font_color_sunday = config['font_sunday_color']
        self._font_style_bold_event = config['font_event_bold']
        self._font_style_underline_event = config['font_event_italic']
        self._font_style_underline_event = config['font_event_underline']
        self._font_color_event = config['font_event_color']
