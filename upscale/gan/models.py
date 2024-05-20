from django.db import models

# Create your models here.

class scaled(models.Model):
    name= models.CharField(max_length=50)
    low_res = models.ImageField(upload_to="gan/files/user_inp")

    def __str__(self):
        return self.name
