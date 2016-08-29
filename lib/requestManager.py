import requests
from lib.logger import Logger

log = Logger


class RequestManager(object):

    @staticmethod
    def post_request(url, **payload):
        r = requests.post(url, payload)
        log.logger("INFO", 'POST Request sent. URL: %s, payload: %s' % (url, payload))
        resp = {"response": r.json(), "code": r.status_code}
        log.logger('INFO', resp)
        return resp

    @staticmethod
    def get_request(url, **payload):
        r = requests.get(url, payload)
        log.logger("INFO", 'GET Request sent. URL: %s, payload: %s' % (url, payload))
        resp = {"response": r.json(), "code": r.status_code}
        log.logger('INFO', resp)
        return resp

