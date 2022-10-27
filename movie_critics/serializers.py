from rest_framework import serializers
from rest_framework.exceptions import APIException
from movie_critics.models import MovieCritic
from django.contrib.auth import authenticate


class UserNotFoundErro(APIException):
    status_code = 404
    default_detail = "Incorrect username or password."
    default_code = "User not found!"


class MovieCriticsSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    birthdate = serializers.DateField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    bio = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        default=None,
    )
    is_critic = serializers.BooleanField(default=False)
    updated_at = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate_username(self, value):
        User_alerady_exists = MovieCritic.objects.filter(
            username=value,
        ).exists()
        if User_alerady_exists:
            raise serializers.ValidationError(
                detail="Username already exists!",
            )
        return value

    def validate_email(self, value):
        Email_alerady_exists = MovieCritic.objects.filter(
            email=value,
        ).exists()
        if Email_alerady_exists:
            raise serializers.ValidationError(
                detail="Email already exists!",
            )
        return value

    def create(self, validated_data):
        user = MovieCritic.objects.create_user(**validated_data)
        return user


class LoginSerializers(serializers.Serializer):

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        users = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        if not users:
            raise UserNotFoundErro
        user = MovieCritic.objects.get(username=username)
        return user
