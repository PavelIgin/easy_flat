from rest_framework.serializers import ModelSerializer

from user.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "avg_rating"]
