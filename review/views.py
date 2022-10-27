from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, Request, status
from KMDB.pagination import CustomPageNumberPagination
from movie.models import Movies
from rest_framework.authentication import TokenAuthentication
from review.models import Reviews
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from review.permissions import ReviewAdmPermission, isReviewAdminOrUser
from review.serializers import ReviewSerializers


class ReviewView(APIView, CustomPageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewAdmPermission]

    def post(self, request: Request, movie_id) -> Response:
        movie = get_object_or_404(Movies, id=movie_id)
        serializers = ReviewSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(critic=request.user, movie=movie)

        return Response(serializers.data, status.HTTP_201_CREATED)

    def get(self, request: Request, movie_id):
        review = Reviews.objects.filter(movie=movie_id)
        if not review:
            return Response(
                {"message": "Invalid movie_id!"},
                status.HTTP_404_NOT_FOUND,
            )
        result_page = self.paginate_queryset(review, request, view=self)
        serializers = ReviewSerializers(result_page, many=True)
        return self.get_paginated_response(serializers.data)


class ReviewDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isReviewAdminOrUser, IsAuthenticatedOrReadOnly]

    def get(self, request: Request, review_id, movie_id) -> Response:
        review = Reviews.objects.filter(id=review_id, movie=movie_id)
        if not review:
            return Response(
                {"message": "Invalid movie_id or review_id "},
                status.HTTP_404_NOT_FOUND,
            )
        serializers = ReviewSerializers(review, many=True)
        return Response(serializers.data)

    def delete(self, request: Request, review_id, movie_id) -> Response:
        review = Reviews.objects.filter(id=review_id, movie=movie_id)
        if not review:
            return Response(
                {"message": "Invalid movie_id or review_id "},
                status.HTTP_404_NOT_FOUND,
            )
        self.check_object_permissions(request, review)
        review.delete()
        return Response("", status.HTTP_200_OK)
