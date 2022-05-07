from rest_framework import serializers

from community.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """
    Сериализатор рейтинга
    """

    class Meta:
        model = Rating
        fields = ["rating_star", "user", "object_id", "content_type"]
        read_only_fields = ["user"]
