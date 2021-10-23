from PIL import Image, ImageDraw, ImageFont
from random import randint, sample
import string


# captcha maker function
def captcha(color_bg):
    text = ''.join(sample(list(10 * string.digits + string.ascii_letters), 5))
    captcha_img = Image.new('RGB', (150, 45), color_bg)
    draw = ImageDraw.Draw(captcha_img)
    font = ImageFont.truetype('Assets/roboto/Roboto-Italic.ttf', 30)
    draw.text((25, 5), text, fill=(randint(0, 256), randint(0, 256), randint(0, 256)), font=font, stroke_width=2,
              stroke_fill="Black")

    draw.line(((randint(0, 5), 25), (randint(130, 150), 25)), fill='black', width=1)
    draw.line(((randint(0, 5), randint(0, 25)), (randint(130, 150), randint(0, 25))), fill='black', width=2)
    draw.line(((randint(0, 50), 0), (randint(100, 150), 50)), fill='green', width=2)
    draw.line(((randint(0, 50), randint(10, 50)), (randint(60, 150), randint(10, 50))), fill='blue', width=2)
    draw.line(((randint(0, 10), randint(0, 10)), (randint(60, 150), randint(40, 50))), fill='red', width=2)

    return captcha_img, text
