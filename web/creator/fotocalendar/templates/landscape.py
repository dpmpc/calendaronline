from creator.fotocalendar.fotocalendar import FotoCalendar


class LandscapeFotoCalendar(FotoCalendar):

    def __init__(self, fullscreen=False):
        self._supports_events = True

        if fullscreen:
            super().__init__("L", 0, 297, 210)
            self._text_background = [255, 255, 255]
            self.tmargin = 0
            self._table_border = False
        else:
            super().__init__("L", 10, 277, 141)

        pdf = self.fpdf

        pdf.set_top_margin(self.tmargin)

        pdf.add_font(fname="files/font/Sawasdee.ttf")
        pdf.add_font(fname="files/font/Sawasdee-Bold.ttf", style="B", family="Sawasdee")
        pdf.set_font("Sawasdee", size=64)

    def _addText(self, date, matrix):
        pdf = self.fpdf

        pdf.set_margin(16)
        with pdf.local_context(fill_opacity=self._table_background_tansparency, stroke_opacity=0, fill_color=self._table_background_color):
            pdf.rect(10, 165, 277, 35, round_corners=self._text_background_round_corners, corner_radius=self._text_background_corner_radius, style="F")

        pdf.set_font(style='B', size=20)
        line_height = 8.5
        col_width = 8.5

        pdf.set_y(171)
        pdf.cell(txt=self.get_month_name_with_year(date), w=pdf.epw, align=self._month_align, new_x="LEFT", new_y="NEXT")

        pdf.set_y(182)
        pdf.set_font(size=7)
        for day in matrix:
            pdf.set_font(style=self._fontWeight(matrix[day]))
            pdf.cell(col_width, txt=self._dayNameAbbrev(matrix[day]["dayOfWeek"]), border=0, align="C", new_y="TOP")
        pdf.ln()
        pdf.set_font(size=11)
        pdf.set_line_width(0.01)
        events = []
        for day in matrix:
            pdf.set_font(style=self._fontWeight(matrix[day]))
            pdf.cell(col_width, line_height, txt=matrix[day]["day"], border=1 if self._table_border else 0, align="C", new_y="TOP")
            for event in matrix[day]["events"]:
                events.append(matrix[day]["day"] + ". " + event)

        if len(events) > 0:
            pdf.set_y(195)
            pdf.set_font(style="", size=8)
            pdf.cell(txt=' • '.join(events), w=pdf.epw, align=self.eventlist_align, new_x="LEFT", new_y="NEXT")
