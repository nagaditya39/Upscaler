from django.db import models

class scaled(models.Model):
    input_image = models.ImageField(upload_to='input_images/', null=True, blank=True)
    ground_img = models.ImageField(upload_to='ground_img/', null=True, blank=True)

    output_image = models.ImageField(upload_to='output_images/', null=True, blank=True)
    psnr = models.FloatField(null=True, blank=True)
    ssim = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Scaled Image {self.id}"
