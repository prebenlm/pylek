import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def create_qr_code(text, output_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img

def get_arial_font_path():
    if os.sys.platform.startswith('win'):
        font_path = 'C:\\Windows\\Fonts\\arial.ttf'
    elif os.sys.platform.startswith('darwin'):
        font_path = '/System/Library/Fonts/Supplemental/Arial.ttf'
    elif os.sys.platform.startswith('linux'):
        font_path = '/usr/share/fonts/truetype/msttcorefonts/arial.ttf'
    else:
        raise Exception("Unsupported platform")
    return font_path

def add_label_to_image(image, label_text):
    img_width, img_height = image.size
    font_size = 50
    font_path = get_arial_font_path()

    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        font = ImageFont.load_default()

    _, _, _, label_height = font.getbbox(label_text)
    label_height += 10

    new_img = Image.new("RGB", (img_width, img_height + label_height), "white")
    new_img.paste(image, (0, 0))
    draw = ImageDraw.Draw(new_img)
    text_bbox = draw.textbbox((0, 0), label_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    draw.text(((img_width - text_width) / 2, img_height), label_text, font=font, fill="black")

    return new_img

def main():
    input_file = "qr_codes_data.txt"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        qr_text = line.strip()
        qr_image = create_qr_code(qr_text, output_dir)
        qr_image_with_label = add_label_to_image(qr_image, qr_text)
        output_path = os.path.join(output_dir, f"qr_code_{i + 1}.png")
        qr_image_with_label.save(output_path)

if __name__ == "__main__":
    main()