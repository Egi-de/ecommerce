from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    content = models.TextField()  # full blog content
    image = models.ImageField(upload_to="blog_images/")
    created_at = models.DateField(auto_now_add=True)
    read_time = models.CharField(max_length=20, blank=True, null=True)  # e.g. "5min"

    def __str__(self):
        return self.title