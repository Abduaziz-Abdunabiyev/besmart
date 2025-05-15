from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.homepage, name='homepage'),
    path('home-test/', views.home, name='home'),
    path('like/<int:content_id>/', views.like_content, name='like_content'),
    # path('like/<int:content_id>/', views.like_content, name='like_content'),
    path('like_content/<int:content_id>/', views.like_content, name='like_content'),
    path('comment/<int:content_id>/', views.comment_content, name='comment_content'),
    path('subscribe/<int:user_id>/', views.subscribe_user, name='subscribe_user'),
    path('videos/', views.video_list, name='video_list'),
    path('videos_item/', views.video_detail, name='video_detail'),
    path('reels/', views.reels_list, name='reels_list'),
    path('reels_android/', views.reels_android, name='reels_android'),

    path('reels/<int:pk>/', views.reel_detail, name='reel_detail'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    # path('image/<int:pk>/', views.image_detail, name='image_detail'),


]
