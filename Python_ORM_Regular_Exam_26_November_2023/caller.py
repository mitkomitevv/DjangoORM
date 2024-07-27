import os
import django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, Avg, Sum, Value
from django.db.models.functions import Coalesce

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Author, Article, Review


# Create queries within functions


def get_authors(search_name=None, search_email=None):
    if search_name and search_email:
        query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    elif search_name:
        query = Q(full_name__icontains=search_name)
    elif search_email:
        query = Q(email__icontains=search_email)
    else:
        return ''

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors.exists():
        return ''

    return '\n'.join(f"Author: {a.full_name}, email: {a.email}, "
                     f"status: {'Banned' if a.is_banned else 'Not Banned'}"
                     for a in authors)

    # query = Q()
    # if search_name is None and search_email is None:
    #     return ''
    #
    # if search_name:
    #     query &= Q(first_name__icontains=search_name)
    # if search_email:
    #     query &= Q(email__icontains=search_email)
    #
    # authors = Author.objects.filter(query).order_by('-full_name')
    #
    # if not authors.exists():
    #     return ''
    #
    # return '\n'.join(f"Author: {a.full_name}, email: {a.email}, "
    #                  f"status: {'Banned' if a.is_banned else 'Not Banned'}"
    #                  for a in authors)


def get_top_publisher():
    author = Author.objects.annotate(article_count=Count('articles')).order_by('-article_count', 'email').first()

    if not author or author.article_count == 0:
        return ''

    return f"Top Author: {author.full_name} with {author.article_count} published articles."


def get_top_reviewer():
    author = Author.objects.annotate(review_count=Count('reviews')).order_by('-review_count', 'email').first()

    if not author or author.review_count == 0:
        return ''

    return f"Top Reviewer: {author.full_name} with {author.review_count} published reviews."


def get_latest_article():
    article = (Article.objects
               .annotate(
                    review_count=Count('reviews'),
                    avg_rating=Avg('reviews__rating')
               )
               .order_by('-published_on')
               .first()
               )

    if not article:
        return ''

    authors = ', '.join(article.authors.order_by('full_name').values_list('full_name', flat=True))
    avg_rating = article.avg_rating if article.avg_rating is not None else 0.0

    return (f"The latest article is: {article.title}. "
            f"Authors: {authors}. "
            f"Reviewed: {article.review_count} times. Average Rating: {avg_rating:.2f}.")


def get_top_rated_article():
    article = Article.objects.annotate(
        avg_rating=Coalesce(Avg('reviews__rating'), Value(0.0)),
        review_count=Count('reviews')
    ).order_by(
        '-avg_rating',
        'title'
    ).first()

    if not article or not article.review_count:
        return ''

    avg_rating = article.avg_rating if article.avg_rating is not None else 0.0

    return (f"The top-rated article is: {article.title}, "
            f"with an average rating of {avg_rating:.2f}, "
            f"reviewed {article.review_count} times.")


def ban_author(email=None):
    if email is None:
        return 'No authors banned.'

    try:
        author = Author.objects.annotate(review_count=Count('reviews')).get(email__exact=email)
    except ObjectDoesNotExist:
        return 'No authors banned.'

    author.is_banned = True
    author.save()

    author.reviews.all().delete()

    return f"Author: {author.full_name} is banned! {author.review_count} reviews deleted."
