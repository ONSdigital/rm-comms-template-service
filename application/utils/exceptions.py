
class CommsTemplateException(Exception):

    status_code = 500

    def __init__(self, error, status_code=None):
        self.error = error
        self.status_code = status_code or CommsTemplateException.status_code


class InvalidTemplateException(CommsTemplateException):
    pass


class DatabaseError(CommsTemplateException):
    pass
