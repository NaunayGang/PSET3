"""Security utilities and decorators."""

from typing import Annotated
from fastapi import Depends

from ..domain.entities.user import User
from ..domain.enums.role import Role
from .dependencies import get_current_user, require_role

# Type aliases for common dependencies
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(require_role(Role.ADMIN))]
SupervisorOrAdmin = Annotated[User, Depends(require_role(Role.SUPERVISOR, Role.ADMIN))]
