import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from pathlib import Path
import re


def read_image(img_path):
    base=os.path.basename(img_path)
    ext = os.path.splitext(base)[1]
    assert ext in ['.PNG','.JPG','.png', '.jpg', '.jpeg', '.JPEG']
    image = tf.io.read_file(img_path)
    if ext == '.png':
        image = tf.image.decode_png(image, channels=3)
    else:
        image = tf.image.decode_jpeg(image, channels=3)
    return image


def scale_image_0_1_range(image):
    image = image / 255
    red_max = tf.reduce_max(image, axis=None)
    red_min = tf.reduce_min(image, axis=None)
    if red_max > 1 or red_min < 0:
        image = tf.clip_by_value(
            image, 0, 1, name=None
        )
    return image



def tensor2img(tensor):
    return (np.squeeze(tensor.numpy()).clip(0, 1) * 255).astype(np.uint8)


def save_image_grid(lr, hr, ref=None, save_path=None):
    lr_title = "lr: {}".format(lr.shape)
    hr_title = "hr: {}".format(hr.shape)
    images = [lr, hr]
    titles = [lr_title, hr_title]
    if ref is not None:
        ref_title = "ref: {}".format(ref.shape)
        images += [ref]
        titles += [ref_title]
        fig, axes = plt.subplots(1, 3, figsize=(20, 10))
    else:
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))


    for i, (img, title) in enumerate(zip(images, titles)):
        axes[i].imshow(img)
        axes[i].set_title(title, fontsize = 20)
        axes[i].axis('off')

    if save_path:
      fig.savefig(save_path, bbox_inches='tight', pad_inches=0.25)
      print(f"Saving image to: {save_path}")

      hr_save_path = os.path.splitext(save_path)[0] + "_hr.png"

      plt.imsave(hr_save_path, hr)
      print(f"Saving individual hr images:")
      print(f"- HR image: {hr_save_path}")

    plt.show()






