"""Email notification command."""

import logging
from ...domain.patterns.command import Command

logger = logging.getLogger(__name__)


class EmailNotificationCommand(Command):
    """Command for sending email notifications."""

    def __init__(self, recipient: str, subject: str, body: str):
        self.recipient = recipient
        self.subject = subject
        self.body = body

    def execute(self) -> None:
        """Execute email sending."""
        logger.info(f"[EMAIL] To: {self.recipient}")
        logger.info(f"[EMAIL] Subject: {self.subject}")
        logger.info(f"[EMAIL] Body: {self.body}")
