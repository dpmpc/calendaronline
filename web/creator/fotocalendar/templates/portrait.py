from creator.fotocalendar.fotocalendar import FotoCalendar
from creator.fotocalendar.bo.config import DefaultConfig


class PortraitFotoCalendar(FotoCalendar):

    _font = "BalsamiqSans"
    _y_offset_month_name = 222
    _y_offset_day_names = _y_offset_month_name + 11

    def __init__(self, fullscreen=False, fullwidth=False, margin=10, image_width=190, image_height=185):
        self._fullscreen = fullscreen
        self._fullwidth = fullwidth

        if fullscreen:
            super().__init__("P", 0, 210, 297)
            self._text_background = [255, 255, 255]
            self.tmargin = 0
        elif fullwidth:
            super().__init__("P", 0, 210, 205)
            self.tmargin = 0
        else:
            super().__init__("P", margin, image_width, image_height)

    def get_default_config(self, date=None) -> DefaultConfig:
        config = super().get_default_config(date)
        config.supports_italic = False
        config.event_serparator = ' • '
        if self._fullscreen:
            config.show_weeks = True
        elif self._fullwidth:
            config.month_align = 'C'
            config.show_weeks = False
        else:
            config.table_border = True
        return config

    def _add_text(self, config, matrix):
        pdf = self.fpdf

        self._add_table_background(config, 10, 215, 190, 73)
        pdf.set_margins(16.75, 20)

        line_height = 8.5
        col_width = 25

        pdf.set_y(self._y_offset_month_name)
        self._add_month_name(config)

        pdf.set_y(self._y_offset_day_names)
        self._set_font(config.fonts.dayname)
        for day in self._dayNames:
            pdf.multi_cell(col_width, txt=day, border=0, align="C", new_y="TOP")

        pdf.ln()
        weeks = self.__toWeekMatrix(matrix)
        events = []
        pdf.set_line_width(0.2)
        for weekId in weeks:
            for dayId in weeks[weekId]:
                day = weeks[weekId][dayId]
                txt = ''
                if day:
                    self._set_font_for_day(day, config)
                    txt = day.day
                    if len(day.events) > 0:
                        events.append(day.day + ". " + config.event_separator.join(day.events))
                pdf.cell(col_width, line_height, txt=txt, border='BT' if config.table_border else 0, align="C", new_y="TOP")

            if config.show_weeks:
                self._set_font(config.fonts.week)
                pdf.cell(col_width, line_height, txt=str(weekId), border=0, align="L", new_y="TOP")

            pdf.ln()

        if len(events) > 0:
            pdf.ln()
            self._set_font(config.fonts.event)
            pdf.cell(txt=config.event_separator.join(events), w=pdf.epw, align=config.eventlist_align, new_x="LEFT", new_y="NEXT")

    def __toWeekMatrix(self, month_matrix):
        weeks = {}
        for day in month_matrix:
            weekId = month_matrix[day].week
            if weekId not in weeks:
                weeks[weekId] = self.__emptyWeek()
            dayId = month_matrix[day].day_of_week
            weeks[weekId][dayId] = month_matrix[day]

        return weeks

    def __emptyWeek(self):
        return {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
