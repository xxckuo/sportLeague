"""
 Created by 七月 on 2018/5/12.
"""
from flask import request, json
from werkzeug.exceptions import HTTPException

__author__ = '七月'


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999
    data = dict()

    def __init__(self, msg=None, code=None, error_code=None,data=None,
                 headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            code=self.code,
            # request=request.method + ' ' + self.get_url_no_param()
            data = self.data
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]

