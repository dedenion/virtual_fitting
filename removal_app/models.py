# removal_app/models.py

from django.db import models

class UserImage(models.Model):
    image = models.ImageField(upload_to='user_images/')

    class Meta:
        app_label = 'removal_app'  # アプリケーション名を指定

