from fpdf import FPDF, ViewerPreferences
from calendar import monthrange

class FotoCalendar:
    _dayNamesAbbrev = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    _dayNames = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    _monthNames = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

    def __init__(self, orientation, margin, image_with, image_height):
        self.border = False
        self.shadow = False
        self.margin = margin
        self.tmargin = 20
        self.image_with = image_with
        self.image_height = image_height
        self.month_align = 'L'
        self.table_border = 1

        pdf = FPDF(orientation=orientation, format="A4")
        self.fpdf = pdf
        pdf.set_display_mode(zoom="fullpage")
        pdf.set_auto_page_break(False)
        pdf.set_font('Helvetica')
        pdf.set_producer("k51.de - Simple create foto calendars as PDF")
        pdf.set_margin(self.margin)    
        pdf.set_top_margin(self.tmargin)    
       


    def addTitle(self, title='', image=None):
        pdf = self.fpdf
        if title != '':
            pdf.set_subject(title)
            pdf.add_page()
            pdf.set_font(style='B', size=100)
            # pdf.cell(txt=date.strftime("%Y"))
        
            pdf.cell(txt=title)
            if image:
                pdf.image(image, h=pdf.eph, w=pdf.epw, x=0, y=0)

    def addMonth(self, date, image=None, border=False, shadow=False, crop=None, background_color=None):
        pdf = self.fpdf
        pdf.add_page()
        if image:
            pdf.image(image, h=self.image_height, w=self.image_with,  x=self.margin, y=self.tmargin)

        self._addText(date, self._generateMonthMatrix(date))

    def _addText(date, matrix):
        pass

    def set_image_border(self, border):
        self.border = border

    def set_image_shadow(self, shadow):
        self.shadow = shadow

    def set_page_background(self, background):
        backgroundRgb = self._hex_color_to_tuple(background)
        print("Set background to ", background, " --> ", backgroundRgb)
        pdf = self.fpdf
        pdf.set_page_background(backgroundRgb)

    def set_center_month(self, center_month):
        self.month_align = 'C' if center_month else 'L'
    
    def set_table_border(self, table_border):
        self.table_border = 1 if table_border else 0
        
    def _generateMonthMatrix(self, date):
        matrix = {}
        max_days = monthrange(date.year, date.month)[1]
        for day in range(1, max_days + 1):
            date = date.replace(day=day)
            dayId = date.timetuple().tm_yday
            matrix[dayId] = self._createDay(date)
        return matrix

    def _createDay(self, date):
        dayOfWeek =  date.isoweekday()
        return {
                "day": str(date.day),
                "dayOfWeek": dayOfWeek,
                "week":  date.isocalendar().week,
                "color": "#000000",
                "weigth": "B" if dayOfWeek >= 6 else "",
            }

    def get_month_name(self, date):
        return self._monthNames[date.month - 1]

    def get_month_name_with_year(self, date):
        return self.get_month_name(date) + " " + self._year(date)

    def _year(self, date):
        return str(date.year)

    def _dayName(self, dayOfWeek):
        return self._dayNames[dayOfWeek - 1]

    def _dayNameAbbrev(self, dayOfWeek):
        return self._dayNamesAbbrev[dayOfWeek - 1]

    def _hex_color_to_tuple(self, color):
        if color.startswith('#'):
            color = color.lstrip('#')
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    
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


        