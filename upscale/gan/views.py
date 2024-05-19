from django.shortcuts import render
from .user_upload import userInputUpload
# Create your views here.

def upload_file(request):
    if request.method == "POST":
        form = userInputUpload(request.POST,request.FILES)