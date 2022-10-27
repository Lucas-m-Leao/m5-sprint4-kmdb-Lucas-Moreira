from django.db import models


class Genres(models.Model):
    name = models.CharField(max_length=127)

    movies = models.ManyToManyField(
        "movie.Movies",
        related_name="genres",
    )
