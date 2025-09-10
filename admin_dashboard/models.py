from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.

class Product(models.Model):
    """Product model for the e-commerce store"""

    # Status choices
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('draft', 'Draft'),
        ('deactive', 'Deactive'),
    ]

    # Category choices
    CATEGORY_CHOICES = [
        ('Dairy, Bread & Eggs', 'Dairy, Bread & Eggs'),
        ('Snacks & Munchies', 'Snacks & Munchies'),
        ('Fruits & Vegetables', 'Fruits & Vegetables'),
        ('Bakery & Biscuits', 'Bakery & Biscuits'),
        ('Instant Food', 'Instant Food'),
        ('Tea, Coffee & Drinks', 'Tea, Coffee & Drinks'),
        ('Atta, Rice & Dal', 'Atta, Rice & Dal'),
        ('Masala, Oil & More', 'Masala, Oil & More'),
        ('Sweet Tooth', 'Sweet Tooth'),
        ('Frozen Veg', 'Frozen Veg'),
        ('Frozen Non-Veg', 'Frozen Non-Veg'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def status_display(self):
        """Return status with proper capitalization"""
        return self.get_status_display()

    @property
    def status_badge_class(self):
        """Return CSS class for status badge"""
        status_classes = {
            'active': 'bg-light-primary text-dark-primary',
            'draft': 'bg-light-warning text-dark-warning',
            'deactive': 'bg-light-danger text-dark-danger',
        }
        return status_classes.get(self.status, 'bg-light-secondary text-dark-secondary')

    class Meta:
        ordering = ['-created_at']

class Customer(models.Model):
    """Customer model extending User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        ordering = ['-created_at']

class DashboardStats(models.Model):
    """Model to store dashboard statistics"""
    date = models.DateField(unique=True)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    daily_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    new_customers = models.IntegerField(default=0)
    total_customers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stats for {self.date}"

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Dashboard Statistics"
