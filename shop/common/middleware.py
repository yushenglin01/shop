import logging

from django.utils.deprecation import MiddlewareMixin
from user.models import User
from lib.http import render_json
from common import errors

errorlogger = logging.getLogger('err')

class AuthMiddleware(MiddlewareMixin):
    URL_WHITE_LIST = [
        '/usr/api/submit_phone',
        '/usr/api/submit_vcode',
    ]

    def process_request(self, request):
        print(request.path)
        if request.path in self.URL_WHITE_LIST:
            return

        uid = request.session.get('uid')
        if not uid:
            return render_json('user not login', errors.USER_NOT_LOGIN.code)

        try:
            user = User.get(id=uid)
            request.user = user
        except User.DoesNotExist:
            return render_json('no this user', errors.NO_THIS_USER.code)

class ExceptionHandlerMiddleware(MiddlewareMixin):
    def process_exception(self,request, exception):

        if isinstance(exception, errors.LogicError):
            errorlogger.error(exception.data)
            return render_json(exception.data, exception.code)
