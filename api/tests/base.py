from django.test import TestCase
from rest_framework.test import APITestCase

from flat.models import Flat
from user.models import CustomUser
from user.service import create_token


class ApiTestCase(APITestCase, TestCase):
    first_password = "123"

    def setUp(self) -> None:
        super().setUp()
        self.admin_user = CustomUser.objects.create(
            username="admin",
            email="test_mail@gmail.com",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        self.admin_user.set_password(self.first_password)
        self.admin_user.save()

        self.quest = CustomUser.objects.create(
            username="quest",
            password=self.first_password,
            email="test_mail_quest@gmail.com",
            is_active=True,
            is_staff=True,
            is_superuser=False,
        )
        self.quest.set_password(self.first_password)
        self.quest.save()
        self.flat = Flat.objects.create(
            rooms_count=3,
            cost=2332,
            max_guest=32,
            arena_timeline="OneDay",
            total_area=23,
            owner=self.admin_user,
        )
        self.flat_two = Flat.objects.create(
            rooms_count=3,
            cost=2332,
            max_guest=14,
            arena_timeline="OneDay",
            total_area=23,
            owner=self.admin_user,
        )

    def authorize(self, user: CustomUser) -> None:
        token = create_token(user)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)
