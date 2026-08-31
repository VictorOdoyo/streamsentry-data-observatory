class DomainError(Exception):
    """Base class for expected workflow failures."""


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class ValidationError(DomainError):
    pass


class InvalidTransitionError(DomainError):
    pass
