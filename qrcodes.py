import cv2
import os
os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/opt/zbar/lib'
from pyzbar import pyzbar
import numpy as np
from var_dump import var_dump
import math
from PIL import Image
import pytesseract
# os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/home/madpre/.local/lib/python3.10/site-packages/cv2/qt/plugins"
# os.environ["QT_DEBUG_PLUGINS"] = "1"
def preprocess_image(frame):
    # Resize the image
    scale_percent = 200  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply adaptive threshold
    threshold = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(threshold, (5, 5), 0)
    # Dilate the image
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(blur, kernel, iterations=1)
    #cv2.imshow("QR Code Scanner", dilated)



    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return dilated


def detect_text(frame):
    # Convert OpenCV image to PIL image
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Use Tesseract to recognize text
    text = pytesseract.image_to_string(pil_image, lang='nor')
    var_dump(text)

    # Split the text into lines and process each line
    lines = text.strip().split('\n')
    names = []
    roles = []

    # Read names and roles from text files
    with open("names.txt", "r") as f:
        names_data = f.read().splitlines()

    with open("roles.txt", "r") as f:
        roles_data = f.read().splitlines()

    for line in lines:
        words = line.split()
        for word in words:
            if word in names_data:
                names.append(word)
            elif word in roles_data:
                roles.append(word)

    pairs = list(zip(names, roles))

    # Write pairs to a text file
    with open("paired_names_and_roles.txt", "w") as f:
        for pair in pairs:
            f.write(f"{pair[0]}: {pair[1]}\n")

    return frame, pairs

def decode_qr_codes(frame):
    # Detect QR codes in the frame
    decoded_objects = pyzbar.decode(frame)

    names = []
    roles = []
    
    
    # Read names and roles from text files
    with open("names.txt", "r") as f:
        names_data = f.read().splitlines()
    
    with open("roles.txt", "r") as f:
        roles_data = f.read().splitlines()

    # Iterate over decoded QR codes and store their positions
    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        var_dump(data)
        position = obj.rect

        x, y, w, h = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if data in names_data:
            names.append({"name": data, "position": position})
        elif data in roles_data:
            roles.append({"role": data, "position": position})

    # Function to calculate the distance between two positions
    def distance(a, b):
        return math.sqrt((a.left - b.left) ** 2 + (a.top - b.top) ** 2)

    # Pair names and roles
    pairs = []
    for name in names:
        closest_role = None
        min_distance = float("inf")
        for role in roles:
            dist = distance(name["position"], role["position"])
            if dist < min_distance:
                min_distance = dist
                closest_role = role

        if closest_role:
            pairs.append((name["name"], closest_role["role"]))
            roles.remove(closest_role)

    # Write pairs to a text file
    with open("paired_names_and_roles.txt", "w") as f:
        for pair in pairs:
            f.write(f"{pair[0]}: {pair[1]}\n")

    return frame, pairs

def main():
    # Replace this with the path to your HEIC image
    # image_path = "IMG_4285.HEIC"
    image_path = "IMG_4285.jpeg"

    # Load the HEIC image as an OpenCV image
    # frame = heic_to_opencv_image(heic_image_path)
    frame = cv2.imread(image_path)

    # Preprocess the image
    # preprocessed_frame = preprocess_image(frame)

    # Process the image and show the results
    frame, text_pairs = detect_text(frame)
    frame, qr_codes = decode_qr_codes(frame)
    for text_pair in text_pairs:
        print("Text pair:", text_pair)
    cv2.imshow("QR Code Scanner", frame)

    # Process the QR codes and update the overlay
    for qr_code in qr_codes:
        # Replace this with your custom logic to update the overlay
        print("QR code data:", qr_code)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

