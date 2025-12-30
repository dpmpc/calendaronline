from creator.fotocalendar.fotocalendar import FotoCalendar
from creator.fotocalendar.bo.config import DefaultConfig


class Design2026FotoCalendar(FotoCalendar):

    _font = "NotoSansDisplay"

    def __init__(self):
        super().__init__("P", 0, 210, 180)
        self.tmargin = 0
        self._add_font("Pacifico")

    def get_default_config(self, date=None) -> DefaultConfig:
        config = super().get_default_config(date)
        config.show_weeks = False
        config.month_show_year = False
        config.supports_italic = False
        config.month_align = 'C'

        config.table_background_color = '#C8C8C8'
        config.fonts.month.size = 75
        config.fonts.month.family = "Pacifico"
        config.fonts.month.color = '#C8C8C8'
        config.fonts.weekday.size = 14
        config.fonts.dayname.color = '#FFFFFF'
        config.fonts.dayname.size = 15
        return config

    def _add_text(self, config, matrix):
        pdf = self.fpdf
        config.fonts.month.color = config.table_background_color

        y = self.image_height - 8.7
        pdf.set_y(y)
        self._add_month_name(config)

        line_height = 11.5
        col_width = 21
        pdf.set_margins((pdf.w - 7 * col_width) / 2, 20)

        x = pdf.get_x() + col_width / 2
        for day in self._dayNamesAbbrev:
            self.__draw_text_circle(x, y + 40, day, config)
            x = x + col_width

        pdf.set_y(y + 50)
        weeks = self.__toWeekMatrix(matrix)
        events = []
        for weekId in weeks:
            for dayId in weeks[weekId]:
                day = weeks[weekId][dayId]
                txt = ''
                if day:
                    self._set_font_for_day(day, config)
                    txt = day.day
                    if len(day.events) > 0:
                        events.append(day.day + ". " + config.event_serparator.join(day.events))
                pdf.cell(col_width, line_height, txt=txt, border='BT' if config.table_border else 0, align="C", new_y="TOP")

            if config.show_weeks:
                self._set_font(config.fonts.week)
                pdf.cell(col_width, line_height, txt=str(weekId), border=0, align="L", new_y="TOP")

            pdf.ln()

    def _add_month_name(self, config):
        y = self.fpdf.get_y() - 1.2
        x = self.fpdf.w - 10
        super()._add_month_name(config)

        # Draw circle with month number
        self._set_font(config.fonts.dayname)
        text = '{:>02}  '.format(config.date.month)
        self.__draw_text_circle(x, y, text, config, 30, 90)

    def __draw_text_circle(self, x, y, text, config, radius=5.5, font_size=None):
        pdf = self.fpdf
        font_size = config.fonts.dayname.size if font_size is None else font_size

        pdf.set_xy(x - radius / 2, y - radius / 2)
        with pdf.local_context(fill_opacity=float(config.table_background_opacity) / 100.0, fill_color=config.table_background_color, font_size_pt=font_size, font_style='B'):
            pdf.circle(x=x, y=y, radius=radius, style="F")
            pdf.cell(w=radius, h=radius, text=text, align='C', border=0, new_x="LMARGIN", new_y="NEXT")

    def __toWeekMatrix(self, monthMatrix):
        weeks = {}
        for day in monthMatrix:
            weekId = monthMatrix[day].week
            if weekId not in weeks:
                weeks[weekId] = self.__emptyWeek()
            dayId = monthMatrix[day].day_of_week
            weeks[weekId][dayId] = monthMatrix[day]

        return weeks

    def __emptyWeek(self):
        return {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
