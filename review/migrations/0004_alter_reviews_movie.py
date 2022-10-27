# Generated by Django 4.1.2 on 2022-10-27 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0001_initial"),
        ("review", "0003_alter_reviews_critic_alter_reviews_movie"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviews",
            name="movie",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="movie.movies",
                unique=True,
            ),
        ),
    ]