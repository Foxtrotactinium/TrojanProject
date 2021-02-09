import os

import qrcode
from PIL import Image, ImageDraw, ImageFont


def insert_newlines(string, every=30):
    return '\n'.join(string[i:i + every] for i in range(0, len(string), every))


def print_label(partNo, desc):
    out = Image.new("RGB", (696, 271), (255, 255, 255))

    fontsize = 1  # starting font size
    fnt = ImageFont.truetype("arial.ttf", fontsize)
    while fnt.getsize(partNo)[0] < 450:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        fnt = ImageFont.truetype("arial.ttf", fontsize)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    fnt = ImageFont.truetype("arial.ttf", fontsize)

    fnt_small = ImageFont.truetype("arial.ttf", 30)

    d = ImageDraw.Draw(out)
    d.multiline_text((20, 20), partNo, font=fnt, fill=(0, 0, 0))

    d.multiline_text((20, 180), insert_newlines(desc), font=fnt_small, fill=(0, 0, 0))

    qr = qrcode.QRCode(box_size=7)
    qr.add_data(partNo)
    qr.make()
    img_qr = qr.make_image()

    pos = (out.size[0] - img_qr.size[0], -20)
    out.paste(img_qr, pos)

    out.save('tempPrint.png')

    os.system('brother_ql -p tcp://172.16.10.60:9100 -m QL-720NW print -l 62x29 tempPrint.png')

    os.remove('tempPrint.png')
