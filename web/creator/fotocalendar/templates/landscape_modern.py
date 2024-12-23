from creator.fotocalendar.templates.landscape import LandscapeFotoCalendar


class LandscapeModernFotoCalendar(LandscapeFotoCalendar):

    _event_serparator = ' • '

    def __init__(self):
        # super().__init__(False)
        # self.image_height = 149
        super().__init__(True)
        self.image_height = 167
        self._table_border = False
        self._add_font("MonsieurLaDoulaise")

    def _addBackground(self):
        pass

    def _addMonthName(self, date):
        monthName = self.get_month_name(date)

        pdf = self.fpdf
        pdf.set_font(family="MonsieurLaDoulaise", size=80)
        pdf.set_text_color(220, 220, 220)
        textWidth = pdf.get_string_width(monthName, True) + 2
        if monthName[-1] == 'l':
            textWidth += 12
        elif monthName[-1] == 't':
            textWidth += 8
        elif monthName[-2] == 'l':
            textWidth += 7
        pdf.text(pdf.epw - textWidth, 197, monthName)
        pdf.set_text_color(0, 0, 0)

    def _addDays(self, matrix, x, y, width):
        super()._addDays(matrix, 10, y, width - 20)
