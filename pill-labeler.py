import argparse
from PIL import Image, ImageDraw
import os
from numpy import inf
import logging

from constants import CENTER_X, CENTER_Y, CLASS_ID, WIDTH_X

logging.basicConfig(level=logging.INFO)


def scan(img, width, height, threshold=30):
    '''
    Scans an image from left to right, top to bottom.
    Returns the location of the top y axis of a pill in the image.

    :param img: Image to scan
    :type img: tuple(int, int, int)

    :param width: Width of image
    :type width: int

    :param height: Height of image
    :type height: int

    :param threshold: Cutoff to distinct object from a black background
    :type threshold: int

    :return: Location of the top y axis of a pill in img
    :rtype: int
    '''
    for y in range(height):
        for x in range(width):
            r, g, b = img[x, y]

            if (r > threshold and g > threshold and b > threshold):
                return y

    # If an image consists of a solid black color with no object
    return inf


def calc_relative_height(height, y):
    '''
    Converts pixels to a value between 0.0-1.0
    This value will be used to determine the height of the object
    in the training data.

    :param height: Height of image in pixels
    :type height: int

    :param y: top y pixel value of the object
    :type y: int

    :return: Height of the object in 0-1.0
    :rtype: float
    '''
    center = height/2
    shape_height = (center-y)*2

    return shape_height/height


def create_label_file(img_name, height_y, output_dir):
    '''
    Creates a label file for a pill image

    :param img_name: Name of image
    :type: img_name: str

    :param height_y: height of object along the y axis
    :type height_y: float

    :output_dir: Location to store the ouptut label
    :type output_dir: str

    :return: File name and direcotry of the output
    :rtype: str
    '''
    file_name = f'{os.path.splitext(img_name)[0]}.txt'
    output_file_name = os.path.join(output_dir, file_name)

    with open(output_file_name, 'w') as outfile:
        label = f'{CLASS_ID} {CENTER_X} {CENTER_Y} {WIDTH_X} {height_y}'
        outfile.write(label)

    return output_file_name


def main():
    parser = argparse.ArgumentParser(
        description='Create labels for pill data set')

    parser.add_argument(
        '--img_dir', help='Image directory of pill data set', required=True)
    parser.add_argument(
        '--label_out', help='Output directory to place the labels', required=True)

    args = parser.parse_args()
    BASE_IMG_DIR = args.img_dir
    LABEL_DIR = args.label_out

    images = os.listdir(BASE_IMG_DIR)

    for file in images:
        logging.info(f'Processing {file}')
        img_path = os.path.join(BASE_IMG_DIR, file)
        img = Image.open(img_path)

        loaded_img = img.load()

        y = scan(loaded_img, img.width, img.height)
        logging.debug(f'Found y: {y}px')

        relative_height = calc_relative_height(img.height, y)
        logging.debug(f'Relative y: {relative_height}')

        create_label_file(file, relative_height, LABEL_DIR)

        logging.info(f'Created label')
        print()

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            # To draw the shapes around the pill
            draw = ImageDraw.Draw(img)
            draw.line((0, y, img.width, y))
            draw.line((0, img.height-y, img.width, img.height-y))
            img.show()


if __name__ == '__main__':
    main()
