
class CommsTemplateException(Exception):

    status_code = 500

    def __init__(self, errors, status_code=None):
        self.errors = errors if type(errors) is list else [errors]
        self.status_code = status_code or InvalidTemplateObject.status_code


class InvalidTemplateObject(CommsTemplateException):
    pass


class DatabaseError(CommsTemplateException):
    pass
