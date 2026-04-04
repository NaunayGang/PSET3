"""Database seed script for development and testing.

Creates initial users: admin, supervisor, operator.
Run with: python -m src.seed
"""

from sqlalchemy.orm import Session

from .domain.enums.role import Role
from .domain.entities.user import User
from .infrastructure.database.connection import get_db
from .infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from .infrastructure.auth.password_handler import hash_password


def seed_initial_users():
    """
    Seed initial users if they don't exist.
    Password for all test users: 'password123'
    """
    db: Session = next(get_db())
    try:
        user_repo = SQLAlchemyUserRepository(db)

        # Create initial users
        initial_users = [
            {
                "name": "System Admin",
                "email": "admin@opscenter.com",
                "role": Role.ADMIN,
                "password": "password123",
            },
            {
                "name": "Team Supervisor",
                "email": "supervisor@opscenter.com",
                "role": Role.SUPERVISOR,
                "password": "password123",
            },
            {
                "name": "Field Operator",
                "email": "operator@opscenter.com",
                "role": Role.OPERATOR,
                "password": "password123",
            },
        ]

        created_count = 0
        skipped_count = 0
        for user_data in initial_users:
            if user_repo.find_by_email(user_data["email"]):
                skipped_count += 1
                print(f"Skipped existing user: {user_data['email']}")
                continue

            hashed = hash_password(user_data["password"])
            user = User(
                id=None,
                name=user_data["name"],
                email=user_data["email"],
                role=user_data["role"],
                hashed_password=hashed,
                created_at=None,
            )
            user_repo.save(user)
            created_count += 1
            print(f"Created user: {user.email}")

        print(f"✅ Seed completed. Created: {created_count}, Skipped: {skipped_count}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_initial_users()
