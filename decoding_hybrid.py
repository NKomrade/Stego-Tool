from PIL import Image

def text_to_binary(text):
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message

def binary_to_text(binary_message):
    # Convert binary message to text
    text = ''
    for i in range(0, len(binary_message), 8):
        try:
            # Attempt to convert the binary substring to an integer
            char_code = int(binary_message[i:i+8], 2)
            # Check if the character code is a valid ASCII value
            if 0 <= char_code <= 255:
                text += chr(char_code)
            else:
                # If not a valid ASCII value, stop decoding
                break
        except ValueError:
            # If conversion fails, stop decoding
            break

    return text

def decode_lsb(image):
    binary_message = ''
    delimiter = '1111111111111110'

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = list(image.getpixel((i, j)))
            for color_channel in range(3):  # RGB channels
                # Extract the LSB of each color channel and append to the binary message
                binary_message += str(pixel[color_channel] & 1)

    # Find the index of the delimiter in the binary message
    delimiter_index = binary_message.find(delimiter)

    if delimiter_index != -1:
        # Remove the delimiter and get the actual binary message
        binary_message = binary_message[:delimiter_index]
    else:
        print("Delimiter not found. The hidden message may be incomplete.")

    return binary_message

def spread_spectrum_decode(image, alpha=0.1):
    binary_message = ''
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = list(image.getpixel((i, j)))
            for color_channel in range(3):  # RGB channels
                # Extract the spread spectrum encoded message from each color channel
                binary_message += str(pixel[color_channel] % 2**alpha)

    return binary_message

def decode_combined(image):
    # Decode using LSB
    lsb_binary_message = decode_lsb(image)

    # Decode using Spread Spectrum on the LSB-decoded message
    spread_spectrum_binary_message = spread_spectrum_decode(image)

    return lsb_binary_message, spread_spectrum_binary_message

# Take input from user
encoded_image_path = r"C:\Users\dearn\OneDrive\Pictures\2_encoded.bmp"

# Open the encoded image
encoded_image = Image.open(encoded_image_path)

# Decode the hidden message
lsb_message, spread_spectrum_message = decode_combined(encoded_image)

# Convert binary message to text
lsb_decoded_text = binary_to_text(lsb_message)
spread_spectrum_decoded_text = binary_to_text(spread_spectrum_message)

print("Decoded message using the hybrid algorithm:")
print(lsb_decoded_text)
