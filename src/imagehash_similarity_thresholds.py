import argparse
from PIL import Image
import imagehash


def get_image_hash_fn(image_hash):
    # Average hash.
    if image_hash == 'ahash':
        return imagehash.average_hash

    # Difference hash.
    if image_hash == 'dhash':
        return imagehash.dhash

    # Perceptual hash.
    if image_hash == 'phash':
        return imagehash.phash

    if image_hash == 'whash':
        return imagehash.whash

    return None


def calc_rotated_diff(image_path):
    image = Image.open(image_path)

    for hash_name in ['ahash', 'dhash', 'phash', 'whash']:
        hash_fn = get_image_hash_fn(hash_name)
        h = hash_fn(image)
        print '\nhash diff for "%s"' % hash_name

        for r in range(1, 360, 15):
            rothash = hash_fn(image.rotate(r))
            print 'rotated by %s degrees: %s diff' % (r, h - rothash)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Outputs hash diff for '
                                     'different rotations of the same image.')
    parser.add_argument('-i', '--image_path',
                        help='Relative path of input image.',
                        required=True)

    args = parser.parse_args()
    calc_rotated_diff(**vars(args))
