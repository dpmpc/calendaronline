from creator.fotocalendar.templates.landscape import LandscapeFotoCalendar
from creator.fotocalendar.bo.config import DefaultConfig


class LandscapeModernFotoCalendar(LandscapeFotoCalendar):
    def __init__(self):
        super().__init__(True)
        self.image_height = 167
        self._add_font("MonsieurLaDoulaise")

    def get_default_config(self, date=None) -> DefaultConfig:
        config = super().get_default_config(date)
        config.month_align = 'R'
        config.month_show_year = False
        config.fonts.month.size = 80
        config.fonts.month.color = '#DCDCDC'
        config.fonts.month.family = 'MonsieurLaDoulaise'
        return config

    def _add_table_background(self, config, x, y, w, h):
        pass

    def _add_month_name(self, config):
        self.fpdf.set_y(173)
        super()._add_month_name(config)

    def _add_days(self, matrix, x, y, width, config):
        super()._add_days(matrix, 10, y, width - 20, config)
