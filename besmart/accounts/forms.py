from django import forms
from .models import Profile, Content

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'avatar', 'age', 'interests', 'contact_preferences', 'content_preferences', 'achievements']

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
