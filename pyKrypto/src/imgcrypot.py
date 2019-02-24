from PIL import Image, ImageFont, ImageDraw


def img_create(message):
    message = message.replace('\n', ' ')
    font = ImageFont.truetype('consolab.ttf', 20)
    width, height = font.getsize(message)
    iwidth, iheight = width + 20, height + 8
    img = Image.new('RGBA', (iwidth, iheight), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 3), message, font=font, fill=(0, 255, 0))
    img.save('msg.png')


def load_message(filename):
    mesg = ''
    with open(filename, 'r', encoding='iso-8859-7') as fil:
        mesg = fil.read()
    return mesg


if __name__ == "__main__":
    fname = "/home/ted/prj/pyted/aa.txt"
    img_create(load_message(fname)[:90000])
