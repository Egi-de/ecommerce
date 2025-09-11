from django.db import models

STATUS_CHOICES = (("published", "published"), ("unpublished", "unpublished"))

class Category(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(
        upload_to="category_icons/",   # folder inside MEDIA_ROOT
        blank=True,
        null=True,
        help_text="Upload a small icon image for this category"
        )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="published")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
