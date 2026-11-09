from django.contrib import admin
from .models import VideoUpload  # Thay VideoUpload bằng tên model video thực tế của bạn trong models.py

admin.site.register(VideoUpload)