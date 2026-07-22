import unicodedata

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_complete_unicode_slug(value):
    """Allow Unicode letters, numbers and combining marks used by Hindi."""
    if not value:
        return

    for character in value:
        category = unicodedata.category(character)
        if category[0] not in {"L", "N", "M"} and character not in {"-", "_"}:
            raise ValidationError(
                _("Enter a valid slug using letters, numbers, underscores, or hyphens."),
                code="invalid",
            )


class CompleteUnicodeSlugFormField(forms.SlugField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators = [
            validator
            for validator in self.validators
            if not isinstance(validator, validators.RegexValidator)
        ]
        self.validators.append(validate_complete_unicode_slug)


class CompleteUnicodeSlugField(models.SlugField):
    """SlugField that preserves and validates Hindi combining characters."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_validators = [validate_complete_unicode_slug]
        # SlugField may cache its original RegexValidator during initialization.
        self.__dict__.pop("validators", None)

    def formfield(self, **kwargs):
        kwargs["form_class"] = CompleteUnicodeSlugFormField
        return super().formfield(**kwargs)
