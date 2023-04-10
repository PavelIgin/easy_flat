from rest_framework import serializers

from user.models import PasswordChangeOrder


class PasswordChangeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["password"]
        model = PasswordChangeOrder
