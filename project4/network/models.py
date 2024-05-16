from django.contrib.auth.models import AbstractUser
from django.db import models

from django import forms

from django.contrib.auth import get_user_model

class User(AbstractUser):
    pass


class Following(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('user', 'followed_user')


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username}: {self.content[:50]}"
