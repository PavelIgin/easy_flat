from django.shortcuts import reverse

from community.models import Rating
from user.models import CustomUser

from . import ApiTestCase


class UserTestCase(ApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = CustomUser.objects.create_user(username="qweqwe", password="123123")

    def test_user_create_rating(self) -> None:
        url = reverse("user-create-rating", args=(self.user.id,))
        self.authorize(self.admin_user)
        data = {"rating_star": Rating.RatingStar.Free}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(
            self.user.rating.get(
                rating_star=Rating.RatingStar.Free,
                object_id=self.user.id,
                content_type=self.user.rating.content_type,
            )
        )

    def test_user_list_rating(self) -> None:
        url = reverse("user-list-rating", args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)

    def test_user_delete(self) -> None:
        url = reverse("user-detail", args=(self.user.id,))
        self.authorize(self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.authorize(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_user_update(self) -> None:
        url = reverse("user-detail", args=(self.user.id,))
        self.authorize(self.user)
        data = {"last_name": "qqqwww"}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
