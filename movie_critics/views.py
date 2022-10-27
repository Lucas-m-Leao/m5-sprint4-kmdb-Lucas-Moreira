from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from movie_critics.models import MovieCritic
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from KMDB.pagination import CustomPageNumberPagination
from movie_critics.permissions import isAdminOrUser
from movie_critics.serializers import LoginSerializers, MovieCriticsSerializers


class ResgisterUser(APIView):
    def post(self, request: Request) -> Response:
        serializers = MovieCriticsSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        return Response(serializers.data, status.HTTP_201_CREATED)


class UserView(APIView, CustomPageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request):
        user = MovieCritic.objects.all()
        result_page = self.paginate_queryset(user, request, view=self)
        serializers = MovieCriticsSerializers(result_page, many=True)

        return self.get_paginated_response(serializers.data)


class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAdminOrUser, IsAuthenticatedOrReadOnly]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(MovieCritic, id=user_id)
        self.check_object_permissions(request, user)
        serializers = MovieCriticsSerializers(user)

        return Response(serializers.data, status.HTTP_200_OK)


class LoginUser(ObtainAuthToken):
    def post(self, request: Request) -> Response:
        serializers = LoginSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        token, _ = Token.objects.get_or_create(user=serializers.validated_data)

        return Response({"token": token.key})
