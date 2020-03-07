from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops
import sys
import os
import random

fontfiles = list(map(lambda x: 'fonts/' + x, os.listdir('fonts')))
fonts = list(filter(lambda x: x.endswith('.otf') or x.endswith('.ttf'), fontfiles))

if len(fonts) == 0:
    print("no fonts found in fonts/, exiting")
    sys.exit(-1)

print("loaded fonts:", " ".join(fonts))
fnt = random.choice(fonts)

img2 = Image.open('texture.png', 'r')
W = img2.size[0]
H = img2.size[1]
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))

text = input()
if not text:
    text = "DeepGraffiti"

draw = ImageDraw.Draw(img)

def drawCenterText(txt, fill='#fff', stroke='#333', sw=0):
    tf = ImageFont.truetype(fnt, 10)
    w, h = draw.textsize(txt, font=tf)
    font = ImageFont.truetype(fnt, round(W / w * 10))
    tw, th = draw.textsize(txt, font=font)
    draw.text(((W-tw)/2, (H-th)/2), txt, fill=fill, font=font, stroke_fill=stroke, stroke_width=sw)


stroke = (random.randint(20, 150),
          random.randint(20, 150),
          random.randint(20, 150))

drawCenterText(text, stroke=stroke, sw=50)

pix = img.load()
pix2 = img2.load()

img.save('.temp.png')

os.system('convert texture.png .temp.png -compose Multiply -composite .temp2.png')
os.system('convert .temp2.png .temp.png -compose copy-opacity -composite final.png')

os.remove('.temp.png')
os.remove('.temp2.png')
