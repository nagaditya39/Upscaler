from django import forms

class userInputUpload(forms.Form):
    input_img = forms.FileField(label="Uplaod Image:")