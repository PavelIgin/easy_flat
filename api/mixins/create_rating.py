import typing

from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from community.models import Rating


class CreateRatingMixin:
    @action(detail=True, methods=["POST"], url_name="create-rating")
    def create_rating(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        object_id: int = kwargs["pk"]
        content_type = ContentType.objects.get_for_model(
            model=request.parser_context["view"].queryset.model
        )
        rating_star = request.data["rating_star"]
        user = request.user
        rating = Rating(
            rating_star=rating_star,
            user=user,
            object_id=object_id,
            content_type=content_type,
        )
        rating.save()
        return Response({"status": 200})
