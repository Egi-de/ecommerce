from django.contrib import admin
from .models import Product, Customer, DashboardStats

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'category', 'description']
    list_editable = ['price', 'stock_quantity', 'is_active']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone']
    list_filter = ['created_at']

@admin.register(DashboardStats)
class DashboardStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_earnings', 'daily_earnings', 'new_customers', 'total_customers']
    list_filter = ['date']
    readonly_fields = ['created_at', 'updated_at']
