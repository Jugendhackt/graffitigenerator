from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops
import sys
import os
import random

fonts = ['font1.ttf', 'font3.otf']

img2 = Image.open('texture.png', 'r')
W = img2.size[0]
H = img2.size[1]
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))

text = sys.argv[1]

draw = ImageDraw.Draw(img)
fnt = random.choice(fonts)

def drawCenterText(txt, fill='#fff', stroke='#333', sw=0):
    tf = ImageFont.truetype(fnt, 10)
    w, h = draw.textsize(txt, font=tf)
    print('Width:', w, '\n', 'IWidth:', W)
    font = ImageFont.truetype(fnt, round(W / w * 10))
    tw, th = draw.textsize(txt, font=font)
    draw.text(((W-tw)/2, (H-th)/2), txt, fill=fill, font=font, stroke_fill=stroke, stroke_width=sw)


stroke = (random.randint(20, 150),
          random.randint(20, 150),
          random.randint(20, 150))

drawCenterText("DeepGraffiti", stroke=stroke, sw=50)

pix = img.load()
pix2 = img2.load()

img.save('.temp.png')

os.system('convert texture.png .temp.png -compose Multiply -composite .temp2.png')
os.system('convert .temp2.png .temp.png -compose copy-opacity -composite final.png')

os.remove('.temp.png')
os.remove('.temp2.png')
