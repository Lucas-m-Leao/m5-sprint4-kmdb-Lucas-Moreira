from rest_framework import serializers
from rest_framework.exceptions import APIException
from movie_critics.serializers import MovieCriticsSerializers

from review.models import Reviews


class UserFoundErro(APIException):
    status_code = 403
    default_detail = "Critic has already done the review!"
    default_code = "Review already has the user!"


class ReviewSerializers(serializers.ModelSerializer):
    critic = MovieCriticsSerializers(read_only=True)

    class Meta:
        model = Reviews
        fields = [
            "id",
            "review",
            "stars",
            "spoilers",
            "recomendation",
            "movie",
            "critic",
        ]
        read_only_fields = [
            "movie",
        ]

    def create(self, validated_data):
        user_already_registered = Reviews.objects.filter(
            critic=validated_data["critic"].id,
            movie=validated_data["movie"].id,
        )
        if user_already_registered:
            raise UserFoundErro

        return Reviews.objects.create(**validated_data)
