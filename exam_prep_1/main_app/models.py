from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator
from django.db import models

from main_app.choices import MovieGenreChoices
from main_app.managers import DirectorManager
from main_app.mixins import IsAwardedField, LastUpdatedField


# Create your models here.


class BasePerson(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )

    class Meta:
        abstract = True

    birth_date = models.DateField(
        default='1900-01-01'
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )


class Director(BasePerson):
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    objects = DirectorManager()


class Actor(BasePerson, IsAwardedField, LastUpdatedField):
    pass


class Movie(IsAwardedField, LastUpdatedField):
    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)],
    )

    release_date = models.DateField()
    storyline = models.TextField(
        null=True,
        blank=True
    )

    genre = models.CharField(
        max_length=6,
        choices=MovieGenreChoices.choices,
        default=MovieGenreChoices.OTHER
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ],
        default=0.0
    )

    is_classic = models.BooleanField(
        default=False
    )

    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    starring_actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, related_name='movies', null=True, blank=True)
    actors = models.ManyToManyField(Actor, related_name='actor_movies')

