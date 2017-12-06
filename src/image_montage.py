import argparse
import cv2
from imutils import build_montages
import math


def add_class_label(image, class_name, bg_color):
    # Add a border.
    image_copy = image.copy()
    image_copy = cv2.copyMakeBorder(
        image, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=bg_color)
    image_copy = cv2.copyMakeBorder(
        image_copy, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    # Add text label
    font = cv2.FONT_HERSHEY_DUPLEX
    scale = 0.4
    thickness = 1
    text_color = (255, 255, 255)
    text_size = cv2.getTextSize(class_name, font, scale, thickness)[0]
    label_start = (1, 12)
    w = label_start[0] + text_size[0]
    h = label_start[1] - text_size[1]

    # Add text label with background around it.
    cv2.rectangle(image_copy, (label_start[0] - 1,
                               label_start[1] + 5), (w, h), bg_color, -1)
    cv2.putText(image_copy, class_name, label_start, font,
                scale, text_color, thickness, cv2.LINE_AA)
    return image_copy


def make_montage(x, y, original_class, input_images, class_names, output_montage):
    images = []
    for i, image_path in enumerate(input_images):
        image = cv2.imread(image_path)
        label = class_names[i]

        # NOTE: OpenCV uses BGR instead of RGB
        bg_color = ([255, 0, 0] if label == original_class else [0, 0, 255])
        im = add_class_label(image, class_names[i], bg_color)
        images.append(im)

    num_cols = 8
    num_rows = int(math.ceil(float(len(images)) / float(num_cols)))
    montages = build_montages(images, (x, y), (num_cols, num_rows))

    for montage in montages:
        cv2.imwrite(output_montage, montage)


def main(**kwargs):
    x = kwargs.get('x_dimension')
    y = kwargs.get('y_dimension')
    input_images = kwargs.get('input_images')
    class_names = kwargs.get('class_names')

    if len(input_images) != len(class_names):
        sys.exit('Exiting: number of input images and class names do not match')

    original_class = kwargs.get('original_class')
    output_montage = kwargs.get('output_montage')

    print 'saving montage under %s...' % output_montage
    make_montage(x, y, original_class, input_images,
                 class_names, output_montage)


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
    parser.add_argument('-oc', '--original_class',
                        help='Class label of image for which this montage '
                        'was requested.',
                        required=True)
    parser.add_argument('-i', '--input_images',
                        help='List with relative paths of input images.',
                        nargs='+',
                        required=True)
    parser.add_argument('-cn', '--class_names',
                        help='List with names of true classes of each image.',
                        nargs='+',
                        required=True)
    parser.add_argument('-o', '--output_montage',
                        help='Relative path of image montage file.',
                        required=True)

    args = parser.parse_args()
    main(**vars(args))
