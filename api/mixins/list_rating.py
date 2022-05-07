import typing

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import RatingSerializer


class ListRatingMixin:
    @action(detail=True, methods=["GET"], url_path="list_rating")
    def list_rating(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        model_name: Model = ContentType.objects.get_for_model(
            request.parser_context["view"].queryset.model
        )
        object_id = kwargs["pk"]
        data = model_name.rating.filter(object_id=object_id, content_type=model_name)
        serializer = RatingSerializer(data, many=True)
        return Response(serializer.data)
