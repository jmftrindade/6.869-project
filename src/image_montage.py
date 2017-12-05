import argparse
import cv2
from imutils import build_montages
import math


def make_montage(x, y, input_images, output_montage):
    images = []
    for image_path in input_images:
        image = cv2.imread(image_path)
        images.append(image)

    num_cols = 12
    num_rows = int(math.ceil(float(len(images)) / float(num_cols)))
    montages = build_montages(images, (x, y), (num_cols, num_rows))

    for montage in montages:
        cv2.imwrite(output_montage, montage)


def main(**kwargs):
    x = kwargs.get('x_dimension')
    y = kwargs.get('y_dimension')
    input_images = kwargs.get('input_images')
    output_montage = kwargs.get('output_montage')

    print 'saving montage under %s...' % output_montage
    make_montage(x, y, input_images, output_montage)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Makes montage of images.')
    parser.add_argument('-ix', '--x_dimension',
                        help='X dimension of input images.',
                        type=int,
                        default=128,
                        required=True)
    parser.add_argument('-iy', '--y_dimension',
                        help='Y dimension of input images.',
                        type=int,
                        default=128,
                        required=True)
    parser.add_argument('-i', '--input_images',
                        help='List with relative paths of input images.',
                        nargs='+',
                        required=True)
    parser.add_argument('-o', '--output_montage',
                        help='Relative path of image montage file.',
                        required=True)

    args = parser.parse_args()
    main(**vars(args))
