from rest_framework import serializers

from user.models import SignUpOrder


class CreateUserSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ["email", "username", "password"]
        model = SignUpOrder
