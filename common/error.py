from fastapi import HTTPException

class BadRequestException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Bad Request")

class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Unauthorized")

class ForbiddenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Forbidden")

class NotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Not Found")