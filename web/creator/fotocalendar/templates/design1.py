from creator.fotocalendar.fotocalendar import FotoCalendar


class Design1FotoCalendar(FotoCalendar):
    __dark = (0, 0, 0)
    __medium1 = (160, 160, 160)
    __medium2 = (192, 192, 192)
    __bg_bright = (255, 255, 255)
    __fg_bright = (255, 255, 255)

    def __init__(self):
        self._font = "Purisa"
        super().__init__("L", 3, 224, 187)
        self._supports_events = True

    def _addText(self, date, matrix):
        pdf = self.fpdf
        col_width = 60
        line_height = (pdf.eph - 12) / 31
        grid_left = pdf.epw - col_width

        pdf.set_font(style='B', size=15)
        self._set_text_color(self.__dark)
        self._set_draw_color(self.__dark)
        self._set_fill_color(self.__bg_bright)

        pdf.set_xy(grid_left, self.tmargin)
        pdf.cell(col_width - 20, 10, txt=self.get_month_name(date), align=self._month_align, new_x="RIGHT", fill=True)
        pdf.cell(20, 10, txt=self._year(date), align="R", new_x="LEFT", new_y="NEXT", fill=True)

        for day in matrix:
            if matrix[day]["isSunday"] or matrix[day]['isHoliday']:
                self._set_text_color(self.__fg_bright)
                self._set_fill_color(self.__medium1)
            elif matrix[day]["isSaturday"]:
                self._set_text_color(self.__dark)
                self._set_fill_color(self.__medium2)
            else:
                self._set_text_color(self.__dark)
                self._set_fill_color(self.__bg_bright)
            pdf.set_x(grid_left)
            pdf.set_font(size=10)
            pdf.cell(7, line_height, txt=matrix[day]["day"], border='T' if self._table_border else 0, align="R", new_y="TOP", fill=True)
            pdf.set_font(size=6)
            text = self._dayNameAbbrev(matrix[day]["dayOfWeek"])
            if len(matrix[day]["events"]) > 0:
                text += " " + matrix[day]['events'][0]
            pdf.cell(col_width - 7, line_height, txt=text, border='T' if self._table_border else 0, align="L", new_y="NEXT", fill=True)

        pdf.set_x(grid_left)
        self._set_fill_color(self.__bg_bright)
        pdf.cell(col_width, 2, txt="", border=self._table_border, fill=True)
