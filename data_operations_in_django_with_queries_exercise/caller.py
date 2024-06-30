import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(
        name=name,
        species=species,
    )

    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    # Artifact.objects.first(is_magcal=True, age__gt=250).update(name=new_name)  # Updates All

    # Artifact.objects.first(is_magcal=True, age__gt=250, pk=artifact.pk).update(name=new_name)
    # Both are the same
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    locations = Location.objects.all().order_by('-id')

    return '\n'.join(f"{l.name} has a population of {l.population}!" for l in locations)


def new_capital():
    # Not a good way
    # Location.objects.filter(id=1).update(is_capital=True)

    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        discount = float(car.price) - (float(car.price) * (sum(int(n) for n in str(car.year)) / 100))
        car.price_with_discount = discount

    cars.bulk_update(cars, ['price_with_discount'])  # 1


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    return '\n'.join(str(t) for t in Task.objects.filter(is_finished=False))


def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 != 0:
            task.is_finished = True

    tasks.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str):
    text_to_replace = ''.join(chr(ord(l) - 3) for l in text)

    Task.objects.filter(title=task_title).update(description=text_to_replace)


def get_deluxe_rooms():
    even_deluxe_rooms = [str(r) for r in HotelRoom.objects.filter(room_type='Deluxe') if r.id % 2 == 0]

    return '\n'.join(even_deluxe_rooms)


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')

    prev_room_capacity = None
    for room in rooms:
        if not room.is_reserved:
            continue

        if prev_room_capacity is None:
            room.capacity += room.id
        else:
            room.capacity += prev_room_capacity

        prev_room_capacity = room.capacity

    rooms.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room():
    room = HotelRoom.objects.last()

    if not room.is_reserved:
        room.delete()


def update_characters():
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7,
    )

    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        intelligence=F('dexterity') + 4,
    )

    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory='The inventory is empty'
    )


def fuse_characters(first_character: Character, second_character: Character):
    new_name = f'{first_character.name} {second_character.name}'
    new_class_name = 'Fusion'
    new_level = (first_character.level + second_character.level) // 2
    new_strength = (first_character.strength + second_character.strength) * 1.2
    new_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    new_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    new_hit_points = first_character.hit_points + second_character.hit_points

    if first_character.class_name in ["Mage", "Scout"]:
        new_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        new_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=new_name,
        class_name=new_class_name,
        level=new_level,
        strength=new_strength,
        dexterity=new_dexterity,
        intelligence=new_intelligence,
        hit_points=new_hit_points,
        inventory=new_inventory,
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()
