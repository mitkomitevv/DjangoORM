import os
import django
from django.db.models import Q, Count, Avg, Max, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Director, Actor, Movie

# Create queries within functions


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    query = Q()
    if search_name is not None:
        query &= Q(full_name__icontains=search_name)
    if search_nationality is not None:
        query &= Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    return '\n'.join(f"Director: {d.full_name}, "
                     f"nationality: {d.nationality}, "
                     f"experience: {d.years_of_experience}"
                     for d in directors)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()
    if not director:
        return ''

    return f"Top Director: {director.full_name}, movies: {director.num_movies}."


def get_top_actor():
    actor = (Actor.objects
             .prefetch_related('movies')
             .annotate(
                 num_movies=Count('movies'),
                 avg_rating=Avg('movies__rating')
             )
             .order_by('-num_movies', 'full_name')
             .first()
             )

    if not actor:
        return ''

    movies = ', '.join(actor.movies.values_list('title', flat=True))

    if not movies:
        return ''

    avg_rating = actor.avg_rating if actor.avg_rating is not None else 0.0

    return (f"Top Actor: {actor.full_name}, "
            f"starring in movies: {movies}, "
            f"movies average rating: {avg_rating:.1f}")


def get_actors_by_movies_count():
    actors = (Actor.objects
              .prefetch_related('movies')
              .annotate(num_movies=Count('actor_movies'))
              .order_by('-num_movies', 'full_name'))[:3]

    if not actors or not actors[0].num_movies:
        return ''

    return '\n'.join(f"{a.full_name}, "
                     f"participated in {a.num_movies} movies"
                     for a in actors)


def get_top_rated_awarded_movie():
    movie = (Movie.objects
             .select_related('starring_actor')
             .prefetch_related('actors')
             .filter(is_awarded=True)
             .order_by('-rating', 'title')
             .first())

    if movie is None:
        return ''

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else 'N/A'
    actors = ', '.join(movie.actors.values_list('full_name', flat=True).order_by('full_name'))

    return (f"Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. "
            f"Starring actor: {starring_actor}. Cast: {actors}.")


def increase_rating():
    updated_movies = (Movie.objects.
                      filter(is_classic=True, rating__lt=10.0)
                      .update(rating=F('rating') + 0.1))

    if not updated_movies:
        return "No ratings increased."

    return f"Rating increased for {updated_movies} movies."
