from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'bio', 'interests', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'interests': forms.Textarea(attrs={'rows': 2}),
        }
