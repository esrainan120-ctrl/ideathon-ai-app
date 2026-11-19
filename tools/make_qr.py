"""Vitrion marka renklerinde QR kod üretir. Kullanım: python tools/make_qr.py <URL> <çıktı.png>"""
import sys
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

PRUSSIAN, TEAL, PASTEL, SILVER = (16, 58, 87), (48, 123, 142), (169, 211, 197), (206, 229, 214)

def main(url: str, out: str) -> None:
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=20, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=PRUSSIAN, back_color="white").convert("RGB")
    w, h = img.size
    # Ortada logo: damla + kesikli çizgiler (yüksek hata düzeltme sayesinde okunur kalır)
    d = ImageDraw.Draw(img)
    r = w // 9
    cx, cy = w // 2, h // 2
    d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=r // 3, fill="white")
    dr = int(r * 0.62)
    d.polygon([(cx, cy - dr * 1.25), (cx - dr * 0.78, cy + dr * 0.05), (cx + dr * 0.78, cy + dr * 0.05)], fill=TEAL)
    d.ellipse([cx - dr * 0.8, cy - dr * 0.55, cx + dr * 0.8, cy + dr * 0.95], fill=TEAL)
    for k in (0.1, 0.38, 0.66):
        y = cy + dr * k
        d.line([cx - dr * 0.45, y, cx + dr * 0.45, y], fill=SILVER, width=max(2, r // 22))
    # Alt bant: marka adı
    pad = 120
    card = Image.new("RGB", (w, h + pad), "white")
    card.paste(img, (0, 0))
    cd = ImageDraw.Draw(card)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 54)
        small = ImageFont.truetype("DejaVuSans.ttf", 30)
    except OSError:
        font = small = ImageFont.load_default()
    cd.rectangle([0, h, w, h + pad], fill=PRUSSIAN)
    cd.text((w // 2, h + 42), "vitrion", font=font, fill=PASTEL, anchor="mm")
    cd.text((w // 2, h + 90), "Akıllı filtre izleme · demo", font=small, fill=SILVER, anchor="mm")
    card.save(out)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
