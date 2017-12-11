import argparse
import glob
import imagehash
import os
import operator
from operator import itemgetter
from PIL import Image
import random


class Cluster:

        def __init__(self, image_path, image_hash):
            self.centroid_hash = image_hash
            self.images = [image_path]

        def __str__(self):
            return ' '.join([i for i in self.images])

        def add_image(self, image):
            self.images.append(image)


def build_initial_clusters(image_paths, image_hash_fn, num_clusters):
    clusters = []

    # In-place shuffle.
    random.shuffle(image_paths)
    centroid_images = image_paths[0:num_clusters]

    for image_path in centroid_images:
        image = Image.open(image_path)
        h = image_hash_fn(image)
        clusters.append(Cluster(image_path, h))

    remaining_images = [i for i in image_paths if i not in centroid_images]

    return clusters, remaining_images


def build_clusters(input_dir, image_hash_fn, num_clusters):
        image_paths = get_image_paths(input_dir)
        clusters, remaining_images = build_initial_clusters(
            image_paths, image_hash_fn, num_clusters)
        image_paths = remaining_images

        print 'clustering images into %s clusters...' % len(clusters)

        count = 0
        step = 100
        for image_path in image_paths:
            found_similar = False
            try:
                image = Image.open(image_path)
                h = image_hash_fn(image)
            except:
                continue
            finally:
                image.close()

            min_diff = 999999  # arbitrarily large value
            centroid_idx = None
            for idx, cluster in enumerate(clusters):
                diff = abs(cluster.centroid_hash - h)

                if diff < min_diff:
                    centroid_idx = idx
                    min_diff = diff

            clusters[centroid_idx].add_image(image_path)

            count += 1
#            if count % step == 0:
#                print 'finished processing %s images' % count

        print_clusters(clusters)


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


def print_clusters(clusters):
        # Descending order by number of images in the cluster.
        sorted_clusters = []
        for c in clusters:
            sorted_clusters.append([c, len(c.images)])
        sorted_clusters.sort(key=itemgetter(1), reverse=True)

        cluster_number = 1
        for c in sorted_clusters:
            print '\ncluster %s:' % cluster_number
            print c[0]
            cluster_number += 1


def main(**kwargs):
    input_dir = kwargs.get('input_dir')
    image_hash = kwargs.get('image_hash')
    image_hash_fn = get_image_hash_fn(image_hash)
    num_clusters = kwargs.get('num_clusters')

    build_clusters(input_dir, image_hash_fn, num_clusters)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Outputs clusters of similar '
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
    parser.add_argument('-nc', '--num_clusters',
                        help='Number of clusters to build.',
                        type=int)

    args = parser.parse_args()
    main(**vars(args))
