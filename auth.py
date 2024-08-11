from myframeuz.middleware import Middleware
import re

STATIC_TOKEN = "jkfb42o9807ewf"

class TokenMiddleware(Middleware):
    regex = re.compile(r"^Token: (\w+)$")

    def process_request(self, request):

        header = request.headers.get("Authorization", "")
        match = self.regex.match(header)
        token = match and match.group(1) or None

        request.token = token

class InvalidTokenException(Exception):
    pass

def login_required(handler):
    def wrapper_handler(request, response, *args, **kwargs):
        token = getattr(request, "token", None)

        if token is None or token != STATIC_TOKEN:
            raise InvalidTokenException("Invalid Token")

        return handler(request, response, *args, **kwargs)

    return wrapper_handler

def on_exception(request, response , exception):
    if isinstance(exception, InvalidTokenException):
        response.text = "Token is invalid"
        response.status_code = 401