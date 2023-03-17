import uuid

from django.db import models
from django.utils.text import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created_at = models.DateField(_('дата создания'), auto_now_add=True)

    class Meta:
        abstract = True
