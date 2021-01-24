import os
import json
import argparse
import random
from PIL import Image, ImageDraw, ImageFont

class CharDataset():
    def __init__(self, char_file, font_file, font_dir, img_size=(128, 128)):
        """Initialize the CharDataset class.

        Parameters:
            char_file (str) -- the name of the character file to read, should be in json format.
            font_file (str) -- the name of the font file to read, should be in json format.\
            font_dir (str) -- the directory of all the font files.
            img_size ((int, int)) -- the height and width of the output image, respectively.
        """
        self.char_list = self.read_char_file(char_file)
        self.min_size = min(*img_size)
        self.font_dict = self.parse_font_file(font_file, font_dir)
        self.img_size = img_size

    def __len__(self):
        return len(self.font_list)

    def gen_test_data(self, root_dir, num_imgs):
        content_dir = os.path.join(root_dir, 'images_content')
        style_dir = os.path.join(root_dir, 'images_style')
        os.makedirs(content_dir, exist_ok=True)
        os.makedirs(style_dir, exist_ok=True)
        for i in range(num_imgs):
            filename, font, offsets = random.choice(self.font_dict['images_content'])
            offsets = tuple(r*s for r, s in zip(offsets, self.img_size))
            raw_char = random.choice(self.char_list)
            ch = self.get_char(raw_char)
            img = self.get_char_img(ch, font, self.img_size, offsets)
            img.save(os.path.join(content_dir, f'{i}.png'))
        for i in range(num_imgs):
            filename, font, offsets = random.choice(self.font_dict['images_style'])
            offsets = tuple(r*s for r, s in zip(offsets, self.img_size))
            raw_char = random.choice(self.char_list)
            ch = self.get_char(raw_char)
            img = self.get_char_img(ch, font, self.img_size, offsets)
            img.save(os.path.join(style_dir, f'{i}.png'))


    def gen_dataset(self, root_dir):
        content_dir = os.path.join(root_dir, 'images_content')
        style_dir = os.path.join(root_dir, 'images_style')
        os.makedirs(content_dir, exist_ok=True)
        os.makedirs(style_dir, exist_ok=True)
        print('=========constructing images_content dataset=========')
        for filename, font, offsets in self.font_dict['images_content']:
            img_dir = os.path.join(content_dir, filename)
            os.makedirs(img_dir, exist_ok=True)
            print(f'generating images using font type [{filename}]')
            for i, img in enumerate(self.char_img_generator(font, offsets)):
                img.save(os.path.join(img_dir, f'{filename}_{i}.png'))
        print('==========constructing images_style dataset==========')
        for filename, font, offsets in self.font_dict['images_style']:
            img_dir = os.path.join(style_dir, filename)
            os.makedirs(img_dir, exist_ok=True)
            print(f'generating images using font type [{filename}]')
            for i, img in enumerate(self.char_img_generator(font, offsets)):
                img.save(os.path.join(img_dir, f'{filename}_{i}.png'))
        print('\ndone!')

    def char_img_generator(self, font, offsets):
        offsets = tuple(r*s for r, s in zip(offsets, self.img_size))
        for raw_char in self.char_list:
            ch = self.get_char(raw_char)
            img = self.get_char_img(ch, font, self.img_size, offsets)
            yield img

    @staticmethod
    def read_char_file(char_file):
        with open(char_file, 'r') as f:
            l = json.load(f)
        return l

    @staticmethod
    def get_font(font_file, size):
        return ImageFont.truetype(font_file, size)

    def parse_font_file(self, font_file, font_dir):
        with open(font_file, 'r') as f:
            d = json.load(f)
        d['images_content'] = self.get_font_list(d['images_content'], font_dir)
        d['images_style'] = self.get_font_list(d['images_style'], font_dir)
        return d
    
    def get_font_list(self, font_info, font_dir):
        font_list = []
        for filename, ratio, offsets in font_info:
            font = self.get_font(os.path.join(font_dir, filename), 
                                 int(ratio*self.min_size))
            font_list.append((filename[:-4], font, offsets))
        return font_list
    
    @staticmethod
    def get_char(unicode):
        int_unicode = int(unicode, 16)
        return chr(int_unicode)

    @staticmethod
    def get_char_img(ch, font, img_size, offsets=(0, 0)):
        img = Image.new("L", img_size, 255)
        draw = ImageDraw.Draw(img)
        draw.text(offsets, ch, 0, font=font)
        return img

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, required=True, help="generate images under this directory")
    parser.add_argument('--font_file', type=str, required=True, help="path to the font name list")
    parser.add_argument('--char_file', type=str, required=True, help="path to the character list")
    parser.add_argument('--font_dir', type=str, required=True, help="path to the directory that stores all the font types")
    parser.add_argument('--img_size', type=int, required=True, help="image size of the generated character")
    parser.add_argument('--test', action='store_true', help="generate test data")
    parser.add_argument('--num_imgs', type=int, default=10, help="how many pairs of test data to generate")
    return parser.parse_args()

def main(args):
    char_set = CharDataset(args.char_file, args.font_file, args.font_dir, (args.img_size, args.img_size))
    if args.test:
        char_set.gen_test_data(args.root_dir, args.num_imgs)
    else:
        char_set.gen_dataset(args.root_dir)

if __name__ == '__main__':
    args = process_command()
    main(args)
