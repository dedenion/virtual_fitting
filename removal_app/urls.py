# removal_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 画像処理のためのURLを設定
    path('remove_background/', views.remove_background, name='remove_background'),
    path('classify_image/', views.classify_image, name='classify_image'),  # 新しいビュー関数に修正
    path('process-image/', views.process_image, name='process_image'),  # 新しいビュー関数に修正
    # path('other_endpoint/', views.other_view, name='other_endpoint'),
]
