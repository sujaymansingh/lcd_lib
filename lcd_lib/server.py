"""A simple server that controls an lcd display.
"""
import flask
import json
import os
import os.path
import traceback

import controller


class Server(flask.Flask):

    def __init__(self, name):
        super(Server, self).__init__(name)
        self.controller = controller.Controller()

    def __enter__(self):
        print self.controller
        self.controller.start()
        return self

    def __exit__(self, type_, value, traceback):
        self.controller.stop()


app = Server(__name__)

@app.route('/api/v1/lcd', methods=['POST'])
def lcd():
    try:
        request = flask.request
    
        raw_data = request.data
        data = json.loads(raw_data)
    
        backlight_already_on = False
    
        if 'line_1' in data:
            app.controller.set_line_1(data['line_1'])
            backlight_already_on = True
    
        if 'line_2' in data:
            app.controller.set_line_2(data['line_2'])
            backlight_already_on = True
    
        if 'backlight' in data:
            if data['backlight'] == 'on':
                if not backlight_already_on:
                    app.controller.turn_backlight_on()
            elif data['backlight'] == 'off':
                app.controller.turn_backlight_off()
    
        response = flask.make_response(json.dumps({'ok': True}))
        response.headers["Content-type"] = "text/json"
        return response
    except:
        traceback.print_exc()


@app.route('/api/v1/debug', methods=['GET'])
def debug():
    return flask.render_template('debug.html')


@app.route('/api/v1/jquery.js', methods=['GET'])
def jquery_js():
    filepath = os.path.join(os.path.dirname(__file__), 'templates', 'jquery.js')
    with open(filepath, 'r') as input_file:
        response = flask.make_response(input_file.read())
    response.headers["Content-type"] = "text/javascript"
    return response


if __name__ == '__main__':
    with app as server:
        server.run(host='0.0.0.0')
