import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import re

def create_qr_code(text, output_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=12,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="transparent")
    return img

def get_font_path():
    if os.sys.platform.startswith('win'):
        font_path = 'C:\\Windows\\Fonts\\courbd.ttf'
    elif os.sys.platform.startswith('darwin'):
        font_path = '/System/Library/Fonts/Supplemental/Courier New Bold.ttf'
    elif os.sys.platform.startswith('linux'):
        font_path = '/usr/share/fonts/truetype/msttcorefonts/courbd.ttf'
    else:
        raise Exception("Unsupported platform")
    return font_path

def add_label_to_image(image, label_text):
    img_width, img_height = image.size
    font_size = 35
    font_path = get_font_path()
    padding = 10
    border_thickness = 10

    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        font = ImageFont.load_default()

    _, _, _, label_height = font.getbbox(label_text)
    label_height += padding * 2

    new_img = Image.new("RGBA", (img_width + 2 * border_thickness, img_height + label_height + border_thickness * 2), (255, 255, 255, 0))
    new_img.paste(image, (border_thickness, border_thickness), image)
    draw = ImageDraw.Draw(new_img)
    text_bbox = draw.textbbox((0, 0), label_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]

    # Draw black background for the label text
    draw.rectangle([(0, img_height + border_thickness), (img_width + 2 * border_thickness, img_height + label_height + border_thickness + padding)], fill="black")
    
    # Draw white label text on the black background
    draw.text(((img_width - text_width) / 2 + border_thickness, img_height + border_thickness + padding), label_text, font=font, fill="white")

    # Draw black borders around the QR-code image
    draw.rectangle([(0, 0), (img_width + 2 * border_thickness, border_thickness)], fill="black")  # top border
    draw.rectangle([(0, 0), (border_thickness, img_height + border_thickness)], fill="black")  # left border
    draw.rectangle([(img_width + border_thickness, 0), (img_width + 2 * border_thickness, img_height + border_thickness)], fill="black")  # right border

    return new_img


def main():
    input_filename = "qr_codes_data.txt"
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    with open(input_filename, "r") as file:
        for line in file:
            qr_text = line.strip()
            if not qr_text:
                continue

            # Check if the line starts with a letter or number followed by an underscore
            if re.match(r"^[A-Za-z0-9]_", qr_text):
                label_text = qr_text[2:]
            else:
                label_text = qr_text

            qr_image = create_qr_code(qr_text, output_folder)
            qr_image_with_label = add_label_to_image(qr_image, label_text)

            output_filename = os.path.join(output_folder, f"QR_{qr_text}.png")
            qr_image_with_label.save(output_filename)

if __name__ == "__main__":
    main()