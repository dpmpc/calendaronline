from creator.fotocalendar.fotocalendar import FotoCalendar


class PortraitFotoCalendar(FotoCalendar):

    _event_serparator = ' • '

    def __init__(self, fullscreen=False, fullwidth=False):
        self._supports_events = True
        self._supports_weeks = True

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
            super().__init__("P", 10, 190, 185)

        self._add_font("ArialRounded")

        pdf = self.fpdf
        pdf.set_font("ArialRounded", size=64)

    def _addText(self, date, matrix):
        pdf = self.fpdf

        with pdf.local_context(fill_opacity=self._table_background_tansparency, stroke_opacity=0, fill_color=self._table_background_color):
            pdf.rect(10, 215, 190, 73, round_corners=self._text_background_round_corners, corner_radius=self._text_background_corner_radius, style="F")

        pdf.set_margins(16.75, 20)
        pdf.set_font(style='B', size=20)
        line_height = 8.5
        col_width = 25

        pdf.set_y(222)
        pdf.cell(txt=self.get_month_name_with_year(date), w=pdf.epw, align=self._month_align, new_x="LMARGIN", new_y="NEXT")

        pdf.set_y(233)
        pdf.set_font(size=8)
        for day in self._dayNames:
            pdf.cell(col_width, txt=day, border=0, align="C", new_y="TOP")
        pdf.ln()
        weeks = self.__toWeekMatrix(matrix)
        events = []
        for weekId in weeks:
            for dayId in weeks[weekId]:
                day = weeks[weekId][dayId]
                txt = ''
                if day:
                    pdf.set_font(style=self._font_style_for_day(day), size=15)
                    txt = day["day"]
                    if len(day["events"]) > 0:
                        events.append(day["day"] + ". " + self._event_serparator.join(day["events"]))
                pdf.cell(col_width, line_height, txt=txt, border='BT' if self._table_border else 0, align="C", new_y="TOP")

            if self._show_weeks:
                pdf.set_font(style='', size=8)
                pdf.cell(col_width, line_height, txt=str(weekId), border=0, align="L", new_y="TOP")

            pdf.ln()

        if len(events) > 0:
            pdf.ln()
            pdf.set_font(style="", size=8)
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
