#!/usr/bin/python3

from PIL import Image
import argparse
import io
import random

def apply_filter(filename, milk_type, eff, comp):
    def probably(chance):
        return random.random() < chance

    # Init constants
    color_map = {
        1: [(0, 0, 0), (102, 0, 31), (137, 0, 146)],
        2: [(0, 0, 0), (92, 36, 60), (203, 43, 43)]
    }
    colors = color_map[1] if milk_type == False else color_map[2]
    punt = 70 if eff else 100
    thresh_mid1, thresh_mid2 = (120, 200) if milk_type == False else (90, 150)

    # Prepare image 
    img = Image.open(filename)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    if comp > 0:
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=max(1, 100 - comp))
        buffer.seek(0)
        img = Image.open(buffer).convert('RGB')

    width, height = img.size

    # Load image pixels
    pixels = img.load()

    # Process image
    for y in range(height):
        for x in range(width):
            R, G, B = pixels[x, y]
            brightness = (R + G + B) / 3

            if brightness <= 25:
                pixels[x, y] = colors[0]
            elif brightness <= 70:
                pixels[x, y] = colors[0] if probably(punt / 100) else colors[1]
            elif brightness < thresh_mid1:
                pixels[x, y] = colors[1] if probably(punt / 100) else colors[0]
            elif brightness < thresh_mid2:
                pixels[x, y] = colors[1]
            elif brightness < 230:
                pixels[x, y] = colors[2] if probably(punt / 100) else colors[1]
            else:
                pixels[x, y] = colors[2]

    return img

def parse_args():
    parser = argparse.ArgumentParser(description="Milk image filter");
    parser.add_argument("-f", "--file", help="Specify input image.", required=True);
    parser.add_argument("-o", "--out", help="Specify out path.", required=True);
    parser.add_argument("-a", "--alt", help="Alternative Milk effect.", action='store_true', default=False)
    parser.add_argument("-p", "--pointism", help="Pointillism effect.", action='store_true', default=False);
    parser.add_argument("-c", "--comp", help="Compression. from 0 to 100. Defaults to 0.", default=0, type=int);
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    img = apply_filter(args.file, args.alt, args.pointism, args.comp)
    img.save(args.out)
