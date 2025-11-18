from creator.fotocalendar.fotocalendar import FotoCalendar


class PortraitFotoCalendar(FotoCalendar):

    _event_serparator = ' • '
    _font = "BalsamiqSans"

    _font_size_month = 20
    _font_size_dayname = 8
    _font_size_day = 15
    _font_size_week = 8
    _font_size_events = 8

    _supports_events = True
    _supports_weeks = True
    _supports_italic = False

    def __init__(self, fullscreen=False, fullwidth=False, margin=10, image_with=190, image_height=185):
        if fullscreen:
            super().__init__("P", 0, 210, 297)
            self._text_background = [255, 255, 255]
            self.tmargin = 0
            self._table_border = False
        elif fullwidth:
            super().__init__("P", 0, 210, 205)
            self.tmargin = 0
            self._table_border = False
            self._show_weeks = False
            self._month_align = 'C'
        else:
            super().__init__("P", margin, image_with, image_height)

    def _addText(self, date, matrix):
        pdf = self.fpdf

        with pdf.local_context(fill_opacity=self._table_background_tansparency, stroke_opacity=0, fill_color=self._table_background_color):
            pdf.rect(10, 215, 190, 73, round_corners=self._text_background_round_corners, corner_radius=self._text_background_corner_radius, style="F")

        pdf.set_margins(16.75, 20)
        pdf.set_font(style='B', size=self._font_size_month)
        line_height = 8.5
        col_width = 25

        pdf.set_y(222)
        pdf.multi_cell(txt=self.get_month_name_with_year(date), w=pdf.epw, align=self._month_align, new_x="LMARGIN", new_y="NEXT")

        pdf.set_y(233)
        pdf.set_font(size=self._font_size_dayname)
        for day in self._dayNames:
            pdf.multi_cell(col_width, txt=day, border=0, align="C", new_y="TOP")
        pdf.ln()
        weeks = self.__toWeekMatrix(matrix)
        events = []
        pdf.set_line_width(0.2)
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

        if len(events) > 0:
            pdf.ln()
            pdf.set_text_color(0, 0, 0)
            pdf.set_font(style="", size=self._font_size_events)
            pdf.cell(txt=self._event_serparator.join(events), w=pdf.epw, align=self.eventlist_align, new_x="LEFT", new_y="NEXT")

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
