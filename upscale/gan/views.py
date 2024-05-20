from django.shortcuts import render,redirect
from .forms import userInputUpload
from .models import scaled
# Create your views here.

def upload_file(request):
   
    if request.method == "POST":
        form = userInputUpload(request.POST,request.FILES)
        print(request.FILES)
        if form.is_valid():
           form.save()

           return redirect('success')  
    else:
        form = userInputUpload()
    return render(request, 'gan/upload.html', {'form': form})

def success_view(request):
    
    latest_upload = scaled.objects.last()  
    if latest_upload:
        upload_url = latest_upload.low_res.url
    else:
        upload_url = None  
    return render(request, 'gan/success.html', {'upload_url': upload_url})