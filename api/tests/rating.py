from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse

from community.models import Rating

from . import ApiTestCase


class RatingTestCase(ApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.rating = Rating.objects.create(
            object_id=self.flat.id,
            rating_star=Rating.RatingStar.Two,
            user=self.admin_user,
            content_type=ContentType.objects.get_for_model(self.flat),
        )

    def test_rating_get(self) -> None:
        url = reverse("rating-detail", args=(self.rating.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_rating_patch(self) -> None:
        url = reverse("rating-detail", args=(self.rating.id,))
        self.authorize(self.admin_user)
        data = {"rating_star": Rating.RatingStar.Four}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
