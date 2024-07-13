import os
import django
from django.db.models import Sum, F, Q

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models

from main_app.models import Product, Category, Customer, Order, OrderProduct

# Create and run queries


def product_quantity_ordered():
    total_products = Product.objects.annotate(
        total=Sum('orderproduct__quantity')
    ).exclude(total=None).order_by('-total')

    return '\n'.join(f"Quantity ordered of {tp.name}: {tp.total}" for tp in total_products)


def ordered_products_per_customer():
    orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')
    result = []

    for order in orders:
        result.append(F"Order ID: {order.id}, Customer: {order.customer.username}")
        for o in order.orderproduct_set.all():
            result.append(f"- Product: {o.product.name}, Category: {o.product.category.name}")

    return '\n'.join(result)


def filter_products():
    query = Q(is_available=True) & Q(price__gt=3.00)
    products = Product.objects.filter(query).order_by('-price', 'name')

    return '\n'.join(f"{p.name}: {p.price}lv." for p in products)


def give_discount():
    query = Q(is_available=True) & Q(price__gt=3.00)
    Product.objects.filter(query).update(price=F('price') * 0.70)
    products = Product.objects.filter(is_available=True).order_by('-price', 'name')

    return '\n'.join(f"{p.name}: {p.price}lv." for p in products)
