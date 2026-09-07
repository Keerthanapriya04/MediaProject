from pathlib import Path

from django import forms

from .models import MediaFile


class MediaUploadForm(forms.ModelForm):

    operation = forms.ChoiceField(
        choices=[
            ("resize", "Resize Image"),
            ("crop", "Crop Image"),
            ("compress", "Compress Media"),
            ("watermark", "Add Watermark"),
            ("thumbnail", "Generate Thumbnail"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = MediaFile

        fields = ["file"]

        widgets = {
            "file": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*,video/*",
                }
            ),
        }

    def clean_file(self):

        uploaded_file = self.cleaned_data.get("file")

        # ------------------------------------------------
        # 1. Check file exists
        # ------------------------------------------------

        if not uploaded_file:
            raise forms.ValidationError(
                "Please select a file."
            )

        # ------------------------------------------------
        # 2. Check empty file
        # ------------------------------------------------

        if uploaded_file.size == 0:
            raise forms.ValidationError(
                "The uploaded file is empty."
            )

        # ------------------------------------------------
        # 3. Maximum file size = 100 MB
        # ------------------------------------------------

        max_size = 100 * 1024 * 1024

        if uploaded_file.size > max_size:
            raise forms.ValidationError(
                "File size cannot exceed 100 MB."
            )

        # ------------------------------------------------
        # 4. Allowed extensions
        # ------------------------------------------------

        allowed_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".gif",
            ".mp4",
            ".mpeg",
            ".mov",
            ".webm",
        }

        extension = Path(uploaded_file.name).suffix.lower()

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Unsupported file extension."
            )

        # ------------------------------------------------
        # 5. Allowed MIME types
        # ------------------------------------------------

        allowed_mime_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
            "image/gif",
            "video/mp4",
            "video/mpeg",
            "video/quicktime",
            "video/webm",
        }

        if uploaded_file.content_type not in allowed_mime_types:
            raise forms.ValidationError(
                "Unsupported file type."
            )

        return uploaded_file