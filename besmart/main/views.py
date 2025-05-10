from django.shortcuts import render
from accounts.models import Content, Profile, User  # import Content from accounts


def homepage(request):
    return render(request, 'main/home.html')

def home(request):
    contents = Content.objects.select_related('user').order_by('-upload_time')
    return render(request, 'main/home_test.html', {'contents': contents})


# accounts/views.py

from django.shortcuts import redirect, get_object_or_404
from .models import Content, Like, Comment, Subscription
from django.contrib.auth.decorators import login_required

@login_required
def like_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    Like.objects.get_or_create(user=request.user, content=content)
    return redirect('home')

@login_required
def comment_content(request, content_id):
    if request.method == 'POST':
        content = get_object_or_404(Content, id=content_id)
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(user=request.user, content=content, text=text)
    return redirect('home')

@login_required
def subscribe_user(request, user_id):
    creator = get_object_or_404(User, id=user_id)
    Subscription.objects.get_or_create(subscriber=request.user, creator=creator)
    return redirect('home')
