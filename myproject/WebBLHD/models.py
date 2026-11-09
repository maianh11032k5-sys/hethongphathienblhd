import uuid
from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import VideoMediaCloudinaryStorage

class VideoUpload(models.Model):
    # Tự động cấp mã định danh video độc nhất (Ví dụ: BLHD-7F3A9C)
    video_id = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Mã Video")
    
    title = models.CharField(max_length=255, verbose_name="Tiêu đề video")
    camera_location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Vị trí / Khu vực Camera")
    recording_time = models.DateTimeField(blank=True, null=True, verbose_name="Thời gian ghi hình")
    
    # Tệp video lưu trên Cloudinary
    video_file = models.FileField(
        upload_to='videos/', 
        storage=VideoMediaCloudinaryStorage(), 
        verbose_name="File Video"
    )
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Người tải lên")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tải lên hệ thống")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả / Ghi chú")
    
    is_detected = models.BooleanField(default=False, verbose_name="Phát hiện bạo lực")
    detection_result = models.TextField(blank=True, null=True, verbose_name="Kết quả phân tích chi tiết")

    def save(self, *args, **kwargs):
        # Tự động sinh mã video nếu chưa có
        if not self.video_id:
            unique_code = uuid.uuid4().hex[:6].upper()
            self.video_id = f"BLHD-{unique_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.video_id}] {self.title}"