class lcd(object):

    def display_string(self, text, linenum):
        print '{0}: {1}'.format(linenum, text)

    def backlight_off(self):
        print 'backlight_off'

    def backlight_on(self):
        print 'backlight_on'
