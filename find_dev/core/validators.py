from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MaximumLengthValidator:
    """
    Validate that the password is of a maximum length.
    """

    def __init__(self, max_length=50):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _(f'This password is too long. Password must contain no more than {self.max_length} characters'),
                code="password_too_long",
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return _(f'Your password must contain no more than {self.max_length} characters')
