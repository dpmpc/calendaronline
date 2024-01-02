from creator.fotocalendar.fotocalendar import FotoCalendar


class PortraitFotoCalendar(FotoCalendar):

    _text_background = None

    def __init__(self, fullscreen=False):
        if fullscreen:
            super().__init__("P", 0, 210, 297)
            self._text_background = [255, 255, 255]
            self.tmargin = 0
            self.default_table_borders = False
        else:
            super().__init__("P", 10, 190, 185)

        pdf = self.fpdf
        pdf.add_font(fname="files/font/Arial Rounded MT Regular.ttf", family="ArialRounded")
        pdf.add_font(fname="files/font/Arial Rounded MT Bold Regular.ttf", style="B", family="ArialRounded")
        pdf.set_font("ArialRounded", size=64)

    def _addText(self, date, matrix):
        pdf = self.fpdf

        if self._text_background is not None:
            with pdf.local_context(fill_opacity=0.7, stroke_opacity=0, fill_color=self._text_background):
                pdf.rect(10, 215, 190, 73, round_corners=self._text_background_round_corners, corner_radius=self._text_background_corner_radius, style="F")

        pdf.set_margins(16.75, 20)
        pdf.set_font(style='B', size=20)
        line_height = 8.5
        col_width = 25

        pdf.set_y(222)
        pdf.cell(txt=self.get_month_name_with_year(date), w=pdf.epw, align=self.month_align, new_x="LMARGIN", new_y="NEXT")

        pdf.set_y(233)
        pdf.set_font(size=8)
        for day in self._dayNames:
            pdf.cell(col_width, txt=day, border=0, align="C", new_y="TOP")
        pdf.ln()
        pdf.set_line_width(0.01)
        weeks = self.__toWeekMatrix(matrix)
        events = []
        for weekId in weeks:
            for dayId in weeks[weekId]:
                day = weeks[weekId][dayId]
                txt = ''
                if day:
                    pdf.set_font(style=self._fontWeight(day), size=15)
                    txt = day["day"]
                    for event in day["events"]:
                        events.append(day["day"] + ". " + event)
                pdf.cell(col_width, line_height, txt=txt, border=self.table_border, align="C", new_y="TOP")

            pdf.set_font(style='', size=8)
            pdf.cell(col_width, line_height, txt=str(weekId), border=0, align="L", new_y="TOP")
            pdf.ln()

        if len(events) > 0:
            pdf.ln()
            pdf.set_font(style="", size=8)
            pdf.cell(txt=' - '.join(events), w=pdf.epw, align=self.eventlist_align, new_x="LEFT", new_y="NEXT")

    def set_table_border(self, table_border):
        self.table_border = 'BT' if table_border else 0

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
