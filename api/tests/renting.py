import json
import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import reverse
from psycopg2.extras import DateRange

from flat.models import Renting

from . import ApiTestCase


class RentingTestCase(ApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.renting = Renting.objects.create(
            flat=self.flat,
            user=self.admin_user,
            count_guest=31,
            lease_duration=DateRange(
                lower=datetime.date(year=2012, month=11, day=1), upper=datetime.date(year=2012, month=11, day=10),
                bounds="[)"
            ),
        )

    def test_renting_post(self) -> None:
        url = reverse("rent-list")
        self.authorize(self.admin_user)
        data = {
            "flat": self.flat.id,
            "count_guest": 31,
            "lease_duration": json.dumps(
                {"upper": "2012-12-01", "lower": "2012-11-10", "bounds": "[)"}
            ),
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)

    def test_renting_patch(self) -> None:
        url = reverse("rent-detail", args=(self.renting.id,))
        self.authorize(self.admin_user)
        data = {
            "count_guest": 22,
            "lease_duration": json.dumps(
                {"upper": "2012-12-01", "lower": "2012-11-10", "bounds": "[)"}
            ),
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_renting_delete(self) -> None:
        url = reverse("rent-detail", args=(self.renting.id,))
        self.authorize(self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Renting.objects.filter(id=self.renting.id).exists())

    def test_renting_get(self) -> None:
        url = reverse("rent-detail", args=(self.renting.id,))
        self.authorize(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_renting_list(self) -> None:
        url = reverse("rent-list")
        self.authorize(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_renting_with_exist_renting_in_this_time(self) -> None:
        url = reverse("rent-list")
        self.authorize(self.admin_user)
        data = {
            "flat": self.flat.id,
            "count_guest": 31,
            "lease_duration": json.dumps(
                {"upper": "2012-12-01", "lower": "2012-11-09", "bounds": "[)"}
            ),
        }
        self.assertRaises(ValidationError, self.client.post, path=url, data=data)

    def test_renting_with_too_much_guest(self) -> None:
        url = reverse("rent-list")
        self.authorize(self.admin_user)
        data = {
            "flat": self.flat.id,
            "count_guest": 35,
            "lease_duration": json.dumps(
                {"upper": "2012-10-09", "lower": "2012-10-01", "bounds": "[)"}
            ),
        }
        self.assertRaises(ValidationError, self.client.post, path=url, data=data)

    def test_renting_with_booked_flat(self) -> None:
        url = reverse("rent-list")
        self.authorize(self.quest)
        data = {
            "flat": self.flat.id,
            "count_guest": 31,
            "lease_duration": json.dumps(
                {"upper": "2012-12-01", "lower": "2012-11-09", "bounds": "[)"}
            ),
        }
        self.assertRaises(ValidationError, self.client.post, path=url, data=data)
