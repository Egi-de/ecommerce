from django.contrib import admin

# Register your models here.
from .models import Store
admin.site.register(Store)

# admin.site.register(Store, StoreAdmin)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'distance', 'created_at')
    prepopulated_fields = {'location': ('name',)}
