from creator.fotocalendar.fotocalendar import FotoCalendar
from creator.fotocalendar.bo.config import DefaultConfig


class Design1FotoCalendar(FotoCalendar):
    __dark = (0, 0, 0)
    __medium1 = (160, 160, 160)
    __medium2 = (192, 192, 192)
    __bg_bright = (255, 255, 255)
    __fg_bright = (255, 255, 255)

    def __init__(self):
        self._font = "Purisa"
        super().__init__("L", 3, 224, 187)

    def get_default_config(self, date=None) -> DefaultConfig:
        config = super().get_default_config(date)
        config.table_border = True
        return config

    def _add_text(self, config, matrix):
        pdf = self.fpdf
        date = config.date

        col_width = 60
        line_height = (pdf.eph - 12) / 31
        grid_left = pdf.epw - col_width

        pdf.set_font(style='B', size=15)
        pdf.set_text_color(self.__dark)
        pdf.set_draw_color(self.__dark)
        pdf.set_fill_color(self.__bg_bright)

        pdf.set_xy(grid_left, self.tmargin)
        pdf.cell(col_width - 20, 10, txt=self.get_month_name(date), align=config.month_align, new_x="RIGHT", fill=True)
        pdf.cell(20, 10, txt=self._year(date), align="R", new_x="LEFT", new_y="NEXT", fill=True)

        for day in matrix:
            if matrix[day].is_sunday or matrix[day].is_holiday:
                pdf.set_text_color(self.__fg_bright)
                pdf.set_fill_color(self.__medium1)
            elif matrix[day].is_saturday:
                pdf.set_text_color(self.__dark)
                pdf.set_fill_color(self.__medium2)
            else:
                pdf.set_text_color(self.__dark)
                pdf.set_fill_color(self.__bg_bright)
            pdf.set_x(grid_left)
            pdf.set_font(size=10)
            pdf.cell(7, line_height, txt=matrix[day].day, border='T' if config.table_border else 0, align="R", new_y="TOP", fill=True)
            pdf.set_font(size=6)
            text = self._dayNameAbbrev(matrix[day].day_of_week)
            if len(matrix[day].events) > 0:
                text += " " + matrix[day].events[0]
            pdf.cell(col_width - 7, line_height, txt=text, border='T' if config.table_border else 0, align="L", new_y="NEXT", fill=True)

        pdf.set_x(grid_left)
        pdf.set_fill_color(self.__bg_bright)
        pdf.cell(col_width, 2, txt="", border=config.table_border, fill=True)
