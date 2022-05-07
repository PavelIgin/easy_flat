import typing

from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet

from api.serializers import PasswordChangeOrderSerializer
from user.models import PasswordChangeOrder


class PasswordChangeOrderViewSet(CreateModelMixin, GenericViewSet):
    """
    ViewSet для заявки на смену пароля. Для активации создан отдельный метод activation.
    При создани модели пользователь является отправителем заявки при помощи переопределения
    метода perform_create()
    """

    queryset: QuerySet = PasswordChangeOrder.objects.get_for_activating()
    serializer_class = PasswordChangeOrderSerializer
    lookup_field = "uuid"

    def perform_create(self, serializer: ModelSerializer) -> None:
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"])
    def activation(
        self, request: Request, uuid: str, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        order: PasswordChangeOrder = self.get_object()
        data = order.activate()
        return Response(data)
