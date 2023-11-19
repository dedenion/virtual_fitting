# removal_app/forms.py
from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Upload Image', required=True, error_messages={'required': 'Please select an image.'})
    