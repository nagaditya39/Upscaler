
import os
import glob
import PIL
from PIL import Image
from pathlib import Path
import tensorflow as tf
from keras.models import load_model
from .esrgan import rrdb_net
from .utils import read_image, scale_image_0_1_range, tensor2img
from .utils import save_image_grid
from .metrics import calculate_psnr, calculate_ssim


SCALE = 4
INPUT_SHAPE=(None, None, 3)


MODEL_PATH = "./saved/models/interp_esr.h5"


IMG_DIR = "/content/finalproj/MyDrive/test/input"  # Path to the directory containing LR images
GT_DIR = "/content/finalproj/MyDrive/test/ground_truth"  # Path to the directory containing ground truth HR images
SAVE_DIR = "/content/finalproj/MyDrive/test/results/interp_res"  # Directory to save the upscaled interp results

Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)

def main():

    model = rrdb_net(input_shape=INPUT_SHAPE,scale_factor=SCALE)

    if os.path.isfile(MODEL_PATH):
        h5_model = load_model(MODEL_PATH, custom_objects={'tf': tf})
        weights = h5_model.get_weights()
        model.set_weights(weights)
        print("[*] load model weights from {}.".format(
        MODEL_PATH))
    else:
        print("[*] Cannot find ckpt or h5 model file.")
        exit()
    model.summary()

    if os.path.isdir(IMG_DIR):  # Check if it's a directory
        for img_path in glob.glob(os.path.join(IMG_DIR, "*.png")):  # Assuming PNG images
            # Extract filename without extension
            filename = os.path.splitext(os.path.basename(img_path))[0]

            # Load LR image
            lr_image = read_image(img_path)
            lr_image = scale_image_0_1_range(lr_image)
            lr_image = tf.expand_dims(lr_image, axis=0)

            base_filename = filename[2:]

            # Load ground truth HR image
            hr_filename = f"hr{base_filename}.png"  # Add "hr" prefix and extension
            hr_img_path = os.path.join(GT_DIR, hr_filename)
            hr_image = read_image(hr_img_path)


            # Generate HR image
            generated_hr = model(lr_image)
            generated_hr_image = tensor2img(generated_hr)
            unscale_lr_image = tensor2img(lr_image)

            # Calculate metrics
            psnr = calculate_psnr(hr_image, generated_hr_image)
            ssim = calculate_ssim(hr_image, generated_hr_image)
            print(f"[***] Image: {filename}, PSNR: {psnr}, SSIM: {ssim}")

            # Save image grid
            save_path = os.path.join(SAVE_DIR, f"{filename}inter_upscaled.png")
            save_image_grid(unscale_lr_image, generated_hr_image,  hr_image, save_path=save_path)

    else:
        print(f"[!] Invalid image directories: {IMG_DIR}")

if __name__ == '__main__':
    main()