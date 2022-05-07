import typing

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class CustomUser(AbstractUser):
    """
    Основная модель пользователя
    """

    rating = GenericRelation("community.rating", null=True, blank=True)
    avg_rating = models.IntegerField(null=True, blank=True)

    def __str__(self) -> typing.Any:
        return self.username
