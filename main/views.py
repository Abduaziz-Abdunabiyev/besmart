from django.shortcuts import render
from accounts.models import Content, Profile, User  # import Content from accounts


def homepage(request):
    return render(request, 'main/home.html')

def home(request):
    contents = Content.objects.select_related('user').order_by('-upload_time')

    # Получаем пользователей с профилем
    users = User.objects.select_related('profile').exclude(id=request.user.id)

    return render(request, 'main/home_test.html', {
        'contents': contents,
        'users': users
    })


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

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def comment_content(request, content_id):
    if request.method == "POST":
        content = Content.objects.get(id=content_id)
        comment_text = request.POST.get('comment')
        comment = Comment.objects.create(user=request.user, content=content, text=comment_text)
        return JsonResponse({'user': request.user.username, 'comment': comment.text})

@login_required
def subscribe_user(request, user_id):
    creator = get_object_or_404(User, id=user_id)
    Subscription.objects.get_or_create(subscriber=request.user, creator=creator)
    return redirect('home')


def video_list(request):
    videos = Content.objects.filter(content_type='video').order_by('-upload_time')
    return render(request, 'main/videos.html', {'videos': videos})


# def video_detail(request):
#     contents = Content.objects.select_related('user').order_by('-upload_time')
#     return render(request, 'main/videos_item.html', {'contents': contents})

# def reels_list(request):
#     return render(request, 'main/reels.html')


def reels_android(request):
    contents = Content.objects.select_related('user').order_by('-upload_time')
    return render(request, 'main/reels_android.html', {'contents': contents}) 


def reels_list(request):
    # Видео с длительностью до 60 секунд включительно
    contents = Content.objects.filter(content_type='video', duration__lte=60).order_by('-upload_time')
    return render(request, 'main/reels.html', {'contents': contents, 'current_tab': 'reels'})

def video_detail(request):
    # Видео с длительностью более 60 секунд
    contents = Content.objects.filter(content_type='video', duration__gt=60).order_by('-upload_time')
    return render(request, 'main/videos_item.html', {'contents': contents, 'current_tab': 'video'})

# def content_photo(request):
#     contents = Content.objects.filter(content_type='image').order_by('-upload_time')
#     return render(request, 'main/content_list.html', {'contents': contents, 'current_tab': 'photo'})
