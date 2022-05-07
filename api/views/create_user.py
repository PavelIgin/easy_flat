import typing

from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import CreateUserSerializers
from user.models import SignUpOrder


class CreateUserViewSet(GenericViewSet, CreateModelMixin):
    """
    ViewSet для заявки на регистрацию. Для активации создан отдельный метод activation.
    """

    queryset: QuerySet = SignUpOrder.objects.get_for_activating()
    serializer_class = CreateUserSerializers
    lookup_field = "uuid"

    @action(detail=True, methods=["POST"])
    def activation(
        self, request: Request, uuid: str, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        order: SignUpOrder = self.get_object()
        data = order.activate()
        return Response(data)
