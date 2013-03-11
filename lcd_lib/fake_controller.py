class Controller(object):

    def __init__(self):
        self.line_length = 16

    def set_line(self, linenum, text):
        if len(text) > self.line_length:
            text = text[0:self.line_length-1]
        print '{0}: {1}'.format(linenum, text)

    def set_line_1(self, text):
        self.set_line(1, text)

    def set_line_2(self, text):
        self.set_line(2, text)

    def turn_display_off(self):
        print 'display_off'

    def turn_display_on(self):
        print 'display_on'
