import traceback
import typing
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.db.transaction import atomic
from django.dispatch import receiver
from django.utils.timezone import now, timedelta

from user.messages import (
    CREATE_ACCOUNT_MESSAGE,
    CREATE_ACCOUNT_MESSAGE_SUCCESS,
    EXPIER_TOCKEN,
    MESSAGE_TITLE,
    MESSAGE_TITLE_SUCCESS,
)
from user.service import create_token
from user.tasks import send_create_user_code

from .user import CustomUser


class CreateUserManager(models.Manager):
    def get_for_activating(self) -> QuerySet:
        return super().get_queryset().filter(activated=False)


class SignUpOrder(models.Model):
    """
    Модель заявки на регистрацию пользователя
    """

    email = models.EmailField()
    sent_at = models.DateTimeField(default=now)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    username = models.CharField(max_length=200)
    activated = models.BooleanField(default=False)
    objects = CreateUserManager()
    error_response = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=16)

    def send(self) -> None:
        """Send email with activation url."""
        try:
            self.send_email()
            self.sent_at = now()
        except Exception:
            self.error_response = traceback.format_exc()
            self.save()

    def send_email(self) -> EmailMultiAlternatives:
        title = MESSAGE_TITLE
        activation_url = (
            f"{settings.FRONTEND_URL}user/create_user/{self.uuid}/activation/"
        )
        text = f"{CREATE_ACCOUNT_MESSAGE} {activation_url} {EXPIER_TOCKEN}"
        response = send_mail(
            title, text, settings.EMAIL_HOST_USER, [self.email], fail_silently=True
        )
        return response

    @atomic
    def activate(self) -> typing.Dict[str, str]:
        self.activated = True
        self.save()
        user = CustomUser.objects.create_user(
            username=self.username, password=self.password, email=self.email
        )
        data = {"token": create_token(user)}
        return data

    def clean(self) -> None:
        """
        Токен действует не более 10 минут. При просроченном токене регистрация невозможна
        """
        if self.sent_at + timedelta(minutes=10) < now():
            raise ValidationError("Your token was expired")
        if CustomUser.objects.filter(email=self.email).exists():
            raise ValidationError("Your email have already busy")

    def save(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.clean()
        super().save(*args, **kwargs)


@receiver(post_save, sender=SignUpOrder)
def send_reset_password_code_signal(
    sender: SignUpOrder, instance: SignUpOrder, **kwargs: typing.Any
) -> None:
    SignUpOrder.objects.filter(username=instance.username).exclude(
        pk=instance.pk
    ).delete()
    if instance.activated:
        title = MESSAGE_TITLE_SUCCESS
        text = CREATE_ACCOUNT_MESSAGE_SUCCESS
        send_mail(
            title, text, settings.EMAIL_HOST_USER, [instance.email], fail_silently=True
        )
    else:
        send_create_user_code(instance.id)
