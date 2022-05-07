from rest_framework import serializers

from flat.models import SpecialOffer


class SpecialOfferSerializers(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = SpecialOffer
        read_only_fields = ["flat"]
