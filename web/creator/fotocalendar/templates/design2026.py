from creator.fotocalendar.fotocalendar import FotoCalendar


class Design2026FotoCalendar(FotoCalendar):

    _event_serparator = ' • '
    _font = "NotoSansDisplay"

    _font_size_month = 75
    _font_size_dayname = 14
    _font_size_day = 15
    _font_size_week = 8
    _font_size_events = 8

    _font_color_month = "#ffffff"

    _supports_events = True
    _supports_weeks = True
    _supports_italic = False

    _table_border = False
    _table_background_color = "#C8C8C8"
    _table_background_tansparency = 1

    _show_weeks = False
    _month_align = 'C'

    def __init__(self):
        super().__init__("P", 0, 210, 180)
        self.tmargin = 0
        self._add_font("Pacifico")

    def _addText(self, date, matrix):
        pdf = self.fpdf

        x = pdf.w - 10
        y = self.image_height - 8
        text = '{:>02}  '.format(date.month)
        self.__draw_text_circle(x, y, text, 30, 90)

        line_height = 11.5
        col_width = 21
        pdf.set_margins((pdf.w - 7 * col_width) / 2, 20)

        pdf.set_y(y)

        # with pdf.local_context(text_color=self._table_background_color, font_size_pt=self._font_size_month, font_family="Pacifico", text_mode=2, stroke_opacity=1, draw_color=self._background_color):
        with pdf.local_context(text_color=self._table_background_color, font_size_pt=self._font_size_month, font_family="Pacifico"):
            pdf.cell(txt=self.get_month_name(date), w=pdf.epw, align=self._month_align, new_x="LMARGIN", new_y="NEXT")

        x = pdf.get_x() + col_width / 2
        for day in self._dayNamesAbbrev:
            self.__draw_text_circle(x, y + 40, day)
            x = x + col_width

        pdf.set_y(y + 50)
        weeks = self.__toWeekMatrix(matrix)
        events = []
        for weekId in weeks:
            for dayId in weeks[weekId]:
                day = weeks[weekId][dayId]
                txt = ''
                if day:
                    pdf.set_font(style=day["fontStyle"], size=self._font_size_day)
                    pdf.set_text_color(day["color"])
                    txt = day["day"]
                    if len(day["events"]) > 0:
                        events.append(day["day"] + ". " + self._event_serparator.join(day["events"]))
                pdf.cell(col_width, line_height, txt=txt, border='BT' if self._table_border else 0, align="C", new_y="TOP")

            if self._show_weeks:
                pdf.set_text_color(0, 0, 0)
                pdf.set_font(style='', size=self._font_size_week)
                pdf.cell(col_width, line_height, txt=str(weekId), border=0, align="L", new_y="TOP")

            pdf.ln()

    def __draw_text_circle(self, x, y, text, radius=5.5, font_size=None):
        pdf = self.fpdf
        font_size = self._font_size_dayname if font_size is None else font_size

        pdf.set_xy(x - radius / 2, y - radius / 2)
        with pdf.local_context(fill_opacity=self._table_background_tansparency, fill_color=self._table_background_color, font_size_pt=font_size, font_style='B', text_color=self._font_color_month):
            pdf.circle(x=x, y=y, radius=radius, style="F")
            pdf.cell(w=radius, h=radius, text=text, align='C', border=0)

    def __toWeekMatrix(self, monthMatrix):
        weeks = {}
        for day in monthMatrix:
            weekId = monthMatrix[day]["week"]
            if weekId not in weeks:
                weeks[weekId] = self.__emptyWeek()
            dayId = monthMatrix[day]["dayOfWeek"]
            weeks[weekId][dayId] = monthMatrix[day]

        return weeks

    def __emptyWeek(self):
        return {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
