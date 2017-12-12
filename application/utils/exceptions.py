
class CommsTemplateException(Exception):
    """ Base exception class allowing consistent formatting of error messages and http codes"""

    status_code = 500

    def __init__(self, error, status_code=None):
        self.error = error
        self.status_code = status_code or CommsTemplateException.status_code


class InvalidTemplateException(CommsTemplateException):
    """ Exception for handling malformed or incorrect data relating to templates"""
    pass


class DatabaseError(CommsTemplateException):
    """ Exception for handling interactions with the database"""
    pass


class InvalidClassificationType(CommsTemplateException):
    """ Exception for handling malformed or incorrect data relating to classifciation types"""
    pass
