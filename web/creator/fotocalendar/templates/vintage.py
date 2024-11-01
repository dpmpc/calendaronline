from creator.fotocalendar.templates.portrait import PortraitFotoCalendar
import math 


class VintageFotoCalendar(PortraitFotoCalendar):

    _font = "Tippa"
    _dayNames = ['Montag\n------', 'Dienstag\n--------', 'Mittwoch\n--------', 'Donnerstag\n----------', 'Freitag\n-------', 'Samstag\n-------', 'Sonntag\n-------']
    _image_border = True
    _image_border_width = 5

    _supports_fonts = False
    _supports_weeks = False

    def __init__(self):
        super().__init__(False, False, 20, 150, 100)
        self._month_align = 'C'
        self._font_size_month = 8
        self._font_size_dayname = 8
        self._font_size_day = 8
        self._font_size_week = 8
        self._font_size_events = 8   
        self._table_border = False

    def get_month_name_with_year(self, date):
        month_name = super().get_month_name_with_year(date)
        return " " + month_name + " \n" + "=" * (len(month_name) + 2)

    def _addImage(self, image):
        pdf = self.fpdf
        x = (pdf.w - self.image_with) / 2
        y = self.tmargin + 40
        h = self.image_height
        w = self.image_with
        if self._image_border:
            self._shadow(x, y, w, h)

        if image:
            pdf.image(image, h=h, w=w, x=x, y=y)
            self._tesa(x - 15, y + 5, 45)
            self._tesa(x + w - 17, y + h + 2, 40)
            self._tesa(x + w - 6, y - 13, - 50)
            self._tesa(x - 7, y + h - 15, - 40)

    def _shadow(self, x, y, w, h, width=1):
        bw_fraction = width / 5
        x1 = x + bw_fraction
        y1 = y + bw_fraction
        w1 = w - bw_fraction
        h1 = h - bw_fraction
        for i in range(0, 5):
            self._shadow_intern(x1 + bw_fraction * i, y1 + bw_fraction * i, w1, h1, bw_fraction, 0.43 - (0.1 * i))

    def _shadow_intern(self, x, y, w, h, border_width, opacity):
        pdf = self.fpdf

        bw2 = border_width / 2
        x1 = x + border_width
        x2 = x + w + bw2
        y1 = y + border_width
        y2 = y + h + bw2

        with pdf.local_context(fill_opacity=0.5, stroke_opacity=opacity, line_width=border_width):
            pdf.line(x1=x1, y1=y2, x2=x2 - border_width, y2=y2)
            pdf.line(x1=x2, y1=y1, x2=x2, y2=y2)

    def _tesa(self, x, y, phi_deg):
        phi = phi_deg * math.pi / 180
        x1 = x * math.cos(phi) - y * math.sin(phi)
        y1 = x * math.sin(phi) + y * math.cos(phi)
        with self.fpdf.rotation(phi_deg, x=0, y=0):
            self.fpdf.image('files/images/Tesa.png', x=x1, y=y1, w=30)
