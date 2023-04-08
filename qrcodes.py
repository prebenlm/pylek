import cv2
import os
os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/opt/zbar/lib'
from pyzbar import pyzbar
import numpy as np
from var_dump import var_dump
import math
# os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/home/madpre/.local/lib/python3.10/site-packages/cv2/qt/plugins"
# os.environ["QT_DEBUG_PLUGINS"] = "1"

def decode_qr_codes(frame):
    # Detect QR codes in the frame
    decoded_objects = pyzbar.decode(frame)

    names = []
    roles = []
    #var_dump(decoded_objects)
    
    # Read names and roles from text files
    with open("names.txt", "r") as f:
        names_data = f.read().splitlines()
    
    with open("roles.txt", "r") as f:
        roles_data = f.read().splitlines()

    # Iterate over decoded QR codes and store their positions
    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        position = obj.rect
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

    # Process the image and show the results
    frame, qr_codes = decode_qr_codes(frame)
    #cv2.imshow("QR Code Scanner", frame)

    # Process the QR codes and update the overlay
    for qr_code in qr_codes:
        # Replace this with your custom logic to update the overlay
        print("QR code data:", qr_code)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

