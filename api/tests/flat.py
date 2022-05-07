from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.shortcuts import reverse

from community.models import Rating
from flat.models import Flat

from . import ApiTestCase


class FlatTestCase(ApiTestCase):
    booked_days_after = "2012-12-1"
    booked_days_before = "2012-12-12"

    def setUp(self) -> None:
        super().setUp()

    def test_flat_post(self) -> None:
        url = reverse("flat-list")
        data = {
            "rooms_count": 3,
            "cost": 2332,
            "max_guest": 32,
            "arena_timeline": "OneDay",
            "total_area": 23,
        }
        self.authorize(self.admin_user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    def test_flat_list(self) -> None:
        url = reverse("flat-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_flat_get(self) -> None:
        url = reverse("flat-detail", args=(self.flat.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_flat_filter(self) -> None:
        url = reverse("flat-list")
        data = {
            "cost_min": 12,
            "cost_max": 10000,
            "rooms_count_min": 2,
            "rooms_count_max": 4,
            "total_area_min": 12,
            "total_area_max": 40,
            "max_guest_min": 12,
            "max_guest_max": 15,
            "arena_timeline": "OneDay",
            "booked_days_after": self.booked_days_after,
            "booked_days_before": self.booked_days_before,
            "order_by": "-cost",
        }
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_flat_filter_with_incorrect_date(self) -> None:
        url = reverse("flat-list")
        data = {
            "booked_days_after": self.booked_days_before,
            "booked_days_before": self.booked_days_after,
        }
        self.assertRaises(ValidationError, self.client.get, path=url, data=data)

    def test_flat_patch(self) -> None:
        url = reverse("flat-detail", args=(self.flat.id,))
        data = {
            "rooms_count": 3422,
            "cost": 54353,
            "max_guest": 3122,
            "arena_timeline": "OneDay",
            "total_area": 2432,
        }
        self.authorize(self.admin_user)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_flat_delete(self) -> None:
        url = reverse("flat-detail", args=(self.flat.id,))
        self.authorize(self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Flat.objects.filter(id=self.flat.id).exists())

    def test_flat_create_rating(self) -> None:
        url = reverse("flat-create-rating", args=(self.flat.id,))
        self.authorize(self.admin_user)
        data = {"rating_star": Rating.RatingStar.Four}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_flat_list_rating(self) -> None:
        url = reverse("flat-list-rating", args=(self.flat.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)

    def test_flat_create_rating_with_already_exist(self) -> None:
        Rating.objects.create(
            object_id=self.flat.id,
            rating_star=Rating.RatingStar.Two,
            user=self.admin_user,
            content_type=ContentType.objects.get_for_model(self.flat),
        )
        url = reverse("flat-create-rating", args=(self.flat.id,))
        data = {"rating_star": Rating.RatingStar.Four}
        self.authorize(self.admin_user)
        self.assertRaises(ValidationError, self.client.post, path=url, data=data)
