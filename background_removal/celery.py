from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Djangoの設定をロードするための環境変数を設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'background_removal.settings')

app = Celery('background_removal')

# Celeryの設定
app.config_from_object('django.conf:settings', namespace='CELERY')

# タスクの自動検出
app.autodiscover_tasks()
