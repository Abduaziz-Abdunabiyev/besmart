from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Profile, Content
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Signup successful.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/auth.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to homepage or dashboard
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/auth.html')

from django.db.models import Sum
from .models import Like

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')

    user_contents = Content.objects.filter(user=request.user)
    video_count = user_contents.filter(content_type='video').count()
    photo_count = user_contents.filter(content_type='image').count()
    content_ids = user_contents.values_list('id', flat=True)
    total_likes = Like.objects.filter(content_id__in=content_ids).count()  
    subscriber_count = profile.subscribers

    context = {
        'form': form,
        'profile': profile,
        'video_count': video_count,
        'photo_count': photo_count,
        'total_likes': total_likes,
        'subscriber_count': subscriber_count,
        'user_contents': user_contents,
    }
    return render(request, 'accounts/profile.html', context)

from django.http import JsonResponse

@login_required
def like_content(request):
    if request.method == 'POST' and request.is_ajax():
        content_id = request.POST.get('content_id')
        action = request.POST.get('action')  # 'like' or 'unlike'
        
        try:
            content = Content.objects.get(id=content_id, user=request.user)
            
            if action == 'like':
                content.likes += 1
            elif action == 'unlike' and content.likes > 0:
                content.likes -= 1
            
            content.save()
            return JsonResponse({'status': 'success', 'likes': content.likes})
        
        except Content.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Content not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


from .forms import ContentUploadForm

# @login_required
# def upload_content(request):
#     if request.method == 'POST':
#         form = ContentUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             content = form.save(commit=False)
#             content.user = request.user
#             content.save()
#             return redirect('home')
#     else:
#         form = ContentUploadForm()
#     return render(request, 'accounts/upload_content.html', {'form': form})

from accounts.utils.ai_filter import is_content_meaningful, generate_tags
import os
import mimetypes
import traceback
from django.conf import settings
from django.core.files.storage import default_storage
from accounts.utils.image_filter import is_image_meaningful
from accounts.utils.video_filter import is_video_appropriate  # <-- Whisper-based video filter

def upload_content(request):
    if request.method == 'POST':
        form = ContentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            content_type = form.cleaned_data['content_type']
            description = form.cleaned_data['description']
            uploaded_file = form.cleaned_data['content_file']

            temp_path = default_storage.save('temp/' + uploaded_file.name, uploaded_file)
            full_temp_path = os.path.join(settings.MEDIA_ROOT, temp_path)

            # --- MIME Type Check ---
            mime_type, _ = mimetypes.guess_type(full_temp_path)
            if content_type == 'video' and (not mime_type or not mime_type.startswith('video')):
                messages.error(request, "⚠️ The uploaded file is not a valid video.")
                default_storage.delete(temp_path)
                return render(request, 'accounts/upload_content.html', {'form': form})

            # --- 1. Image Filter ---
            if content_type == 'image':
                if not is_image_meaningful(full_temp_path):
                    messages.error(request, "🖼️ This image is not meaningful or educational.")
                    default_storage.delete(temp_path)
                    return render(request, 'accounts/upload_content.html', {'form': form})

            # --- 2. Video Filter (Whisper + Multi-AI) ---
            if content_type == 'video':
                try:
                    is_clean, reason, transcript = is_video_appropriate(full_temp_path)
                    if not is_clean:
                        messages.error(request, reason)
                        default_storage.delete(temp_path)
                        return render(request, 'accounts/upload_content.html', {'form': form})
                    print("🧾 Transcript:", transcript)
                except Exception as e:
                    if settings.DEBUG:
                        messages.error(request, f"⚠️ Error: {traceback.format_exc()}")
                    else:
                        messages.error(request, f"⚠️ Error processing video. Please try again.")
                    default_storage.delete(temp_path)
                    return render(request, 'accounts/upload_content.html', {'form': form})

            # --- 3. Description Filter ---
            if not is_content_meaningful(description):
                messages.error(request, "📝 Description does not appear meaningful or educational.")
                default_storage.delete(temp_path)
                return render(request, 'accounts/upload_content.html', {'form': form})

            # --- 4. Tag Generation + Save ---
            tags = generate_tags(description)
            content = form.save(commit=False)
            content.user = request.user
            content.tags = tags
            # content.transcript = transcript if content_type == 'video' else ""
            content.save()

            default_storage.delete(temp_path)
            messages.success(request, "✅ Content uploaded successfully!")
            return redirect('home')
    else:
        form = ContentUploadForm()

    return render(request, 'accounts/upload_content.html', {'form': form})

from django.shortcuts import get_object_or_404

@login_required
def delete_content(request, content_id):
    content = get_object_or_404(Content, id=content_id, user=request.user)
    if request.method == "POST":
        content.delete()  # This removes the record from the DB
        # Optional: remove the file from the filesystem (only if using FileSystemStorage)
        if content.content_file:
            content.content_file.delete(save=False)
    return redirect('profile_view')  # Change to your actual profile page URL name
