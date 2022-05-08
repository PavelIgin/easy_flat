import typing

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import SpecialOfferSerializers

from flat.models import SpecialOffer


class ListSpecialOfferMixin:
    @action(detail=True, methods=["GET"], url_path="list_special_offer")
    def list_special_offer(
            self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        object_id = kwargs['pk']
        data = SpecialOffer.objects.filter(flat=object_id)
        serializer = SpecialOfferSerializers(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)
