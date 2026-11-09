from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('giam-sat/', views.giam_sat_view, name='giam_sat'),
    path('upload/', views.upload_video_view, name='video_upload'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
]