"""Template Method pattern for notification message construction.

The Template Method pattern defines the skeleton of an algorithm in a base class,
letting subclasses override specific steps without changing the algorithm's structure.
"""

from abc import ABC, abstractmethod


class NotificationBuilder(ABC):
    """Abstract base class for building notification messages.

    This class implements the Template Method pattern. The build_notification()
    method defines the algorithm skeleton, while subclasses implement specific steps.
    """

    def build_notification(self) -> str:
        """
        Template method that defines the notification building algorithm.

        This method orchestrates the steps to build a complete notification message.
        Subclasses should NOT override this method.

        Returns:
            The complete formatted notification message
        """
        # Validate first
        self.validate()

        # Build components
        subject = self.build_subject()
        body = self.build_body()

        # Format the final message
        message = self.format_message(subject, body)

        return message

    @abstractmethod
    def build_subject(self) -> str:
        """
        Build the notification subject/title.

        This is a required step that subclasses must implement.

        Returns:
            The notification subject
        """
        pass

    @abstractmethod
    def build_body(self) -> str:
        """
        Build the notification body content.

        This is a required step that subclasses must implement.

        Returns:
            The notification body text
        """
        pass

    def format_message(self, subject: str, body: str) -> str:
        """
        Format the complete notification message.

        This is a concrete method with default implementation that subclasses
        can optionally override.

        Args:
            subject: The notification subject
            body: The notification body

        Returns:
            The formatted complete message
        """
        return f"Subject: {subject}\n\n{body}"

    def validate(self) -> None:
        """
        Validate the notification data.

        This is a hook method with default implementation. Subclasses can
        override to add validation logic.

        Raises:
            ValueError: If validation fails
        """
        # Default: no validation required
        pass
