import typing

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404


class Rating(models.Model):
    """
    Создание рейтинга для привязанного объекта
    """

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="rating"
    )
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, null=True)

    class RatingStar(models.IntegerChoices):
        One = 1
        Two = 2
        Free = 3
        Four = 4
        Five = 5

    rating_star = models.IntegerField(choices=RatingStar.choices)

    def save(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        model_name = ContentType.objects.get(id=self.content_type.id).model_class()
        get_object_or_404(model_name, pk=self.object_id)
        super().clean()
        if (
            Rating.objects.filter(
                content_type__pk=self.content_type.id,
                object_id=self.object_id,
                user=self.user,
            ).exists()
            and self.id is None
        ):
            raise ValidationError("you have already taken a rating")


@receiver(post_delete, sender=Rating)
@receiver(post_save, sender=Rating)
def update_avg_rating_for_parent(
    sender: Rating, instance: Rating, **kwargs: typing.Any
) -> None:
    avg_rating = sender.objects.filter(
        content_type=instance.content_type, object_id=instance.object_id
    ).aggregate(avg_rating=Avg("rating_star"))
    instance.content_object.avg_rating = avg_rating["avg_rating"]
    instance.content_object.save()
