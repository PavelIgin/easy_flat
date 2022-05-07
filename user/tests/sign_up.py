import datetime
from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.shortcuts import reverse

from api.tests import ApiTestCase
from user.models import SignUpOrder
from user.service import create_token

from . import MockSMTPSSLSuccess


class SignUpTestCase(ApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.sing_up_order = SignUpOrder.objects.create(
            username="qwerty", password="123445", email="test_sing_up@gmail.com"
        )
        self.sing_up_order.save()

    @patch("django.core.mail.send_mail")
    def test_sign_up_order(self, send_mail: MagicMock) -> None:
        url = reverse("create_user-list")
        data = {
            "username": "qwerty",
            "password": "123456",
            "email": "test_sign_up_order@gmail.com",
        }
        send_mail.return_value = MockSMTPSSLSuccess()
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    def test_sign_up_order_on_block_mail(self) -> None:
        url = reverse("create_user-list")
        data = {
            "username": "qwerty",
            "password": "123456",
            "email": "test_mail@gmail.com",
        }
        self.assertRaises(ValidationError, self.client.post, path=url, data=data)

    def test_sign_up_activation(self) -> None:
        data = {"uuid": self.sing_up_order.uuid}
        url = reverse("create_user-activation", kwargs=data)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    @patch("user.models.sign_up.now")
    def test_sing_up_expire_token(self, now: MagicMock) -> None:
        now.return_value = datetime.datetime.now(
            tz=datetime.timezone.utc
        ) + datetime.timedelta(minutes=11)
        data = {"uuid": self.sing_up_order.uuid}
        url = reverse("create_user-activation", kwargs=data)
        self.assertRaises(ValidationError, self.client.post, path=url, data=data)

    def test_create_token(self) -> None:
        create_token(self.admin_user)
