from django import forms
from .models import Profile, Content

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'avatar', 'age', 'interests', 'contact_preferences', 'content_preferences', 'achievements']

    def save(self, commit=True):
        profile = super().save(commit=False)
        
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        
        if commit:
            user.save()  
            profile.save()  
        return profile

class ContentUploadForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['content_type', 'content_file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter a short description'}),
        }

<<<<<<< HEAD
# forms.py
from .models import Content

class ContentUploadForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['content_type', 'content_file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter a short description'}),
        }
=======

from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    full_name = forms.CharField(label='Full Name', max_length=255, required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # Update full_name of profile created by signal
            user.profile.full_name = self.cleaned_data["full_name"]
            user.profile.save()
        return user

>>>>>>> origin/main
