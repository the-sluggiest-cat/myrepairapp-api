class BaseMRAException(Exception):
    def __init__(self, message):
        super().__init__(message)

class TooManyRequests(BaseMRAException):
    def __init__(self):
        super().__init__("Too many requests.")

class Forbidden(BaseMRAException):
    def __init__(self):
        super().__init__("This action is not allowed. Are you using the correct API key?")

class InternalServerError(BaseMRAException):
    def __init__(self):
        super().__init__("MyRepairApp responded with status code 500. It may be down for maintenance, or something went wrong internally.")

class BadRequest(BaseMRAException):
    def __init__(self, message: dict):
        super().__init__(message)

class MethodNotAllowed(BaseMRAException):
    def __init__(self):
        super().__init__("This action is not allowed on this resource. If you're reading this, I messed up, not you.")