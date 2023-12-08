from celery import shared_task
import base64
import rembg
from PIL import Image, ImageOps
import io
import numpy as np
from tensorflow.keras.models import load_model
from django.utils import timezone
import uuid
from django.conf import settings

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

@shared_task
def process_and_remove_background(image_data):
    # 画像を処理して縦横の幅が広い方をカットし、正方形に加工
    processed_image = process_image(Image.open(io.BytesIO(image_data)))

    # 背景除去
    output_image = rembg.remove(processed_image)

    return base64.b64encode(output_image).decode("utf-8")

@shared_task
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
# 他の関数も同様に追加可能
