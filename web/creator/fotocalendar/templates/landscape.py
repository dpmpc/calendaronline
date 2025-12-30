from creator.fotocalendar.fotocalendar import FotoCalendar
from creator.fotocalendar.bo.config import DefaultConfig


class LandscapeFotoCalendar(FotoCalendar):

    _font = "Sawasdee"

    def __init__(self, fullscreen=False):
        self._fullscreen = fullscreen
        if fullscreen:
            super().__init__("L", 0, 297, 210)
            self.tmargin = 0
        else:
            super().__init__("L", 10, 277, 141)

    def get_default_config(self, date=None) -> DefaultConfig:
        config = super().get_default_config(date)
        config.month_align = 'L'
        config.fonts.dayname.size = 7
        config.fonts.weekday.size = 11
        config.fonts.saturday.size = 11
        config.fonts.sunday.size = 11
        if not self._fullscreen:
            config.table_border = True
        return config

    def _add_text(self, config, matrix):
        pdf = self.fpdf
        self._add_table_background(config, 10, 165, 277, 35)
        pdf.set_y(171)
        self._add_month_name(config)

        self._add_days(matrix, pdf.l_margin, 182, pdf.epw, config)

    def _add_table_background(self, config, x, y, w, h):
        self.fpdf.set_margin(16)
        super()._add_table_background(config, x, y, w, h)

    def _add_days(self, matrix, x, y, width, config):
        pdf = self.fpdf
        col_width = width / len(matrix)
        line_height = 8.5

        pdf.set_xy(x, y)
        self._set_font(config.fonts.dayname)
        for day in matrix:
            if matrix[day].is_saturday or matrix[day].is_sunday:
                pdf.set_font(style='B')
            else:
                pdf.set_font(style='')
            pdf.cell(col_width, txt=self._dayNameAbbrev(matrix[day].day_of_week), border=0, align="C", new_y="TOP")
        pdf.set_xy(x, y + pdf._lasth)
        pdf.set_line_width(0.01)
        events = []
        for day in matrix:
            self._set_font_for_day(matrix[day], config)
            pdf.cell(col_width, line_height, txt=matrix[day].day, border=1 if config.table_border else 0, align="C", new_y="TOP")
            if len(matrix[day].events) > 0:
                events.append(matrix[day].day + ". " + config.event_separator.join(matrix[day].events))

        if len(events) > 0:
            pdf.set_y(195)
            pdf.set_font(style="", size=8)
            pdf.cell(txt=config.event_separator.join(events), w=pdf.epw, align=config.eventlist_align, new_x="LEFT", new_y="NEXT")
