from django.db import models
from django.db.models import Count


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return (self.prefetch_related('orders')
                .annotate(num_orders=Count('orders'))
                .filter(num_orders__gt=2)
                .order_by('-num_orders'))
