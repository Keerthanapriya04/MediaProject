from django import forms
from .models import MediaJob

class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = MediaJob
        fields = ['original_file']
        widgets = {
            'original_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'required': True
            })
        }