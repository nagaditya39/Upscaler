from django.db import models
from django.conf import settings
import PIL
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from utils import read_image, scale_image_0_1_range, tensor2img
# Create your models here.

class scaled(models.Model):
    name= models.CharField(max_length=50)
    low_res = models.ImageField(upload_to="gan/files/user_inp")

    def upscale_image(self):
        model = load_model(settings.RRDB_MODEL_PATH)
        lr_image = Image.open(self.low_res)
        # Resize LR image for RRDB model
        lr_image = lr_image.resize((128, 128))  
        lr_image_array = np.array(lr_image) / 255.0
        lr_image_tensor = tf.expand_dims(lr_image_array, axis=0)
        hr_image_tensor = model.predict(lr_image_tensor)
        hr_image_array = (hr_image_tensor.squeeze() * 255.0).astype(np.uint8)
        return Image.fromarray(hr_image_array)