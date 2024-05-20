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

           return redirect('success')  # Redirect to a success page
    else:
        form = userInputUpload()
    return render(request, 'gan/upload.html', {'form': form})

def success_view(request):
    return render(request, 'gan/success.html')