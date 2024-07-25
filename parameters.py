import imageio
import numpy as np
from skimage.transform import resize

def mse(image1, image2):
    array1 = np.array(image1)
    array2 = np.array(image2)

    if array1.shape != array2.shape:
        raise ValueError("Images must have the same dimensions")

    mse_values = np.mean((array1 - array2) ** 2, axis=(0, 1))
    return mse_values

def psnr(mse_values, max_pixel_value=255):
    psnr_values = 10 * np.log10((max_pixel_value)**2 / mse_values)
    return psnr_values

# Load images
image_path1 = "path to image 1"
image_path2 = "path to image 2"
image1 = imageio.imread(image_path1)
image2 = imageio.imread(image_path2)

# Check and resize images if necessary
if image1.shape != image2.shape:
    # Resize images to the same dimensions
    image1 = resize(image1, (image2.shape[0], image2.shape[1]))

# Calculate MSE and PSNR
mse_values = mse(image1, image2)
psnr_values = psnr(mse_values)

# Print results
for i, psnr_value in enumerate(psnr_values):
    if i == 0:
        print(f"PSNR for RED channel: {psnr_value} dB")
    elif i == 1:
        print(f"PSNR for GREEN channel: {psnr_value} dB")
    elif i == 2:
        print(f"PSNR for BLUE channel: {psnr_value} dB\n")

for i, mse_value in enumerate(mse_values):
    if i == 0:
        print(f"MSE for RED channel: {mse_value}")
    elif i == 1:
        print(f"MSE for GREEN channel: {mse_value}")
    elif i == 2:
        print(f"MSE for BLUE channel: {mse_value}\n")
