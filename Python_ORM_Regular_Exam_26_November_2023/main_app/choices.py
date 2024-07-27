from django.db import models


class ArticleChoices(models.TextChoices):
    TECHNOLOGY = 'Technology', 'Technology'
    SCIENCE = 'Science', 'Science'
    EDUCATION = 'Education', 'Education'
