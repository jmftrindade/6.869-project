import argparse
import glob
import imagehash
import os
from operator import itemgetter
from PIL import Image
import operator


class Cluster:

        def __init__(self, image_path, image_hash):
            self.centroid_hash = image_hash
            self.images = [image_path]

        def __str__(self):
            return ' '.join([i for i in self.images])

        def add_image(self, image):
            self.images.append(image)


def is_similar(centroid_hash, image_hash, threshold):
    return abs(centroid_hash - image_hash) < threshold


# XXX: Similarity threshold is heavily dependent on distance measure.
# This is linear on the number of clusters created, which is of course
# correlated with the similarity threshold.
def build_clusters(input_dir, image_hash_fn, threshold):
        image_paths = get_image_paths(input_dir)

        clusters = []
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

            # XXX: currently poor-man's seeding of initial centroids,
            # should change it to proper kmeans or kmeans++ instead
            for cluster in clusters:
               if is_similar(cluster.centroid_hash, h, threshold):
                    cluster.add_image(image_path)
                    found_similar = True
                    break

            if not found_similar:
                clusters.append(Cluster(image_path, h))

            count += 1
            if count % step == 0:
                print 'finished processing %s images' % count

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
            print 'cluster %s:' % cluster_number
            print c[0]
            cluster_number += 1


def main(**kwargs):
    input_dir = kwargs.get('input_dir')
    image_hash = kwargs.get('image_hash')
    image_hash_fn = get_image_hash_fn(image_hash)
    threshold = kwargs.get('threshold')
    threshold = 10 if threshold is None else float(threshold)

    build_clusters(input_dir, image_hash_fn, threshold)


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
    parser.add_argument('-t', '--threshold',
                        help='Similarity threshold.')

    args = parser.parse_args()
    main(**vars(args))
