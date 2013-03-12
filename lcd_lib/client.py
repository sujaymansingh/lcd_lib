"""A client wrapper for the api.
"""
import json
import requests


class LCDException(Exception):
    pass


class Client(object):

    def __init__(self, host='localhost', port=5000):
        self.url = 'http://{0}:{1}/api/v1/lcd'.format(host, port)

    def set_text(self, line_1=None, line_2=None):
        payload = {}
        if line_1:
            payload['line_1'] = line_1
        if line_2:
            payload['line_2'] = line_2

        headers = {'content-type': 'application/json'}
        response = requests.post(self.url, data=json.dumps(payload), headers=headers)

        response_payload = json.loads(response.content)
        ok = response_payload['ok']

        if not ok:
            raise LCDException(response.content)
        
