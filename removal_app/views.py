# removal_app/views.py
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import uuid
import rembg
import base64
from PIL import Image, ImageOps
import io
from tensorflow.keras.models import load_model
import numpy as np
from django import template

from celery.result import AsyncResult

class YourTemplateView(TemplateView):
    template_name = 'index.html'
from .tasks import process_and_remove_background, classify_image




from django.core.files.base import ContentFile


# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()


def remove_background(request):
    output_image_data = None

    fs_gallery = FileSystemStorage(location=settings.MEDIA_ROOT)
    class_name = None
    confidence_score = None

    if 'output_image_path' in request.session:
        del request.session['output_image_path']

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            image_data = form.cleaned_data['image'].file.read()
            
            processed_image_task = process_and_remove_background.delay(image_data)
            classify_image.delay(processed_image_task.get(), form.cleaned_data['image'].name)

            processed_image = processed_image_task.get()
            class_name, confidence_score, _ = classify_image(processed_image, form.cleaned_data['image'].name)

            image_filename = generate_filename({"class_name": class_name}, form.cleaned_data['image'].name, class_name)

            output_image_data = base64.b64decode(processed_image)

            request.session['output_image_path'] = fs_gallery.url(image_filename)

    else:
        form = ImageUploadForm()

    if output_image_data:
        return HttpResponse(output_image_data, content_type='image/png')

    return render(request, 'remove_background.html', {'form': form, 'output_image_path': request.session.get('output_image_path'), 'class_name': class_name, 'confidence_score': confidence_score})






def process_image(image):
    # 縦横の幅が広い方を取得
    max_size = max(image.size)

    # 正方形に切り取り
    new_image = image.crop((0, 0, max_size, max_size))

    # 切り取った画像をバイト型に変換
    output_image = io.BytesIO()
    new_image.save(output_image, format='PNG')
    processed_image = output_image.getvalue()

    return processed_image





from django.contrib.staticfiles.storage import staticfiles_storage
# ...
register = template.Library()
@register.filter(name='filename_from_image')
def filename_from_image(value):
    return value.split('/')[-1]

# ...

def image_gallery(request):
    gallery_dir = settings.MEDIA_ROOT  # メディアフォルダのパス

    images = {'tops': [], 'pants': []}

    for image in os.listdir(gallery_dir):
        image_path = os.path.join(settings.MEDIA_URL, image)
        
        if 'tops' in image:
            images['tops'].append(image_path)
        elif 'pants' in image:
            images['pants'].append(image_path)

    context = {
        'images_tops': images['tops'],
        'images_pants': images['pants'],
    }

    return render(request, 'image_gallery.html', context)

def delete_image(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return JsonResponse({'message': 'Image deleted successfully.'})
    else:
        return JsonResponse({'error': 'File not found.'}, status=404)

def fitting(request):
    image1 = request.GET.get('image1', '')
    image2 = request.GET.get('image2', '')

    return render(request, 'fitting.html', {'selectedImages': [image1, image2]})