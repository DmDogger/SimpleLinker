from app.core.exceptions.base import ApplicationError

class NotFound(ApplicationError):
    pass

class LinkExist(ApplicationError):
    pass