import traceback
import typing
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import models
from django.db.models.signals import post_save
from django.db.transaction import atomic
from django.dispatch import receiver
from django.utils.timezone import now, timedelta

from user.messages import (
    CHANGE_PASSWORD_MESSAGE,
    CHANGE_PASSWORD_MESSAGE_SUCCESS,
    EXPIER_TOCKEN,
    MESSAGE_TITLE,
    MESSAGE_TITLE_SUCCESS,
)
from user.service import create_token
from user.tasks import send_reset_password_code

if typing.TYPE_CHECKING:
    from user.models import CustomUser


class PasswordChangeOrderManager(models.Manager):
    def get_for_activating(self) -> models.QuerySet:
        return super().get_queryset().filter(activated=False)


class PasswordChangeOrder(models.Model):
    """
    Модель заявки на спену пародя пользователя
    """

    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    password = models.CharField(max_length=16)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    error_response = models.TextField(null=True, blank=True)
    sent_at = models.DateTimeField(default=now)
    activated = models.BooleanField(default=False)
    objects = PasswordChangeOrderManager()

    def clean(self) -> None:
        if self.sent_at + timedelta(minutes=10) < now():
            raise ValidationError("Your token was expired")

    def save(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def send(self) -> None:
        """Send email with activation url."""
        self.clean()
        try:
            self.send_email()
        except Exception:
            self.error_response = traceback.format_exc()
            self.save()

    def send_email(self) -> EmailMultiAlternatives:
        title = MESSAGE_TITLE
        activation_frontend_url = (
            f'{settings.FRONTEND_URL}{"user/change_password"}/{self.uuid}/activation/'
        )
        text = f"{CHANGE_PASSWORD_MESSAGE} {activation_frontend_url} {EXPIER_TOCKEN}"
        response = send_mail(
            title, text, settings.EMAIL_HOST_USER, [self.user.email], fail_silently=True
        )
        return response

    @atomic
    def activate(self) -> typing.Dict[str, str]:
        """
        Changes password for related user.

        Returns dict with token for REST authorization.
        """
        self.activated = True
        self.save()
        user: CustomUser = self.user
        user.set_password(self.password)
        user.save()
        data = {"token": create_token(user)}
        return data


@receiver(post_save, sender=PasswordChangeOrder)
def send_reset_password_code_signal(
    sender: PasswordChangeOrder,
    instance: PasswordChangeOrder,
    *args: typing.Any,
    **kwargs: typing.Any,
) -> None:
    PasswordChangeOrder.objects.filter(user=instance.user).exclude(
        pk=instance.pk
    ).delete()
    if instance.activated:
        title = MESSAGE_TITLE_SUCCESS
        text = CHANGE_PASSWORD_MESSAGE_SUCCESS
        send_mail(
            title,
            text,
            settings.EMAIL_HOST_USER,
            [instance.user.email],
            fail_silently=True,
        )
    else:
        send_reset_password_code(instance.id)
