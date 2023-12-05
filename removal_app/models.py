# removal_app/models.py

from django.db import models

from cloudinary.models import CloudinaryField

class UserImage(models.Model):
    name = models.CharField(max_length=10)
    image = models.ImageField(upload_to="user_images/", blank=True)

    class Meta:
        app_label = 'removal_app'  # アプリケーション名を指定