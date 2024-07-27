from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from main_app.choices import ArticleChoices
from main_app.managers import AuthorsArticleCountManager


# Create your models here.


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
        ],
    )

    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005)
        ],
    )

    website = models.URLField(null=True, blank=True)

    objects = AuthorsArticleCountManager()


class Article(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)],
    )

    content = models.TextField(
        validators=[MinLengthValidator(10)],
    )

    category = models.CharField(
        max_length=10,
        choices=ArticleChoices.choices,
        default=ArticleChoices.TECHNOLOGY
    )

    authors = models.ManyToManyField(Author, related_name='articles')

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )


class Review(models.Model):
    content = models.TextField(
        validators=[MinLengthValidator(10)],
    )

    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0),
        ]
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='reviews')

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')

    published_on = models.DateTimeField(auto_now_add=True, editable=False)
