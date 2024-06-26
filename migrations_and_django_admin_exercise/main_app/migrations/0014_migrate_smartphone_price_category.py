from django.db import migrations


def assign_price(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')
    multiplier = 120
    smartphones_to_update = []

    for smartphone in smartphone_model.objects.all():
        smartphone.price = multiplier * len(smartphone.brand)
        smartphones_to_update.append(smartphone)

    smartphone_model.objects.bulk_update(smartphones_to_update, ['price'])


def assign_category(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')
    smartphones_to_update = []

    for smartphone in smartphone_model.objects.all():
        if smartphone.price >= 750:
            smartphone.category = 'Expensive'
        else:
            smartphone.category = 'Cheap'
        smartphones_to_update.append(smartphone)

    smartphone_model.objects.bulk_update(smartphones_to_update, ['category'])


def reverse_price_category(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')
    default_price = smartphone_model._meta.get_field('price').default
    default_category = smartphone_model._meta.get_field('category').default
    smartphones_to_update = []

    for smartphone in smartphone_model.objects.all():
        smartphone.price = default_price
        smartphone.category = default_category
        smartphones_to_update.append(smartphone)

    smartphone_model.objects.bulk_update(smartphones_to_update, ['price', 'category'])


def apply_assigns(apps, schema_editor):
    assign_price(apps, schema_editor)
    assign_category(apps, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_smartphone'),
    ]

    operations = [
        migrations.RunPython(apply_assigns, reverse_price_category)
    ]
