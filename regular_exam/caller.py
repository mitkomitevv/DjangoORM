import os
import django
from django.db.models import Q, Count, Sum, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Astronaut, Spacecraft, Mission

# Create queries within functions


def get_astronauts(search_string=None):
    if search_string is None:
        return ''

    query = (
        Q(name__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    )

    astronauts = (Astronaut.objects
                  .filter(query)
                  .order_by('name')
                  )

    if not astronauts:
        return ''

    return '\n'.join(f"Astronaut: {a.name}, "
                     f"phone number: {a.phone_number}, "
                     f"status: {'Active' if a.is_active else 'Inactive'}"
                     for a in astronauts)


def get_top_astronaut():
    astronauts = Astronaut.objects.get_astronauts_by_missions_count()

    if not astronauts.exists():
        return "No data."

    top_astronaut = astronauts.first()
    if top_astronaut.mission_count == 0:
        return "No data."

    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.mission_count} missions."


def get_top_commander():
    commanders = (Astronaut.objects
                  .prefetch_related('missions')
                  .annotate(mission_count=Count('missions'))
                  .order_by('-mission_count', 'phone_number')
                  )

    if not commanders.exists():
        return "No data."

    top_commander = commanders.first()
    if top_commander.mission_count == 0:
        return "No data."

    return f"Top Commander: {top_commander.name} with {top_commander.mission_count} commanded missions."


def get_last_completed_mission():
    mission = (Mission.objects
               .select_related('spacecraft', 'commander')
               .prefetch_related('astronauts')
               .annotate(total_spacewalks=Sum('astronauts__spacewalks'))
               .filter(status='Completed')
               .order_by('-launch_date')
               .first()
               )

    if not mission:
        return "No data."

    commander_name = mission.commander.name if mission.commander else 'TBA'
    astronauts = ', '.join(mission.astronauts.values_list('name', flat=True).order_by('name'))

    return (f"The last completed mission is: {mission.name}. "
            f"Commander: {commander_name}. "
            f"Astronauts: {astronauts}. "
            f"Spacecraft: {mission.spacecraft.name}. "
            f"Total spacewalks: {mission.total_spacewalks}.")


def get_most_used_spacecraft():
    spacecraft = (Spacecraft.objects
                  .prefetch_related('missions')
                  .annotate(
                        num_missions=Count('missions', distinct=True),
                        unique_astronauts=Count('missions__astronauts', distinct=True))
                  .order_by('-num_missions', 'name')
                  .first()
                  )

    if not spacecraft or spacecraft.num_missions == 0:
        return "No data."

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.num_missions} missions, "
            f"astronauts on missions: {spacecraft.unique_astronauts}.")


def decrease_spacecrafts_weight():
    spacecrafts = (Spacecraft.objects
                   .prefetch_related('missions')
                   .filter(
                        missions__status='Planned',
                        weight__gte=200.0)
                   .distinct()
                   )

    num_for_update = spacecrafts.count()

    if num_for_update == 0:
        return "No changes in weight."

    spacecrafts.update(weight=F('weight') - 200.0)

    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    return (f"The weight of {num_for_update} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")
