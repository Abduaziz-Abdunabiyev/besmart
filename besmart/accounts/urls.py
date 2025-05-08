from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile_view'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('upload_content/', views.upload_content, name='upload_content'),
    
]

