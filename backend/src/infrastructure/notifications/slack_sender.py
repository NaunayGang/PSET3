"""Slack notification command."""

import logging
from ...domain.patterns.command import Command

logger = logging.getLogger(__name__)


class SlackNotificationCommand(Command):
    """Command for sending Slack notifications."""

    def __init__(self, webhook_url: str, message: str):
        self.webhook_url = webhook_url
        self.message = message

    def execute(self) -> None:
        """Execute Slack sending."""
        logger.info(f"[SLACK] Webhook: {self.webhook_url}")
        logger.info(f"[SLACK] Message: {self.message}")
