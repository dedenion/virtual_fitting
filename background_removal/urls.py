
# background_removal/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from removal_app import views  # 追加



urlpatterns = [
    path('admin/', admin.site.urls),
    path('remove_background/', include('removal_app.urls')),
    path('image_gallery/', views.image_gallery, name='image_gallery'),  # image_galleryのパスを追加
    path('', TemplateView.as_view(template_name='index.html'), name='home'),  # トップページ用のビューを追加
    path('delete_image/<str:filename>/', views.delete_image, name='delete_image'),
    path('fitting/', views.fitting, name='fitting')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    