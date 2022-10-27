from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authentication import TokenAuthentication
from KMDB.pagination import CustomPageNumberPagination

from movie.permissions import MoviAdmPermission

from .models import Movies
from .serializers import MovieSerializer


class MoviesView(APIView, CustomPageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [MoviAdmPermission]

    def post(self, request: Request) -> Response:
        serializers = MovieSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        return Response(serializers.data, status.HTTP_201_CREATED)

    def get(self, request: Request):

        movie = Movies.objects.all()
        result_page = self.paginate_queryset(movie, request, view=self)
        serializers = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(serializers.data)


class MoviesDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [MoviAdmPermission]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movies, id=movie_id)
        serializers = MovieSerializer(movie)
        return Response(serializers.data, status.HTTP_200_OK)

    def patch(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movies, id=movie_id)
        serializers = MovieSerializer(movie, request.data, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: id) -> Response:
        movie = get_object_or_404(Movies, id=movie_id)
        movie.delete()
        return Response("", status.HTTP_200_OK)
