from rest_framework import serializers

from flat.models import Flat


class FlatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Flat
        read_only_fields = ["owner"]
