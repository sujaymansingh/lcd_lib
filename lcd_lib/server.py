"""A simple server that controls an lcd display.
"""
import flask
import json
import os
import os.path

if os.getenv('NO_HARDWARE', '') == '1':
    import lcd_lib.fake_controller as controller
else:
    from lcd_lib import controller


class Server(flask.Flask):

    def __init__(self, name):
        super(Server, self).__init__(name)
        self.controller = controller.Controller()


app = Server(__name__)

@app.route('/lcd', methods=['POST'])
def lcd():
    request = flask.request

    raw_data = request.data
    data = json.loads(raw_data)

    display_already_on = False

    if 'line_1' in data:
        app.controller.set_line_1(data['line_1'])
        display_already_on = True

    if 'line_2' in data:
        app.controller.set_line_2(data['line_2'])
        display_already_on = True

    if 'display' in data:
        if data['display'] == 'on':
            if not display_already_on:
                app.controller.turn_display_on()
        elif data['display'] == 'off':
            app.controller.turn_display_off()

    response = flask.make_response(json.dumps({'ok': True}))
    response.headers["Content-type"] = "text/json"
    return response


@app.route('/debug', methods=['GET'])
def debug():
    return flask.render_template('debug.html')


@app.route('/jquery.js', methods=['GET'])
def jquery_js():
    filepath = os.path.join(os.path.dirname(__file__), 'templates', 'jquery.js')
    with open(filepath, 'r') as input_file:
        response = flask.make_response(input_file.read())
    response.headers["Content-type"] = "text/javascript"
    return response


if __name__ == '__main__':
    app.run(host= '0.0.0.0')
