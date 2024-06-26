# Generated by Django 5.0.4 on 2024-06-26 09:59

from django.db import migrations


def assign_rarity(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')
    items_to_update = []

    for item in item_model.objects.all():
        if item.price <= 10:
            item.rarity = 'Rare'
        elif item.price <= 20:
            item.rarity = 'Very Rare'
        elif item.price <= 30:
            item.rarity = 'Extremely Rare'
        else:
            item.rarity = 'Mega Rare'

        items_to_update.append(item)

    item_model.objects.bulk_update(items_to_update, ['rarity'])


def reverse_rarity(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')
    items_to_update = []

    default_rarity = item_model._meta.get_field('rarity').default

    for item in item_model.objects.all():
        item.rarity = default_rarity
        items_to_update.append(item)

    item_model.objects.bulk_update(items_to_update, ['rarity'])


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_item'),
    ]

    operations = [
        migrations.RunPython(assign_rarity, reverse_rarity)
    ]
