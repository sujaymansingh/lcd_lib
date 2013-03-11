import lcd_display


class Controller(object):

    def __init__(self):
        self.lcd = lcd_display.lcd()
        self.line_length = 16

    def set_line(self, linenum, text):
        if len(text) > self.line_length:
            text = text[0:self.line_length-1]
        self.lcd.display_string(text, linenum)

    def set_line_1(self, text):
        self.set_line(1, text)

    def set_line_2(self, text):
        self.set_line(2, text)

    def turn_backlight_off(self):
        self.lcd.backlight_off()

    def turn_backlight_on(self):
        self.lcd.backlight_on()
