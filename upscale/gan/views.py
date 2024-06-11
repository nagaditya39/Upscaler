from io import BytesIO
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .forms import userInputUpload
from .models import scaled
from keras.models import load_model
from utils import read_image, scale_image_0_1_range, tensor2img
from metrics import calculate_psnr, calculate_ssim
from esrgan import rrdb_net
import tensorflow as tf
from PIL import Image

SCALE = 4
INPUT_SHAPE = (None, None, 3)
MODEL_PATH = settings.RRDB_MODEL_PATH

def upscale_image(image_path, model):
    lr_image = read_image(image_path)
    lr_image = scale_image_0_1_range(lr_image)
    lr_image = tf.expand_dims(lr_image, axis=0)
    generated_hr = model(lr_image)
    generated_hr_image = tensor2img(generated_hr)
    return generated_hr_image


def upload_file(request):
    if request.method == 'POST':
        form = userInputUpload(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()

            model = rrdb_net(input_shape=INPUT_SHAPE, scale_factor=SCALE)

            if os.path.isfile(MODEL_PATH):
                try:
                    h5_model = load_model(MODEL_PATH, custom_objects={'tf': tf})
                    weights = h5_model.get_weights()
                    model.set_weights(weights)
                    print(f"Model weights loaded from {MODEL_PATH}")
                except Exception as e:
                    print(f"Error loading model: {e}")
                    return HttpResponse(f"Error loading model: {e}")
            else:
                print("Model file not found.")
                return HttpResponse("Model file not found.")

            if image_instance.input_image and image_instance.ground_img: 
                upscaled_image_array = upscale_image(image_instance.input_image.path, model)
                upscaled_image = Image.fromarray(upscaled_image_array)
                

                ground_truth_image_array = read_image(image_instance.ground_img.path)
                psnr_value = calculate_psnr(ground_truth_image_array, upscaled_image_array)
                ssim_value = calculate_ssim(ground_truth_image_array, upscaled_image_array)
                image_instance.psnr = psnr_value
                image_instance.ssim = ssim_value
            
                image_buffer = BytesIO() 
                upscaled_image.save(image_buffer, format='PNG')  
                image_buffer.seek(0)  

                image_instance.output_image.save(f"upscaled_{image_instance.id}.png", image_buffer)
                image_instance.save()
                return redirect('success')  
            else:
                return HttpResponse("Please upload both input and ground truth images.")
        else:
            return HttpResponse("Please upload an image file.")
    else:
        form = userInputUpload()
    return render(request, 'gan/upload.html', {'form': form})

def view_images(request):
    images = scaled.objects.all()
    return render(request, 'gan/view_images.html', {'images': images})

def delete_image(request, image_id):
    image = scaled.objects.get(id=image_id)
    image.input_image.delete()
    image.output_image.delete()
    image.delete()
    return redirect('view_images')

def success_view(request):
    return render(request, 'gan/success.html')