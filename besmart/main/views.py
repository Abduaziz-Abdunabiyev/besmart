from django.shortcuts import render
from accounts.models import Content, Profile, User  # import Content from accounts


def homepage(request):
    return render(request, 'main/home.html')

def home(request):
    contents = Content.objects.select_related('user').order_by('-upload_time')
    return render(request, 'main/home_test.html', {'contents': contents})


from django.shortcuts import redirect, get_object_or_404
from .models import Comment, Subscription
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
from django.http import JsonResponse
from main.models import Content
from accounts.models import Like

@login_required
# def like_content(request, content_id):
#     content = get_object_or_404(Content, id=content_id)

#     # Create a Like only if it doesn't already exist
#     like, created = Like.objects.get_or_create(user=request.user, content=content)

#     if created:
#         content.likes += 1  # optional
#         content.save()

#     total_likes = Like.objects.filter(content=content).count()
#     return HttpResponse(status=204)
def like_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)

    # Check if the user has already liked the content
    like = Like.objects.filter(user=request.user, content=content).first()

    if like:
        # If the user has already liked the content, remove the like (unlike)
        like.delete()
        action = "unliked"
    else:
        # If the user has not liked the content yet, add the like
        Like.objects.create(user=request.user, content=content)
        action = "liked"

    total_likes = Like.objects.filter(content=content).count()  # Get the updated like count

    # Return a JSON response with the updated like count and action (liked/unliked)
    return JsonResponse({
        'total_likes': total_likes,
        'action': action
    })

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


def video_list(request):
    videos = Content.objects.filter(content_type='video').order_by('-upload_time')
    return render(request, 'main/videos.html', {'videos': videos})
