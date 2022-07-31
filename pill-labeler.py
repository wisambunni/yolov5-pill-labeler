from fileinput import filename
from hashlib import new
from PIL import Image, ImageDraw
import os
from matplotlib.pyplot import text
from numpy import inf

from constants import IMG_DIR

# IMG_NAME = '0006-9117_0_0.jpg'
# IMG_NAME = '66993-057_0_1.jpg'
IMG_NAME = '0002-4464_0_0.jpg'

def scan(img, width, height):
    for y in range(height):
        for x in range(width):
            r = img[x, y][0]
            g = img[x, y][1]
            b = img[x, y][2]

            if (r > 30 and g > 30 and b > 30):
                return x, y

    return inf, inf


def transform_to_label(height, y):
    center = height/2
    shape_width = (center-y)*2

    return shape_width/height

def create_label_file(IMG_NAME, transform):
    new_name = os.path.splitext(IMG_NAME)[0]
    file_name = 'D:\Projects\yolov5-pill-labeler\\files\%s.txt' % new_name
    text_file = open(file_name,"w")

    text_file.write(f"0 0.5 0.5 1.0 {transform}")
    text_file.close()
    return

def main():
    IMG_PATH = os.path.join(IMG_DIR, IMG_NAME)

    img = Image.open(IMG_PATH)

    loaded_img = img.load()

    x, y = scan(loaded_img, img.width, img.height)

    # To draw the shapes around the pill
    # draw = ImageDraw.Draw(img)
    # draw.line((0, y, img.width, y))
    # draw.line((0, img.height-y, img.width, img.height-y))
    # img.show()
    
    transform = transform_to_label(img.height, y)

    create_file = create_label_file(IMG_NAME, transform)

    # print(x, y)

    # print(transform)


if __name__ == '__main__':
    main()

