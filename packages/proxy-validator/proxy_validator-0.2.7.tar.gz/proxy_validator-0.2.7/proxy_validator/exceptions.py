class BaseError(Exception):
    pass


class ValidationProxyError(BaseError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"""{self.message}"""

    __repr__ = __str__
