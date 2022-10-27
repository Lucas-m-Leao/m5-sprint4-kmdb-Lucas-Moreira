from enum import unique
from django.db import models


class RecomendationOptions(models.TextChoices):
    MustWatch = "Must Watch"
    ShouldWatch = "Should Watch"
    AvoidWatch = "Avoid Watch"
    DEFAULT = "No Opinion "


class Reviews(models.Model):
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField(null=True, default=False)
    recomendation = models.CharField(
        max_length=50,
        choices=RecomendationOptions.choices,
        default=RecomendationOptions.DEFAULT,
        null=True,
    )
    critic = models.ForeignKey(
        "movie_critics.MovieCritic",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    movie = models.ForeignKey(
        "movie.Movies",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
