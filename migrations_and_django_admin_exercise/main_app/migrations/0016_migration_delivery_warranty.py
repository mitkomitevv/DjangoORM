# Generated by Django 5.0.4 on 2024-06-26 11:01

from django.db import migrations
from django.utils import timezone


def set_delivery_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')
    orders_to_update = []

    for order in order_model.objects.all():
        if order.status == 'Pending':
            order.delivery = order.order_date + timezone.timedelta(days=3)
            orders_to_update.append(order)
        elif order.status == 'Completed':
            order.warranty = '24 months'
            orders_to_update.append(order)
        elif order.status == 'Cancelled':
            order.delete()

    order_model.objects.bulk_update(orders_to_update, ['delivery', 'warranty'])


def reverse_delivery_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')
    orders_to_update = []

    for order in order_model.objects.all():
        if order.status == "Pending":
            order.delivery = None
        elif order.status == "Completed":
            order.warranty = order_model._meta.get_field('warranty').default

        orders_to_update.append(order)

    order_model.objects.bulk_update(orders_to_update, ['delivery', 'warranty'])


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_order'),
    ]

    operations = [
        migrations.RunPython(set_delivery_warranty, reverse_delivery_warranty)
    ]
