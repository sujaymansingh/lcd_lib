import datetime
import os
import threading
import time

if str(os.getenv('NO_HARDWARE', '')) == '1':
    import fake_lcd_display as lcd_display
else:
    import lcd_display



class DimAfterDelay(threading.Thread):

    def __init__(self, delay_in_seconds, controller):
        super(DimAfterDelay, self).__init__()
        self.dim_timedelta = datetime.timedelta(seconds=delay_in_seconds)
        self.controller = controller

    def run(self):
        while self.controller.active:
            now = datetime.datetime.now()
            if self.controller.is_backlight_on and now - self.controller.last_updated_at > self.dim_timedelta:
                self.controller.turn_backlight_off()
            time.sleep(0.25)
        print 'thread finished'


class Controller(object):

    def __init__(self):
        self.lcd = lcd_display.lcd()
        self.line_length = 16
        self.last_updated_at = datetime.datetime.now()
        self.active = False
        self.is_backlight_on = True
        self.dimmer = DimAfterDelay(5, self)

    def set_line(self, linenum, text):
        if len(text) > self.line_length:
            text = text[0:self.line_length-1]
        self.lcd.display_string(text, linenum)
        self.is_backlight_on = True
        self.last_updated_at = datetime.datetime.now()

    def set_line_1(self, text):
        self.set_line(1, text)

    def set_line_2(self, text):
        self.set_line(2, text)

    def turn_backlight_off(self):
        self.is_backlight_on = False
        self.lcd.backlight_off()

    def turn_backlight_on(self):
        self.is_backlight_on = True
        self.lcd.backlight_on()

    def start(self):
        self.active = True
        self.dimmer.start()

    def stop(self):
        self.active = False
