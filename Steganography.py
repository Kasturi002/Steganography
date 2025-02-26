import cv2
import numpy as np
import random

def encode_message(image_path, secret_message, output_path):
    image = cv2.imread(image_path)
    
    secret_message += "###"  
    binary_message = ''.join(format(ord(i), '08b') for i in secret_message)

    rows, cols, channels = image.shape
    total_pixels = rows * cols

    if len(binary_message) > total_pixels * 3:
        raise ValueError("Message is too large to be hidden in this image")

    binary_index = 0
    for row in range(rows):
        for col in range(cols):
            for channel in range(3):  
                if binary_index < len(binary_message):
                    image[row, col, channel] = (image[row, col, channel] & ~1) | int(binary_message[binary_index])
                    binary_index += 1
 
    cv2.imwrite(output_path, image)
    print("Message successfully encoded and saved as", output_path)

def decode_message(image_path):
    image = cv2.imread(image_path)
    
    binary_message = ""
    for row in image:
        for pixel in row:
            for channel in pixel[:3]:  
                binary_message += str(channel & 1)

    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    extracted_message = ''.join(chr(int(char, 2)) for char in chars)

    extracted_message = extracted_message.split("###")[0]
    print("Decoded Message:", extracted_message)
    return extracted_message

if __name__ == "__main__":
    encode_message("input_image.png", "Hello, this is a secret!", "stego_image.png")

    decode_message("stego_image.png")
