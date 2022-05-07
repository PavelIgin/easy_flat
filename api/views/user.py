from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from api.mixins import CreateRatingMixin, ListRatingMixin
from api.permissions import OwnerOrReadOnly
from api.serializers import CustomUserSerializer
from user.models import CustomUser


class CustomUserViewSet(
    CreateRatingMixin,
    ListRatingMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [OwnerOrReadOnly]
