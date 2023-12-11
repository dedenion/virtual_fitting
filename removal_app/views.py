from django.http import JsonResponse
from .forms import ImageUploadForm
import rembg
import base64
from PIL import Image, ImageOps
import io
from keras.models import load_model
import numpy as np
from django.shortcuts import render

# モデルとクラス名の読み込み
model = load_model("keras_Model.h5", compile=False)
class_names = [line.strip() for line in open("labels.txt", "r")]

def remove_background(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # フォームから画像を取得
            image_data = form.cleaned_data['image'].file.read()

            # 画像処理と背景除去
            processed_image = process_image(image_data)
            output_image = rembg.remove(processed_image)

            # 画像分類
            class_name, confidence_score = classify_image(output_image)

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

def classify_image(output_image):
    # ここで必要な画像の前処理を行う（背景除去後の画像を扱う）
    # この関数内での前処理は背景除去後の画像に対してのみ必要
    # その後画像分類を行うための処理を追加する
    image = Image.open(io.BytesIO(output_image)).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # 以下は現在の classify_image() 関数と同様の画像分類の処理を追加する

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = float(prediction[0][index])
    return class_name, confidence_score

def process_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    max_size = max(image.size)
    new_image = image.crop((0, 0, max_size, max_size))
    output_image = io.BytesIO()
    new_image.save(output_image, format='PNG')
    processed_image = output_image.getvalue()
    return processed_image
