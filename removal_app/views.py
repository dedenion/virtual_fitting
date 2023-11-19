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
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from django import template



class YourTemplateView(TemplateView):
    template_name = 'index.html'




from django.core.files.base import ContentFile


# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

def save_to_media(image_data, filename):
    # ファイルを `media` フォルダに保存
    media_root = settings.MEDIA_ROOT
    file_path = os.path.join(media_root, filename)

    with open(file_path, 'wb') as f:
        f.write(image_data)

    return file_path

# ... (他のインポートや関数の定義)

# removal_app/views.py

# ... (他のインポートや関数の定義)

def remove_background(request):
    output_image_path = request.session.get('output_image_path', None)
    fs_gallery = FileSystemStorage(location=settings.MEDIA_ROOT)

    # 分類結果の変数を初期化
    class_name = None
    confidence_score = None

def remove_background(request):
    # セッションから前回の画像をクリア
    if 'output_image_path' in request.session:
        del request.session['output_image_path']

    fs_gallery = FileSystemStorage(location=settings.MEDIA_ROOT)

    # 分類結果の変数を初期化
    class_name = None
    confidence_score = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            image_data = form.cleaned_data['image'].file.read()

            # 画像の加工と背景除去
            processed_image = process_and_remove_background(image_data)
            
            # 背景除去
            output_image = rembg.remove(base64.b64decode(processed_image))

            # クラス名を取得
            class_name, confidence_score, _ = classify_image(processed_image, form.cleaned_data['image'].name)  # filename を渡す

            # 画像分類の結果を表示
            print("Class:", class_name)
            print("Confidence Score:", confidence_score)

            # 画像分類の結果をもとにファイル名を生成
            image_filename = generate_filename({"class_name": class_name}, form.cleaned_data['image'].name, class_name)

            # 画像を `media` フォルダに保存
            image_path = save_to_media(base64.b64decode(processed_image), image_filename)
            request.session['output_image_path'] = fs_gallery.url(image_path)


            # ファイルパスではなく、メディアURLをセッションに保存
            request.session['output_image_path'] = fs_gallery.url(image_path)  # URL を保存

    else:
        form = ImageUploadForm()

    return render(request, 'remove_background.html', {'form': form, 'output_image_path': request.session.get('output_image_path'), 'class_name': class_name, 'confidence_score': confidence_score})

def classify_image(output_image, filename):
    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Load and preprocess the image
    image = Image.open(io.BytesIO(base64.b64decode(output_image))).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Predict the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    
    # Get the class name using [2:] to remove leading spaces
    class_name = class_names[index][2:].strip()
    
    confidence_score = prediction[0][index]

    # ファイル名を生成
    image_filename = generate_filename({"class_name": class_name}, filename, class_name)

    return class_name, confidence_score, image_filename


# removal_app/views.py

def generate_filename(instance, filename, class_name):
    now = timezone.now()
    # instanceが存在し、class_nameが'tops'または'pants'の場合、その値を優先して使用
    if instance and 'class_name' in instance:
        class_name = instance['class_name']
    else:
        print(f"Using 'unknown' for class_name")
        class_name = 'unknown'
    unique_filename = f"{now.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4()}_{class_name}.jpg"
    return unique_filename


def process_and_remove_background(image_data):
    # 画像を処理して縦横の幅が広い方をカットし、正方形に加工
    processed_image = process_image(Image.open(io.BytesIO(image_data)))

    # 背景除去
    output_image = rembg.remove(processed_image)

    return base64.b64encode(output_image).decode("utf-8")

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