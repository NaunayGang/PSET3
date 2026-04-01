"""Domain layer exceptions."""


class DomainException(Exception):
    """Base exception for domain layer errors."""

    pass


class ValidationError(DomainException):
    """Raised when entity validation fails."""

    pass


class InvalidStateTransitionError(DomainException):
    """Raised when an invalid state transition is attempted."""

    def __init__(self, message: str = "Invalid state transition"):
        super().__init__(message)


class EntityNotFoundError(DomainException):
    """Raised when a requested entity is not found."""

    def __init__(self, entity_type: str, entity_id: int):
        super().__init__(f"{entity_type} with ID {entity_id} not found")
        self.entity_type = entity_type
        self.entity_id = entity_id


class PermissionDeniedError(DomainException):
    """Raised when a user lacks permission for an action."""

    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)


class BusinessRuleViolationError(DomainException):
    """Raised when a business rule is violated."""

    pass
