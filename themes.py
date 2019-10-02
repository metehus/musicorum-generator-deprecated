import pylast
import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

API_KEY = os.getenv("LASTFM_KEY", 'xxx')


def get_img_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


class Themes:
    lastfm = None

    roboto_regular = None
    roboto_mono_medium = None
    roboto_cond_regular = None

    def __init__(self):
        self.lastfm = pylast.LastFMNetwork(api_key=API_KEY)
        self.roboto_regular = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 35)
        self.roboto_mono_medium = ImageFont.truetype("./fonts/RobotoMono-Medium.ttf", 12)
        self.roboto_cond_regular = ImageFont.truetype("./fonts/roboto-condensed.regular.ttf", 15)

    def get_list_from_type(self, user, top, period):
        lfm_user = self.lastfm.get_user(user)
        res_list = None
        # print(period)
        # print(top)
        if top == 'artists':
            res_list = lfm_user.get_top_artists(period, limit=37)
        if top == 'tracks':
            res_list = lfm_user.get_top_tracks(period, limit=37)
        if top == 'albums':
            res_list = lfm_user.get_top_albums(period, limit=37)
        if top == 'tags':
            res_list = lfm_user.get_top_tags(period, limit=37)

        return res_list

    def grid(self, user, size, top_type, period):
        img_size = 1000
        gradient_magnitude = 1.8
        img = Image.new('RGBA', (img_size, img_size))
        top = self.get_list_from_type(user=user, top=top_type, period=period)
        print(len(top))
        if size < 2 or size > 6:
            size = 3

        cover_size = round(img_size / size)

        # ph = Image.new('RGBA', (img_size, img_size), color=(255, 200, 130))

        pos = 0
        for i in range(size):
            y = (i * cover_size)
            for j in range(size):
                x = (j * cover_size)

                print(pos)
                if pos >= len(top):
                    cover = Image.new("RGB", (1, 1))
                else:
                    item = top[pos]
                    cover = get_img_from_url(item.item.get_cover_image(size=pylast.SIZE_EXTRA_LARGE))

                pos = pos + 1

                cover = cover.resize((cover_size, cover_size), Image.ANTIALIAS)

                img.paste(cover, (x, y))
                # img.paste(ph, (x, y))

        gradient = Image.new('L', (1, img_size), color=0xFF)

        for i in range(size):
            y = (i * cover_size)
            for yg in range(cover_size):
                gl = yg + y
                if gl >= img_size:
                    break
                gradient.putpixel((0, gl), int(255 * (1 - gradient_magnitude * float(yg) / cover_size)))
        alpha = gradient.resize((img_size, img_size))
        black_im = Image.new('RGBA', (img_size, img_size), color=0)  # i.e. black
        black_im.putalpha(alpha)
        black_im.resize((img_size, cover_size))
        img = Image.alpha_composite(img, black_im)

        draw = ImageDraw.Draw(img)

        pos = 0
        for i in range(size):
            for j in range(size):

                if pos < len(top):
                    item = top[pos]
                    tx = (j * cover_size) + 10
                    ty = (i * cover_size) + 20
                    draw.text((tx, ty), item.item.get_name(), font=self.roboto_cond_regular, fill=(255, 255, 255))

                pos = pos + 1

        return img

    def normal(user, modules):
        img = Image.new('RGBA', (600, 700))

