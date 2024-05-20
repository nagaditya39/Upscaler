from django import forms
from .models import scaled

class userInputUpload(forms.ModelForm):
    class Meta:
        model = scaled
        fields = ['name','low_res']