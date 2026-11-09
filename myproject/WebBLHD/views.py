from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import VideoUploadForm
from .models import VideoUpload

def login_view(request):
    """Trang đăng nhập hệ thống, tự động bắt sự kiện chưa đăng nhập"""
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next', 'index')
            if not next_url or 'admin' in next_url:
                next_url = 'index'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        
    show_auth_message = 'next' in request.GET or 'next' in request.POST
        
    context = {
        'form': form,
        'show_auth_message': show_auth_message,
    }
    return render(request, 'WebBLHD/login.html', context)

def logout_view(request):
    """Đăng xuất khỏi hệ thống"""
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    """Trang chủ / Quản lý danh sách video (Bắt buộc đăng nhập)"""
    videos = VideoUpload.objects.all().order_by('-recording_time' if hasattr(VideoUpload, 'recording_time') else '-id')
    
    query = request.GET.get('q', '')
    camera = request.GET.get('camera', '')
    status = request.GET.get('status', '')
    date_str = request.GET.get('date', '')
    
    if query:
        videos = videos.filter(Q(title__icontains=query) | Q(video_id__icontains=query)) if hasattr(VideoUpload, 'video_id') else videos.filter(Q(title__icontains=query))
    if camera:
        videos = videos.filter(camera_location=camera)
    if status:
        videos = videos.filter(status=status)
    if date_str:
        videos = videos.filter(recording_time__date=date_str) if hasattr(VideoUpload, 'recording_time') else videos
        
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('giam_sat')
    else:
        form = VideoUploadForm()
        
    context = {
        'form': form,
        'videos': videos,
        'query': query,
        'selected_camera': camera,
        'selected_status': status,
        'selected_date': date_str,
    }
    return render(request, 'WebBLHD/index.html', context)

@login_required(login_url='login')
def giam_sat_view(request):
    """Trang giám sát camera trực quan (Bắt buộc đăng nhập)"""
    videos = VideoUpload.objects.all().order_by('-recording_time' if hasattr(VideoUpload, 'recording_time') else '-id')
    
    query = request.GET.get('q', '')
    camera = request.GET.get('camera', '')
    status = request.GET.get('status', '')
    date_str = request.GET.get('date', '')
    
    if query:
        videos = videos.filter(Q(title__icontains=query))
    if camera:
        videos = videos.filter(camera_location=camera)
    if status:
        videos = videos.filter(status=status)
        
    context = {
        'videos': videos,
        'query': query,
        'selected_camera': camera,
        'selected_status': status,
    }
    return render(request, 'WebBLHD/giam_sat.html', context)

@login_required(login_url='login')
def upload_video_view(request):
    """Trang tải lên video mới (Bắt buộc đăng nhập)"""
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('giam_sat')
    else:
        form = VideoUploadForm()
        
    context = {
        'form': form,
    }
    return render(request, 'WebBLHD/upload.html', context)

@login_required(login_url='video_detail')
def video_detail(request, video_id):
    """Trang xem chi tiết video AI"""
    video = get_object_or_404(VideoUpload, pk=video_id)
    return render(request, 'WebBLHD/videoDetails.html', {'video': video})