from django.core.validators import MinLengthValidator
from django.db import models


class IsAwardedField(models.Model):
    class Meta:
        abstract = True

    is_awarded = models.BooleanField(
        default=False
    )


class LastUpdatedField(models.Model):
    class Meta:
        abstract = True

    last_updated = models.DateTimeField(
        auto_now=True
    )
