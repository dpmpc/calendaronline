from creator.fotocalendar.fotocalendar import FotoCalendar


class LandscapeFotoCalendar(FotoCalendar):
    def __init__(self):
        super().__init__("L", 16, 263.5, 148.2)
        # pdf = self.fpdf
        # pdf.add_font(fname="files/font/Sawasdee.ttf")
        # pdf.add_font(fname="files/font/Sawasdee-Bold.ttf", style="B", family="Sawasdee")
        # pdf.set_font("Sawasdee", size=64)

        # pdf.add_font(fname="files/font/DejaVuSans-ExtraLight.ttf", family="DejaVuSans")
        # pdf.add_font(fname="files/font/DejaVuSans.ttf", style="B", family="DejaVuSans")
        # pdf.set_font("DejaVuSans", size=64)

    def _addText(self, date, matrix):
        pdf = self.fpdf

        pdf.set_font(style='B', size=20)
        line_height = 8.5
        col_width = 8.5

        pdf.set_y(173)
        pdf.cell(txt=self.get_month_name_with_year(date), w=pdf.epw, align=self.month_align, new_x="LEFT", new_y="NEXT")
        pdf.set_font(size=8)
        for day in matrix:
            pdf.set_font(style=self._fontWeight(matrix[day]))
            pdf.cell(col_width, txt=self._dayNameAbbrev(matrix[day]["dayOfWeek"]), border=0, align="C", new_y="TOP")
        pdf.ln()
        pdf.set_font(size=15)
        pdf.set_line_width(0.01)
        events = []
        for day in matrix:
            pdf.set_font(style=self._fontWeight(matrix[day]))
            pdf.cell(col_width, line_height, txt=matrix[day]["day"], border=self.table_border, align="C", new_y="TOP")
            for event in matrix[day]["events"]:
                events.append(matrix[day]["day"] + ". " + event)

        if len(events) > 0:
            pdf.set_y(195)
            pdf.set_font(style="", size=8)
            pdf.cell(txt=' - '.join(events), w=pdf.epw, align=self.eventlist_align, new_x="LEFT", new_y="NEXT")
