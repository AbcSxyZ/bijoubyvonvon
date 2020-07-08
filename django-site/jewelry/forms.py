from django import forms
from django.forms import widgets

class DescriptionForm(forms.Form):
    """
    Displayed as an admin view to change the description/images
    of the website.
    """
    description = forms.CharField(widget=forms.Textarea)
    image_profil = forms.ImageField(label="Image profil", required=True)
    image_banner = forms.ImageField(label="Image bannière", required=True)

    def is_valid(self, *args, **kwargs):
        super().is_valid(*args, **kwargs)
        return True
