from creator.fotocalendar.fotocalendar import FotoCalendar


class PortraitFotoCalendar(FotoCalendar):
    def __init__(self):
        super().__init__("P", 16, 176, 195)
        pdf = self.fpdf
        pdf.add_font(fname="files/font/DejaVuSans.ttf", family="DejaVuSans")
        pdf.add_font(fname="files/font/DejaVuSans-Bold.ttf", style="B", family="DejaVuSans")
        pdf.set_font("DejaVuSans", size=64)

    def _addText(self, date, matrix):
        pdf = self.fpdf

        pdf.set_margins(16.75, 20)
        pdf.set_font(style='B', size=20)
        line_height = 8.5
        col_width = 25

        pdf.set_y(220)
        pdf.cell(txt=self.get_month_name_with_year(date), w=pdf.epw, align=self.month_align, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(size=8)
        for day in self._dayNames:
            pdf.cell(col_width, txt=day, border=0, align="C", new_y="TOP")
        pdf.ln()
        pdf.set_line_width(0.01)
        weeks = self.__toWeekMatrix(matrix)
        for weekId in weeks:
            for dayId in weeks[weekId]:
                day = weeks[weekId][dayId]
                txt = ''
                if day:
                    pdf.set_font(style=day["weigth"], size=15)
                    txt = day["day"]
                pdf.cell(col_width, line_height, txt=txt, border=self.table_border, align="C", new_y="TOP")

            pdf.set_font(style='', size=8)
            pdf.cell(col_width, line_height, txt=str(weekId), border=0, align="L", new_y="TOP")
            pdf.ln()

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
