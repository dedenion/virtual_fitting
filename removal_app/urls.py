# removal_app/urls.py

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from . import views
from .views import delete_image
from removal_app import views


urlpatterns = [
    path('/', views.YourTemplateView.as_view(), name='home'),
    path('remove_background/', views.remove_background, name='remove_background'),
    path('image_gallery/', views.image_gallery, name='image_gallery'),
    path('delete_image/<str:filename>/', delete_image, name='delete_image'),
    path('fitting/', views.fitting, name='fitting')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
