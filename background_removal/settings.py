

from pathlib import Path
import os
from decouple import Config, Csv
import dj_database_url 
import cloudinary
import environ


BASE_DIR = Path(__file__).resolve().parent.parent


# .envファイルが存在する場合はロードする
env_file = Path(".") / ".env"
if env_file.exists():
    environ.Env.read_env(str(env_file))

env = environ.Env()


SECRET_KEY = 'fhalfahghiaghiahvhpg843ytygsjroeigjirinbknitrh348ujijguj8ujgdngire834jgjkgnsjrgiu34jgihosghie4ru934jgjeoigjo34uegoirgj39485u98w384yuwgjlrjgu845oujgeojg498uyg4eigjshoie4tug29ty483ytgirdngboerhgw9utg4j3itj34jgy7wygsnvglkeh4oyt34ut20ut3ihgiojeo9u48to4iwhgjsljrigut43ut8gojgjmosirwug4utoiwj39gu8uj4j398tuosiejgno4ij493yut98jifgenwgjoi438uty8shiogj4893utosjgi4o389tu98sjgohes4'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'cloudinary_storage',
    'cloudinary',
    "removal_app",
    'django_celery_results',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "background_removal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "background_removal.wsgi.application"


# HerokuのJawsDB MySQLの接続情報を取得
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# マイグレーションファイルのディレクトリを変更する場合（必須ではありませんが推奨されます）
MIGRATION_MODULES = {
    'removal_app': 'removal_app.migrations_jawsdb',  # 必要なアプリに適用してください
}




AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / 'staticfiles')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_URL = '/media/'


MODEL_PATH = BASE_DIR / "keras_model.h5"
LABELS_PATH = BASE_DIR / "labels.txt"

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}

# Celery設定
# Celeryの設定
CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL', 'amqp://')  # CloudAMQPの接続URLを環境変数から取得
CELERY_RESULT_BACKEND = 'rpc://'  # CloudAMQPを結果バックエンドとして指定
# task状態が開始になったかを確認できるための設定
CELERY_TASK_TRACK_STARTED = True
