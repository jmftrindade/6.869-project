import argparse
import cv2
from imutils import build_montages
import math


def add_labels(image, class_name, prediction_name, bg_color):
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
    padding_w = 1
    padding_h = 5

    # Add class label on top left corner.
    class_text_size = cv2.getTextSize(
        'L:' + class_name, font, scale, thickness)[0]
    class_start = (1, 12)
    c_w = class_start[0] + class_text_size[0]
    c_h = class_start[1] - class_text_size[1]
    cv2.rectangle(image_copy, (class_start[0] - padding_w,
                               class_start[1] + padding_h), (c_w, c_h), bg_color, -1)
    cv2.putText(image_copy, 'L:' + class_name, class_start, font,
                scale, text_color, thickness, cv2.LINE_AA)

    # Add prediction right below class label.
    pred_text_size = cv2.getTextSize(
        'P:' + prediction_name, font, scale, thickness)[0]
    # right below class label
    pred_start = (1, class_start[1] + class_text_size[1] + padding_h)
    p_w = pred_start[0] + pred_text_size[0]
    p_h = pred_start[1] - pred_text_size[1]
    cv2.rectangle(image_copy, (pred_start[0] - padding_w,
                               pred_start[1] + padding_h), (p_w, p_h), bg_color, -1)
    cv2.putText(image_copy, 'P:' + prediction_name, pred_start, font,
                scale, text_color, thickness, cv2.LINE_AA)
    return image_copy


def make_montage(x, y, original_class, input_images, class_names,
                 prediction_names, output_montage):
    images = []
    for i, image_path in enumerate(input_images):
        image = cv2.imread(image_path)
        class_label = class_names[i]
        prediction = prediction_names[i]

        # NOTE: OpenCV uses BGR instead of RGB
        bg_color = ([255, 0, 0] if class_label ==
                    original_class else [0, 0, 255])
        im = add_labels(image, class_label, prediction, bg_color)
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
    prediction_names = kwargs.get('prediction_names')

    if len(input_images) != len(class_names):
        sys.exit('Exiting: number of input images and class names do not match')

    if len(class_names) != len(prediction_names):
        sys.exit('Exiting: number of class names and prediction names do not match')

    original_class = kwargs.get('original_class')
    output_montage = kwargs.get('output_montage')

    print 'saving montage under %s...' % output_montage
    make_montage(x, y, original_class, input_images,
                 class_names, prediction_names, output_montage)


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
    parser.add_argument('-pn', '--prediction_names',
                        help='List with top1 class predictions for each image.',
                        nargs='+',
                        required=True)
    parser.add_argument('-o', '--output_montage',
                        help='Relative path of image montage file.',
                        required=True)

    args = parser.parse_args()
    main(**vars(args))
