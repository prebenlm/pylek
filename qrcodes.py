import cv2
from pyzbar import pyzbar
import pyheif
import numpy as np
import os
from var_dump import var_dump
# os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/home/madpre/.local/lib/python3.10/site-packages/cv2/qt/plugins"
# os.environ["QT_DEBUG_PLUGINS"] = "1"


def decode_qr_codes(frame):
    qr_codes = pyzbar.decode(frame)
    for qr_code in qr_codes:
        x, y, w, h = qr_code.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        var_dump(qr_code)

        data = qr_code.data.decode("utf-8")
        print(f'Position: x = {x} / y = {y} / w = {w} / h = {h} / tekst = {qr_code.data.decode("utf-8")}')
        cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame, [qr_code.data.decode("utf-8") for qr_code in qr_codes]



# Other functions (decode_qr_codes, etc.) remain the same

def heic_to_opencv_image(file_path):
    heif_file = pyheif.read(file_path)
    return cv2.cvtColor(
        cv2.imdecode(
            np.frombuffer(heif_file.data, dtype=np.uint8),
            cv2.IMREAD_COLOR),
        cv2.COLOR_RGB2BGR)

def main():
    # Replace this with the path to your HEIC image
    # image_path = "IMG_4285.HEIC"
    image_path = "IMG_4285.jpeg"

    # Load the HEIC image as an OpenCV image
    # frame = heic_to_opencv_image(heic_image_path)
    frame = cv2.imread(image_path)

    # Process the image and show the results
    frame, qr_codes = decode_qr_codes(frame)
    cv2.imshow("QR Code Scanner", frame)

    # Process the QR codes and update the overlay
    for qr_code in qr_codes:
        # Replace this with your custom logic to update the overlay
        print("QR code data:", qr_code)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()