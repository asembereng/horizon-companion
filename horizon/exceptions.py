"""
Chapter 11: Error Handling — Custom Exceptions

Horizon-specific exception hierarchy. Custom exceptions make error
handling explicit and debuggable.
"""


class HorizonError(Exception):
    """Base exception for all Horizon errors.

    Chapter 11: A shared base class lets callers catch all
    Horizon errors with a single `except HorizonError`.
    """
    def __init__(self, message: str, code: str = "HORIZON_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(HorizonError):
    """Raised when input data fails validation."""
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(
            message=f"Validation error on '{field}': {message}",
            code="VALIDATION_ERROR",
        )


class NotFoundError(HorizonError):
    """Raised when a requested resource doesn't exist."""
    def __init__(self, resource: str, identifier: int | str):
        self.resource = resource
        self.identifier = identifier
        super().__init__(
            message=f"{resource} with id '{identifier}' not found",
            code="NOT_FOUND",
        )


class AuthenticationError(HorizonError):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, code="AUTH_ERROR")


class AuthorizationError(HorizonError):
    """Raised when a user lacks permission for an action."""
    def __init__(self, action: str, resource: str):
        super().__init__(
            message=f"Not authorized to {action} {resource}",
            code="FORBIDDEN",
        )
