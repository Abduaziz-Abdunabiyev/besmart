from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'interests', 'skills', 'social_links', 'profile_picture', 'achievements', 'notification_preferences']
        widgets = {
            'achievements': forms.Textarea(attrs={'placeholder': 'Add achievements like awards or badges'}),
            'social_links': forms.Textarea(attrs={'placeholder': 'Add links to your social profiles (JSON format)'}),
        }

# forms.py
from .models import Content

class ContentUploadForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['content_type', 'content_file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter a short description'}),
        }
