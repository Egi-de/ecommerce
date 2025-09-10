from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random
from admin_dashboard.models import Product, Customer, DashboardStats

class Command(BaseCommand):
    help = 'Populate sample data for dashboard'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample products
        products_data = [
            {'name': 'Fresh Apples', 'category': 'Fruits', 'price': 4.99, 'stock': 150},
            {'name': 'Organic Bananas', 'category': 'Fruits', 'price': 2.99, 'stock': 200},
            {'name': 'Fresh Broccoli', 'category': 'Vegetables', 'price': 3.49, 'stock': 80},
            {'name': 'Carrots', 'category': 'Vegetables', 'price': 1.99, 'stock': 120},
            {'name': 'Whole Milk', 'category': 'Dairy', 'price': 3.99, 'stock': 50},
            {'name': 'Greek Yogurt', 'category': 'Dairy', 'price': 5.99, 'stock': 75},
            {'name': 'Chicken Breast', 'category': 'Meat', 'price': 8.99, 'stock': 40},
            {'name': 'Salmon Fillet', 'category': 'Seafood', 'price': 12.99, 'stock': 25},
        ]
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'description': f"Fresh {product_data['name'].lower()} from local farms",
                    'category': product_data['category'],
                    'price': product_data['price'],
                    'stock_quantity': product_data['stock'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        # Create sample customers
        customers_data = [
            {'username': 'john_doe', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'},
            {'username': 'jane_smith', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com'},
            {'username': 'mike_wilson', 'first_name': 'Mike', 'last_name': 'Wilson', 'email': 'mike@example.com'},
            {'username': 'sarah_brown', 'first_name': 'Sarah', 'last_name': 'Brown', 'email': 'sarah@example.com'},
            {'username': 'david_jones', 'first_name': 'David', 'last_name': 'Jones', 'email': 'david@example.com'},
        ]
        
        for customer_data in customers_data:
            user, user_created = User.objects.get_or_create(
                username=customer_data['username'],
                defaults={
                    'first_name': customer_data['first_name'],
                    'last_name': customer_data['last_name'],
                    'email': customer_data['email'],
                }
            )
            if user_created:
                customer, created = Customer.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone': f'+1-555-{random.randint(1000, 9999)}',
                        'address': f'{random.randint(100, 999)} Main St, City, State'
                    }
                )
                if created:
                    self.stdout.write(f'Created customer: {customer}')
        
        # Create sample dashboard stats for the last 30 days
        today = timezone.now().date()
        for i in range(30):
            date = today - timedelta(days=i)
            daily_earnings = random.uniform(1000, 5000)
            new_customers = random.randint(0, 10)
            
            stats, created = DashboardStats.objects.get_or_create(
                date=date,
                defaults={
                    'daily_earnings': daily_earnings,
                    'total_earnings': daily_earnings * (i + 1),  # Cumulative
                    'new_customers': new_customers,
                    'total_customers': Customer.objects.count() + new_customers
                }
            )
            if created:
                self.stdout.write(f'Created stats for {date}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample data!')
        )
