# removal_app/models.py

from django.db import models

from cloudinary.models import CloudinaryField

class UserImage(models.Model):
    image = CloudinaryField('image')  # CloudinaryFieldを利用して画像を保存

    class Meta:
        app_label = 'removal_app'  # アプリケーション名を指定