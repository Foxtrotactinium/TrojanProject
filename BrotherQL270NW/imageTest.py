import os

import qrcode
from PIL import Image, ImageDraw, ImageFont


def insert_newlines(string, every=64):
    return '\n'.join(string[i:i + every] for i in range(0, len(string), every))


def print_label(partNo, desc):
    out = Image.new("RGB", (696, 271), (255, 255, 255))

    fnt = ImageFont.truetype("arial.ttf", 40)
    fnt_small = ImageFont.truetype("arial.ttf", 20)

    d = ImageDraw.Draw(out)
    d.multiline_text((40, 40), partNo, font=fnt, fill=(0, 0, 0))

    d.multiline_text((40, 180), insert_newlines(desc), font=fnt_small, fill=(0, 0, 0))

    qr = qrcode.QRCode(box_size=6)
    qr.add_data(partNo)
    qr.make()
    img_qr = qr.make_image()

    pos = (out.size[0] - img_qr.size[0], 0)
    out.paste(img_qr, pos)

    out.save('tempPrint.png')

    os.system('brother_ql -p tcp://10.0.0.68:9100 -m QL-720NW print -l 62x29 tempPrint.png')

    os.remove('tempPrint.png')