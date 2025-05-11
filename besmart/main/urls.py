from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.homepage, name='homepage'),
    path('home-test/', views.home, name='home'),
<<<<<<< HEAD
    # path('like/<int:content_id>/', views.like_content, name='like_content'),
    path('like_content/<int:content_id>/', views.like_content, name='like_content'),
=======
    path('like/<int:content_id>/', views.like_content, name='like_content'),
>>>>>>> origin/gulmira
    path('comment/<int:content_id>/', views.comment_content, name='comment_content'),
    path('subscribe/<int:user_id>/', views.subscribe_user, name='subscribe_user'),

]
