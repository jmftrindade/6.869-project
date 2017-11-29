import argparse
import glob
import imagehash
import os
from PIL import Image
import sys


def get_image_paths(input_dir):
    images = []
    for e in ['*.gif', '*.jpg', '*.png']:
        images.extend(glob.glob(os.path.join(input_dir, e)))

    return sorted(images)


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

    # Default is wavelength hash.
    return imagehash.whash


def main(**kwargs):
    image_hash = kwargs.get('image_hash')
    input_dir = kwargs.get('input_dir')

    image_paths = get_image_paths(input_dir)
    image_hash_fn = get_image_hash_fn(image_hash)

    print 'Building similarity index using "%s"...' % image_hash
    index = create_similarity_index(image_paths, image_hash_fn)

    if index is None:
        print 'No similar images found.'
        return

    print 'similar images:'
    for k, v in index.iteritems():
        print ' '.join(v)


def create_similarity_index(image_paths, image_hash_fn):
    images_index = {}
    for f in image_paths:
        try:
            h = image_hash_fn(Image.open(f))
        except Exception as e:
            print 'Could not hash image %s: "%s"' % (f, e)

        # XXX: This is currently an exact match, which only works variations
        # of average hash.  For dhash and phash, we actually need to look at
        # the difference.
        images_index[h] = images_index.get(h, []) + [f]

    # No 2 images are similar.
    if len(images_index) == len(image_paths):
        return None

    return images_index


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Outputs list of similar '
                                     'images.')
    parser.add_argument('-i', '--input_dir',
                        help='Relative path of directory with input images.',
                        required=True)
    parser.add_argument('-ih', '--image_hash',
                        choices=['ahash', 'dhash', 'phash', 'whash'],
                        dest='image_hash',
                        action='store',
                        help='Type of hashing function to use for similarity.',
                        required=True)

    args = parser.parse_args()
    main(**vars(args))
