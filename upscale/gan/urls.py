from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('success/', views.success_view, name='success'),
    path('images/', views.view_images, name='view_images'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
]