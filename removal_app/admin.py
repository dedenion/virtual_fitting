# removal_app/admin.py

from django.contrib import admin
from .models import UserImage

@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']
    search_fields = ['id']  # 必要に応じて検索フィールドを追加

    class Meta:
        model = UserImage
