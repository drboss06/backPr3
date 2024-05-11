from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# class Comment(models.Model):
#     comment = models.TextField()
#     #author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

class Comment(models.Model):
    content = models.TextField()

    def __str__(self):
        return f'{self.content}'

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name}"

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    featured_image = models.ImageField(blank=True, default="default.jpg", upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    comment = models.ManyToManyField(Comment, blank=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name}"
    


