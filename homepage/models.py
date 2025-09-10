from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)          # e.g. Bakery & Biscuits
    name = models.CharField(max_length=100)           # e.g. NutriChoice Digestive
    weight = models.CharField(max_length=50, blank=True, null=True)  # optional
    price = models.DecimalField(max_digits=10, decimal_places=2)     # better than CharField
    rating = models.FloatField(default=0)             # e.g. 4.5
    reviews = models.IntegerField(default=0)          # e.g. 25

    def __str__(self):
        return self.name
    

class Contact(models.Model):
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.email
    

class Error_404(models.Model):
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.message


class About(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email













