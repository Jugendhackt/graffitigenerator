from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops
import sys
import os
import random


def drawCenterText(txt, fnt, draw, W, H, fill='#fff', stroke='#333', sw=0):
    tf = ImageFont.truetype(fnt, 40)
    w, h = draw.textsize(txt, font=tf)
    if w/h > W/H:  # aspect wider
        newsize = round((W - 40) / w * 40)
    else:  # aspect higher
        newsize = round((H - 40) / h * 40)
    font = ImageFont.truetype(fnt, newsize)
    tw, th = draw.textsize(txt, font=font)
    x = (W-tw)/2 - 2
    y = (H-th)/2
    print("drawing text %dx%d at (%d,%d) in canvas %dx%d (scaled to %dpt from %dx%d)" % (
        tw, th, x, y, W, H, newsize, w, h))
    draw.text((x, y), txt, fill=fill, font=font,
              stroke_fill=stroke, stroke_width=sw)


def generate(text="DeepGraffiti", out="final.png", trim=True):
    fontfiles = map(lambda x: 'fonts/' + x, os.listdir('fonts'))
    fonts = list(filter(lambda x: x.endswith('.otf')
                        or x.endswith('.ttf'), fontfiles))

    texturefiles = map(lambda x: 'textures/' + x, os.listdir('textures'))
    textures = list(filter(lambda x: x.endswith('-small.png'), texturefiles))

    if len(fonts) == 0:
        print("no fonts found in fonts/, exiting")
        sys.exit(-1)

    if len(textures) == 0:
        print("no textures found in textures/, exiting")
        sys.exit(-1)

    print("loaded fonts:", " ".join(fonts))
    fnt = random.choice(fonts)

    print("loaded textures:", " ".join(fonts))
    texture = random.choice(textures)

    img2 = Image.open(texture, 'r')
    W = img2.size[0]
    H = img2.size[1]
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))

    if not text:
        text = "DeepGraffiti"

    draw = ImageDraw.Draw(img)

    stroke = (random.randint(20, 150),
              random.randint(20, 150),
              random.randint(20, 150))

    fill = (random.randint(200, 255),
            random.randint(200, 255),
            random.randint(200, 255))

    drawCenterText(text, fnt, draw, W, H, fill=fill, stroke=stroke, sw=10)

    pix = img.load()
    pix2 = img2.load()

    img.save('.temp.png')

    os.system(
        'convert %s .temp.png -compose Multiply -composite .temp2.png' % texture)
    if trim:
        os.system('convert .temp2.png .temp.png -compose copy-opacity -composite .temp3.png')
        os.system('convert .temp3.png -trim %s' % out)
        os.remove('.temp.png')
        os.remove('.temp2.png')
        os.remove('.temp3.png')
    else:
        os.system('convert .temp2.png .temp.png -compose copy-opacity -composite %s' % out)
        os.remove('.temp.png')
        os.remove('.temp2.png')
    