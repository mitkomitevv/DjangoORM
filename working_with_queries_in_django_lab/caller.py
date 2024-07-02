import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review


def find_books_by_genre_and_language(genre: str, language: str):
    return Book.objects.filter(genre=genre, language=language)


def find_authors_nationalities():
    authors = Author.objects.filter(nationality__isnull=False)

    return '\n'.join(f"{a.first_name} {a.last_name} is {a.nationality}" for a in authors)


def order_books_by_year():
    books = Book.objects.order_by('publication_year', 'title')

    return '\n'.join(f"{b.publication_year} year: {b.title} by {b.author}" for b in books)


def delete_review_by_id(review_id):
    review = Review.objects.get(id=review_id)
    review.delete()

    return f"Review by {review.reviewer_name} was deleted"


def filter_authors_by_nationalities(nationality: str):
    authors = Author.objects.filter(nationality=nationality).order_by('first_name', 'last_name')

    return '\n'.join(a.biography if a.biography else f"{a.first_name} {a.last_name}" for a in authors)


def filter_authors_by_birth_year(birth_year1, birth_year2):
    authors = Author.objects.filter(birth_date__year__range=[birth_year1, birth_year2]).order_by('-birth_date')

    return '\n'.join(f"{a.birth_date}: {a.first_name} {a.last_name}" for a in authors)


def change_reviewer_name(old_name, new_name):
    Review.objects.filter(reviewer_name=old_name).update(reviewer_name=new_name)

    return Review.objects.all()
