from fpdf import FPDF
from fpdf.drawing import color_from_hex_string
from calendar import monthrange
from icalevents.icalevents import events
from datetime import date


class FotoCalendar:
    _dayNamesAbbrev = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    _dayNames = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    _monthNames = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    _month_align = 'L'

    _background_color = None

    _table_border = True
    _table_background_color = [255, 255, 255]
    _table_background_tansparency = 0.7

    _image_border = False
    _image_border_width = 3
    _image_border_color = [0, 0, 0]

    _text_background_round_corners = True
    _text_background_corner_radius = 2

    def __init__(self, orientation, margin, image_with, image_height):
        self.margin = margin
        self.tmargin = 20
        self.image_with = image_with
        self.image_height = image_height

        self.eventlist_align = 'C'
        self.eventlist = {}

        pdf = FPDF(orientation=orientation, format="A4")
        pdf.set_display_mode(zoom="fullpage")
        pdf.set_auto_page_break(False)
        pdf.set_font('Helvetica')
        pdf.set_producer("k51.de - Simple create foto calendars as PDF")
        pdf.set_margin(self.margin)
        pdf.set_top_margin(self.tmargin)

        self.fpdf = pdf

    def addTitle(self, title='', image=None):
        pdf = self.fpdf
        if title != '':
            pdf.set_subject(title)
            pdf.add_page()
            pdf.set_font(style='B', size=100)
            pdf.cell(txt=title)
            if image:
                pdf.image(image, h=pdf.eph, w=pdf.epw, x=0, y=0)

    def addMonth(self, date, image=None):
        pdf = self.fpdf

        if self._background_color is not None:
            pdf.set_page_background(self._background_color)

        pdf.add_page()
        if self._image_border:
            print("Add border with witdth ", self._image_border_width, " and color ", self._image_border_color)
            pdf.set_line_width(self._image_border_width)
            pdf.set_draw_color(self._image_border_color)
            x = self.margin - self._image_border_width / 2
            y = self.tmargin - self._image_border_width / 2
            h = self.image_height + self._image_border_width
            w = self.image_with + self._image_border_width
            pdf.rect(x, y, w, h)
            pdf.set_draw_color(0, 0, 0)

        if image:
            pdf.image(image, h=self.image_height, w=self.image_with, x=self.margin, y=self.tmargin)

        self._addText(date, self._generateMonthMatrix(date))

    def _addText(date, matrix):
        pass

    def set_background_color(self, background_color):
        if background_color is not None:
            self._background_color = color_from_hex_string(background_color)

    def set_table_border(self, table_border):
        self._table_border = True if table_border is not None and table_border else False

    def set_table_background_color(self, table_background_color):
        if table_background_color is not None:
            self._table_background_color = color_from_hex_string(table_background_color)

    def set_table_background_tansparency(self, table_background_tansparency):
        if table_background_tansparency is not None:
            self._table_background_tansparency = float(table_background_tansparency) / 100

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
        self.shadow = shadow

    def set_center_month(self, center_month):
        if center_month is not None:
            self._month_align = 'C' if center_month else 'L'

    def set_options_from_request(self, request, postfix=''):
        self.set_background_color(request.POST.get('background_color' + postfix))
        self.set_center_month(request.POST.get('center_month' + postfix))

        self.set_table_border(request.POST.get('table_border' + postfix))
        self.set_table_background_color(request.POST.get('table_background_color' + postfix))
        self.set_table_background_tansparency(request.POST.get('table_background_tansparency' + postfix))

        self.set_image_border(request.POST.get('image_border' + postfix))
        self.set_image_border_color(request.POST.get('image_border_color' + postfix))
        self.set_image_border_widht(request.POST.get('image_border_width' + postfix))

    def set_ics_url(self, ics_url):
        if ics_url != "":
            start = date(2024, 1, 1)
            end = date(2024, 12, 31)
            evts = events(url=ics_url, start=start, end=end)
            for evt in evts:
                datekey = evt.start.strftime("%Y%m%d")
                if datekey not in self.eventlist:
                    self.eventlist[datekey] = []
                self.eventlist[datekey].append(evt.summary)
        else:
            self.eventlist = {}

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
        events = self._get_events(date)
        return {
            "day": str(date.day),
            "dayOfWeek": dayOfWeek,
            "week": date.isocalendar().week,
            "color": "#000000",
            "events": events,
            "isSunday": dayOfWeek == 7,
            "isStaurday": dayOfWeek == 6,
            "hasEvents": len(events) > 0
        }

    def get_month_name(self, date):
        return self._monthNames[date.month - 1]

    def get_month_name_with_year(self, date):
        return self.get_month_name(date) + " " + self._year(date)

    def _get_events(self, date):
        datekey = date.strftime("%Y%m%d")
        if datekey in self.eventlist:
            for evt in self.eventlist[datekey]:
                print("Event for ", datekey, ":", evt)
            return self.eventlist[datekey]
        else:
            return []

    def _year(self, date):
        return str(date.year)

    def _dayName(self, dayOfWeek):
        return self._dayNames[dayOfWeek - 1]

    def _dayNameAbbrev(self, dayOfWeek):
        return self._dayNamesAbbrev[dayOfWeek - 1]

    def _fontWeight(self, day):
        return "B" if day["isSunday"] or day["isStaurday"] or day["hasEvents"] else ""

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
