class AppError(Exception):
    status = 400
    def __init__(self, message, status=None):
        super().__init__(message)
        self.message = message
        if status: self.status = status

class NotFound(AppError): status = 404
class Forbidden(AppError): status = 403
class Unauthorized(AppError): status = 401
