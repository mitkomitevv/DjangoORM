import os
from datetime import date, timedelta

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Author, Book, Artist, Song, Product, Review, Driver, DrivingLicense, Owner, Car, \
    Registration


# Create queries within functions


def show_all_authors_with_their_books():
    authors = Author.objects.all().order_by('id')
    author_books = []

    for author in authors:
        # books = Book.objects.filter(author=author)
        books = author.book_set.all()

        if books:
            author_books.append(f"{author.name} has written - {', '.join(b.title for b in books)}!")

    return '\n'.join(author_books)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)

    return artist.songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()

    average_rating = sum(r.rating for r in reviews) / len(reviews)

    # product = Product.objects.annotate(
    #     average_rating=Avg('reviews__rating'),
    # ).get(name=product_name)

    return average_rating


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    get_products_with_no_reviews().delete()


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')

    return '\n'.join(f"License with number: {l.license_number} expires on "
                     f"{l.issue_date + timedelta(days=365)}!" for l in licenses)


def get_drivers_with_expired_licenses(due_date: date):
    drivers = Driver.objects.all()
    expired = []

    for d in drivers:
        if d.license.issue_date + timedelta(days=365) > due_date:
            expired.append(d)

    # expiration_cutoff_date = due_date - timedelta(days=365)
    #
    # drivers_with_expired_licenses = Driver.objects.filter(
    #     license__issue_date__gt=expiration_cutoff_date,
    # )

    return expired


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.owner = owner

    car.save()

    registration.registration_date = date.today()
    registration.car = car

    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

