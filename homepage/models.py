from django.db import models
from django.urls import reverse
# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=True)   # e.g. "Groceries, Bakery"
    description = models.TextField(blank=True)
    delivery_type = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    distance = models.CharField(max_length=50, blank=True) 
    logo = models.ImageField(upload_to='stores/logos/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store-detail', kwargs={'slug': self.slug})

    