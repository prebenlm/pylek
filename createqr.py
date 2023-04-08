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

def add_label_to_image(image, label_text):
    img_width, img_height = image.size
    font_size = 20
    
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    label_height = font.getsize(label_text)[1] + 10

    new_img = Image.new("RGB", (img_width, img_height + label_height), "white")
    new_img.paste(image, (0, 0))
    draw = ImageDraw.Draw(new_img)
    text_width, text_height = draw.textsize(label_text, font)
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