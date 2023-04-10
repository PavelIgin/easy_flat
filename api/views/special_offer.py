from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response

from api.serializers import SpecialOfferSerializers
from api.permissions import OwnerOrReadOnly

from flat.models import SpecialOffer


class SpecialOfferViewSet(CreateModelMixin,
                          RetrieveModelMixin,
                          UpdateModelMixin,
                          DestroyModelMixin,
                          GenericViewSet):
    serializer_class = SpecialOfferSerializers
    queryset = SpecialOffer.objects.all()
    permission_classes = OwnerOrReadOnly

    def list(self, request, *args, **kwargs):
        object_id = self.request.GET["object_id"]
        data = SpecialOffer.objects.filter(id=object_id)
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)
