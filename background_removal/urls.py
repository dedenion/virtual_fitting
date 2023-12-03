"""
URL configuration for background_removal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('/', TemplateView.as_view(template_name='index.html'), name='home'),  # トップページ用のビューを追加
    path('delete_image/<str:filename>/', views.delete_image, name='delete_image'),
    path('fitting/', views.fitting, name='fitting')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    