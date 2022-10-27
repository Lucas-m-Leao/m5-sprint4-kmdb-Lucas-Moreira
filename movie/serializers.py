from genre.serializers import GenreSerializers
from rest_framework import serializers
from genre.models import Genres
from movie.models import Movies


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()
    genres = GenreSerializers(many=True)

    def create(self, validated_data):
        genre = validated_data.pop("genres")
        movie = Movies.objects.create(**validated_data)
        for key in genre:
            genre_instace = Genres.objects.get_or_create(**key)
            genre_instace[0].movies.add(movie)

        return movie

    def update(self, instance, validated_data):
        instance.genres.clear()
        genres = validated_data.pop("genres")
        for key, value in validated_data.items():
            setattr(instance, key, value)
        for value in genres:
            genre = Genres.objects.get_or_create(**value)

            instance.genres.add(genre[0])
            instance.save()

        return instance
