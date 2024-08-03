import os
import django
from django.db.models import Q, Count, F, Case, When, Value, BooleanField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Profile, Product, Order


# Create queries within functions


def get_profiles(search_string=None):
    if search_string is None:
        return ''

    query = (
            Q(full_name__icontains=search_string)
            |
            Q(email__icontains=search_string)
            |
            Q(phone_number__icontains=search_string)
    )

    profiles = (Profile.objects
                .prefetch_related('orders')
                .annotate(num_orders=Count('orders'))
                .filter(query)
                .order_by('full_name'))

    if not profiles:
        return ''

    return '\n'.join(f"Profile: {p.full_name}, "
                     f"email: {p.email}, "
                     f"phone number: {p.phone_number}, "
                     f"orders: {p.num_orders}"
                     for p in profiles)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ''

    return '\n'.join(f"Profile: {p.full_name}, "
                     f"orders: {p.num_orders}"
                     for p in profiles)


def get_last_sold_products():
    order = Order.objects.prefetch_related('products').last()

    if order is None or not order.products.exists():
        return ''

    products = ', '.join(order.products.order_by('name').values_list('name', flat=True))

    return f"Last sold products: {products}"


def get_top_products():
    products = (Product.objects
                .annotate(sold=Count('orders'))
                .filter(sold__gt=0)
                .order_by('-sold', 'name'))[:5]

    if not products:
        return ''

    top_products = '\n'.join(f"{p.name}, sold {p.sold} times" for p in products)

    return f"Top products:\n{top_products}"


def apply_discounts():
    orders = (Order.objects
              .prefetch_related('products')
              .annotate(num_products=Count('products'))
              .filter(num_products__gt=2, is_completed=False)
              .update(total_price=F('total_price') * 0.9))

    return f"Discount applied to {orders} orders."


def complete_order():
    order_to_update = (Order.objects
                       .prefetch_related('products')
                       .filter(is_completed=False)
                       .order_by('creation_date')
                       .first())

    if not order_to_update:
        return ''

    order_to_update.products.update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available'),
            output_type=BooleanField()
        )
    )

    order_to_update.is_completed = True
    order_to_update.save()

    return "Order has been completed!"
