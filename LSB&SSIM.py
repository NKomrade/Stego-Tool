from PIL import Image
import os

def text_to_binary(text):
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message

def resize_image(image, size=(128, 128)):
    return image.resize(size)

def encode_lsb(image, message):
    binary_message = text_to_binary(message)
    binary_message += '1111111111111110'

    data_index = 0
    delimiter_found = False

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = list(image.getpixel((i, j)))
            for color_channel in range(3):
                if data_index < len(binary_message):
                    pixel[color_channel] = (pixel[color_channel] & ~1) | int(binary_message[data_index])
                    data_index += 1
                else:
                    delimiter_found = True
                    break
            image.putpixel((i, j), tuple(pixel))
            if delimiter_found:
                break
        if delimiter_found:
            break

    return image

def spread_spectrum_encode(image, message, alpha=0.01):
    binary_message = text_to_binary(message)

    data_index = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = list(image.getpixel((i, j)))
            for color_channel in range(3):
                if data_index < len(binary_message):
                    # Ensure the resulting pixel value is in the valid range [0, 255]
                    new_value = min(255, max(0, pixel[color_channel] + round(alpha * int(binary_message[data_index]))))
                    pixel[color_channel] = new_value
                    data_index += 1
                else:
                    break
            image.putpixel((i, j), tuple(pixel))
            if data_index >= len(binary_message):
                break
    return image

def combine_lsb_spread_spectrum(image, message):
    # Resize the image to 256x256 pixels
    resized_image = resize_image(image.copy(), size=(128, 128))

    # Encode the first half of the message using LSB
    lsb_message = message
    lsb_encoded_image = encode_lsb(resized_image.copy(), lsb_message)

    # Encode the second half of the message using Spread Spectrum
    ss_message = message
    ss_encoded_image = spread_spectrum_encode(lsb_encoded_image.copy(), ss_message)

    return ss_encoded_image

def msg(filename):
    with open(filename, 'r') as file:
        msg = file.read()
    return msg

image_path = r"C:\Users\dearn\OneDrive\Pictures\2.bmp"
message = msg(r"C:\Users\dearn\OneDrive\Desktop\NK FOLDER\25KB.txt")

original_image = Image.open(image_path)

# Combine encoding methods on resized image
encoded_image = combine_lsb_spread_spectrum(original_image, message)

output_folder = r"C:\Users\dearn\OneDrive\Pictures"

os.makedirs(output_folder, exist_ok=True)

base_name = os.path.splitext(os.path.basename(image_path))[0]
output_path = os.path.join(output_folder, base_name + '_encoded.bmp')
encoded_image.save(output_path)
print(f"Encoded image saved at: {output_path}")
