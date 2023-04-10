import datetime
from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.shortcuts import reverse

from api.tests import ApiTestCase
from user.models import PasswordChangeOrder

from .mock import MockSMTPSSLSuccess


class ChangePasswordTestCase(ApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.password_change_order = PasswordChangeOrder.objects.create(
            user=self.admin_user, password="mega_password123"
        )
        self.password_change_order.save()

    @patch("user.models.change_password.now")
    def test_reset_password_expire_token(self, now: MagicMock) -> None:
        now.return_value = datetime.datetime.now(
            tz=datetime.timezone.utc
        ) + datetime.timedelta(minutes=11)
        data = {"uuid": self.password_change_order.uuid}
        url = reverse("change_password-activation", kwargs=data)
        self.assertRaises(ValidationError, self.client.post, path=url, data=data)

    @patch("django.core.mail.send_mail")
    def test_reset_password(self, send_mail: MagicMock) -> None:
        url = reverse("change_password-list")
        self.authorize(self.quest)
        send_mail.return_value = MockSMTPSSLSuccess()
        data = {"password": self.first_password}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    @patch("django.core.mail.send_mail")
    def test_reset_password_activation(self, send_mail: MagicMock) -> None:
        data = {"uuid": self.password_change_order.uuid}
        url = reverse("change_password-activation", kwargs=data)
        send_mail.return_value = MockSMTPSSLSuccess()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.admin_user.refresh_from_db()
        self.assertTrue(
            self.admin_user.check_password(self.password_change_order.password)
        )
