from rest_framework import serializers

from flat.models import Renting


class RentSerializer(serializers.ModelSerializer):
    """
    Сериализатор сущности аренды
    """

    class Meta:
        model = Renting
        fields = ["flat", "count_guest", "lease_duration"]
