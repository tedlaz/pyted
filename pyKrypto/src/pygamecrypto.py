from PIL import Image, ImageFont, ImageDraw
import pygame
import pygame.locals as lc
import sys
import os


def img_create(message):
    message = message.replace('\n', '')
    font = ImageFont.truetype('consolab.ttf', 20)
    width, height = font.getsize(message)
    iwidth, iheight = width + 20, height + 8
    img = Image.new('RGBA', (iwidth, iheight), (0, 0, 0, 100))
    draw = ImageDraw.Draw(img)
    draw.text((10, 3), message, font=font, fill=(0, 255, 0))
    return img
    # img.save('msg.jpg')


def events():
	for evt in pygame.event.get():
		if evt.type == lc.QUIT or (
                evt.type == lc.KEYDOWN and evt.key == lc.K_ESCAPE):
			pygame.quit()
			sys.exit()


def run(message):
    # define display surface			
    W, H = 576, 30
    HW, HH = W / 2, H / 2
    AREA = W * H
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    # setup pygame
    pygame.init()
    CLOCK = pygame.time.Clock()
    DS = pygame.display.set_mode((W, H), pygame.NOFRAME)
    # pygame.display.set_caption("code.Pylet - Scrolling Background Image")
    FPS = 80
    #bkgd = pygame.image.load("/home/ted/prj/pyted/msg.jpg").convert()
    img = img_create(message)
    bkgd = pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert()
    x = 0
    # main loop
    start = True
    while True:
        events()
        rel_x = x % bkgd.get_rect().width
        DS.blit(bkgd, (rel_x - bkgd.get_rect().width, 0))
        if rel_x < W:
            DS.blit(bkgd, (rel_x, 0))
        x -= 1
        pygame.display.update()
        if start:
            pygame.time.delay(1000)
            start = False
        CLOCK.tick(FPS)


def load_message(filename):
    mesg = ''
    with open(filename, 'r', encoding='utf-8') as fil:
        mesg = fil.read()
    return mesg



if __name__ == "__main__":
    fname = "/home/ted/prj/pyted/aa.txt"
    run("This is Ted Lazaros Speaking in front of you !!!")
