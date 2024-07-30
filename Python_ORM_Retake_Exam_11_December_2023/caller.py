import os
import django
from django.db.models import Q, Count


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import TennisPlayer, Tournament, Match

# Create queries within functions


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    query = Q()
    if search_name:
        query &= Q(full_name__icontains=search_name)
    if search_country:
        query &= Q(country__icontains=search_country)

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not players.exists():
        return ''

    return '\n'.join(f"Tennis Player: {p.full_name}, "
                     f"country: {p.country}, "
                     f"ranking: {p.ranking}"
                     for p in players)


def get_top_tennis_player():
    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()
    if not player:
        return ''

    return f"Top Tennis Player: {player.full_name} with {player.matches_won} wins."


def get_tennis_player_by_matches_count():
    player = (TennisPlayer.objects
              .annotate(played=Count('matches'))
              .order_by('-played', 'ranking')
              .first()
              )

    if not player or not player.played:
        return ''

    return f"Tennis Player: {player.full_name} with {player.played} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''

    tournaments = (Tournament.objects
                   .prefetch_related('matches')
                   .filter(surface_type__icontains=surface)
                   .annotate(num_matches=Count('matches'))
                   .order_by('-start_date')
                   )

    if not tournaments.exists():
        return ''

    return '\n'.join(f"Tournament: {t.name}, "
                     f"start date: {t.start_date}, "
                     f"matches: {t.num_matches}"
                     for t in tournaments)


def get_latest_match_info():
    match = (Match.objects
             .prefetch_related('players')
             .order_by('-date_played', '-id')
             .first())

    if not match:
        return ''

    players = match.players.order_by('full_name')
    p1 = players.first()
    p2 = players.last()
    winner = 'TBA' if not match.winner else match.winner.full_name

    return (f"Latest match played on: {match.date_played}, tournament: {match.tournament.name}, "
            f"score: {match.score}, players: {p1.full_name} vs {p2.full_name}, "
            f"winner: {winner}, summary: {match.summary}")


def get_matches_by_tournament(tournament_name=None):
    if not tournament_name:
        return "No matches found."

    matches = (Match.objects
               .select_related('tournament', 'winner')
               .filter(tournament__name=tournament_name)
               .order_by('-date_played')
               )

    if not matches:
        return "No matches found."

    return '\n'.join(f"Match played on: {m.date_played}, "
                     f"score: {m.score}, "
                     f"winner: {m.winner.full_name if m.winner else 'TBA'}"
                     for m in matches)
