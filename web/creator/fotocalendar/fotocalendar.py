from fpdf import FPDF
from fpdf.pattern import LinearGradient, RadialGradient
from calendar import monthrange
from creator.fotocalendar.bo.config import DefaultConfig, MonthConfig, FontConfig, DayConfig


class FotoCalendar:
    _dayNamesAbbrev = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    _dayNames = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    _monthNames = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

    _font = 'Helvetica'
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

    def addTitle(self, title='', image=None):
        pdf = self.fpdf
        if title != '':
            pdf.set_subject(title)
            pdf.add_page()
            pdf.set_font(style='B', size=100)
            pdf.cell(txt=title)
            if image:
                pdf.image(image, h=pdf.eph, w=pdf.epw, x=0, y=0)

    def add_month(self, config: MonthConfig):
        self._add_page(config)
        self._add_image(config)
        self._add_text(config, self._generate_month_matrix(config))

    def get_default_config(self, date=None) -> DefaultConfig:
        return DefaultConfig(self.get_image_aspect_ratio(), date, self._font)

    def _add_table_background(self, config, x, y, w, h):
        pdf = self.fpdf
        with pdf.local_context(fill_opacity=config.table_background_transparency, stroke_opacity=0, fill_color=config.table_background_color):
            pdf.rect(x, y, w, h, round_corners=config.table_background_round_corners, corner_radius=config.table_background_corner_radius, style="F")

    def _add_page(self, config): 
        pdf = self.fpdf
        if config.background_type == 'S' and config.background_color is not None:
            pdf.set_page_background(config.background_color)
        else:
            pdf.set_page_background(None)

        pdf.add_page()

        self._create_background_gradient(config)
        pdf.start_section(self.get_month_name_with_year(config.date), 0)

    def _create_background_gradient(self, config):
        pdf = self.fpdf
        colors = [config.background_color, config.background_color_b]

        if config.background_type == 'V':
            grad = LinearGradient(0, 0, pdf.w, 0, colors)
        elif config.background_type == 'H':
            grad = LinearGradient(0, 0, 0, pdf.h, colors)
        elif config.background_type == 'D':
            grad = LinearGradient(0, 0, pdf.w, pdf.h, colors)
        elif config.background_type == 'R':
            center_x = pdf.w / 2
            center_y = pdf.h / 2
            if pdf.w > pdf.h:
                r = pdf.w / 2
            else:
                r = pdf.h / 2
            grad = RadialGradient(center_x, center_y, 0, center_x, center_y, r, colors, config.background_color_b)
        else:
            grad = None

        if grad is not None:
            with pdf.use_pattern(grad):
                # Draw a rectangle that will be filled with the gradient
                pdf.rect(x=0, y=0, w=pdf.w, h=pdf.h, style="FD")

    def _add_text(self, config, matrix):
        pass

    def _add_month_name(self, config):
        self._set_font(config.fonts.month)
        text = self.get_month_name_with_year(config.date) if config.month_show_year else self.get_month_name(config.date)
        self.fpdf.cell(txt=text, w=self.fpdf.epw, align=config.month_align, new_x="LMARGIN", new_y="NEXT")

    def _add_image(self, config):
        if config.image is not None:
            pdf = self.fpdf
            x = self.margin
            y = self.tmargin
            h = self.image_height
            w = self.image_with
            if config.image_border:
                x = self.margin + config.image_border_width
                y = self.tmargin + config.image_border_width
                h = self.image_height - config.image_border_width * 2
                w = self.image_with - config.image_border_width * 2
                with pdf.local_context(set_line_width=config.image_border_width, draw_color=config.image_border_color):
                    pdf.rect(x + config.image_border_width / 2, y + config.image_border_width / 2, w - config.image_border_width, h - config.image_border_width)
            pdf.image(config.image, h=h, w=w, x=x, y=y)

    def _add_font(self, family):
        if family in self._fonts:
            pdf = self.fpdf
            font = self._fonts[family]
            pdf.add_font(fname=font['R'], family=family)
            pdf.add_font(fname=font['B'], style="B", family=family)
            pdf.add_font(fname=font['I'], style="I", family=family)
            pdf.add_font(fname=font['BI'], style="BI", family=family)
            pdf.set_text_shaping(True)

    def _generate_month_matrix(self, config):
        matrix = {}
        date = config.date
        max_days = monthrange(date.year, date.month)[1]
        for day in range(1, max_days + 1):
            date = date.replace(day=day)
            dayId = date.timetuple().tm_yday
            matrix[dayId] = self._create_day(date, config)
        return matrix

    def _create_day(self, date, config) -> DayConfig:
        day = str(date.day)
        day_of_week = date.isoweekday()
        week = date.isocalendar().week
        events = self._get_event_texts(date, config)
        is_holiday = self._get_is_holiday(date, config)

        return DayConfig(day, day_of_week, week, events, is_holiday)

    def get_month_name(self, date):
        return self._monthNames[date.month - 1]

    def get_month_name_with_year(self, date):
        return self.get_month_name(date) + " " + self._year(date)

    def _get_event_texts(self, date, config):
        event_text_list = []
        for evt in config.events_for_date(date):
            event_text_list.append(evt.text)

        return event_text_list

    def _get_is_holiday(self, date, config):
        for evt in config.events_for_date(date):
            if evt.is_holiday:
                return True
        return False

    def _year(self, date):
        return str(date.year)

    def _dayName(self, dayOfWeek):
        return self._dayNames[dayOfWeek - 1]

    def _dayNameAbbrev(self, dayOfWeek):
        return self._dayNamesAbbrev[dayOfWeek - 1]

    def _set_font(self, config: FontConfig):
        style = self._to_font_style(config)
        self.fpdf.set_font(style=style, size=config.size, family=config.family)
        self.fpdf.set_text_color(config.color)

    def _set_font_for_day(self, day: DayConfig, config: MonthConfig):
        if day.is_saturday:
            self._set_font(config.fonts.saturday)
        elif day.is_sunday:
            self._set_font(config.fonts.sunday)
        elif day.is_holiday:
            self._set_font(config.fonts.events)
        else:
            self._set_font(config.fonts.weekday)

    def _to_font_style(self, config: FontConfig):
        style = ''
        if config.bold:
            style += 'B'
        if config.italic:
            style += 'I'
        if config.underline:
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