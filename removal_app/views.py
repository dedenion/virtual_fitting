from django.http import JsonResponse
from .forms import ImageUploadForm
import rembg
import base64
from PIL import Image, ImageOps
import io
import numpy as np
import random  # ランダムな値を生成するためのモジュール
from django.shortcuts import render

def remove_background(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # フォームから画像を取得
            image_data = form.cleaned_data['image'].file.read()

            # 画像処理と背景除去
            processed_image = process_image(image_data)
            output_image = rembg.remove(processed_image)

            # ランダムなクラス名と信頼度スコアを生成
            class_name = f"Class_{random.randint(1, 100)}"
            confidence_score = random.uniform(0.5, 0.95)

            # レスポンスを返す
            return JsonResponse({
                'processed_image': base64.b64encode(processed_image).decode("utf-8"),
                'output_image': base64.b64encode(output_image).decode("utf-8"),
                'class_name': class_name,
                'confidence_score': confidence_score
            })
        # フォームが無効な場合の処理
        # エラーメッセージを返すか、フォームエラーの詳細を返すなどの対応が必要です
    else:
        # GETリクエストに対する処理
        form = ImageUploadForm()
        context = {'form': form}
        return render(request, 'remove_background.html', context)

# process_image関数はそのままにしておきます
def process_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    max_size = max(image.size)
    new_image = image.crop((0, 0, max_size, max_size))
    output_image = io.BytesIO()
    new_image.save(output_image, format='PNG')
    processed_image = output_image.getvalue()
    return processed_image
