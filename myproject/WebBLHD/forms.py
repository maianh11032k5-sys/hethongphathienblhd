from django import forms
from .models import VideoUpload

class VideoUploadForm(forms.ModelForm):
    # Khai báo trực tiếp danh sách lựa chọn cho trường camera_location để hiển thị dạng dropdown chuẩn
    camera_location = forms.ChoiceField(
        choices=[
            ('', '-- Chọn khu vực camera --'),
            ('Sân trường', 'Sân trường'),
            ('Cổng trường', 'Cổng trường'),
            ('Nhà A', 'Nhà A'),
            ('Nhà B', 'Nhà B'),
            ('Nhà xe', 'Nhà xe'),
            ('Cầu thang bộ', 'Cầu thang bộ'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Vị trí / Khu vực Camera"
    )

    class Meta:
        model = VideoUpload
        fields = ['title', 'camera_location', 'recording_time', 'video_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nhập tiêu đề hoặc tên sự kiện...'
            }),
            'recording_time': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
            'video_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }