from django.db import models
from django.db.models import Q


class ProductManager(models.Manager):
    def available_products(self):
        return self.filter(is_available=True)

    def available_products_in_category(self, category_name: str):
        return self.filter(Q(is_available=True) & Q(category__name=category_name))
