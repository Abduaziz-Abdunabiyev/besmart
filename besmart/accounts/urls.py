from django.urls import path
from . import views
from .views import profile_view

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', profile_view, name='profile_view'),
    path('upload_content/', views.upload_content, name='upload_content'),
    
]

