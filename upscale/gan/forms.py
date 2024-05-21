from django import forms
from .models import scaled

class userInputUpload(forms.ModelForm):
    class Meta:
        model = scaled
        fields = ['input_image','ground_img']