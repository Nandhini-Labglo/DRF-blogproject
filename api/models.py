from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Post(models.Model):

    slug = models.SlugField(null=True)
    title = models.CharField(max_length=100,)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ImageField(upload_to='media', blank=True, )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at", "-updated_at"]


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ["-created_at", "-updated_at"]
