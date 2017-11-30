import argparse
import glob
import imagehash
import os
from operator import itemgetter
from PIL import Image
import math
import operator


class Cluster:

        def __init__(self, image_filename, image_phash):
            self.centroid = image_phash
            self.images = [image_filename]

        def __str__(self):
            return ' '.join([i for i in self.images])

        def add_image(self, image):
            self.images.append(image)


def is_similar(centroid, image_phash, threshold):
        # Bitwise count.
        h, d = 0, centroid ^ image_phash
        while d:
            h += 1
            d &= d - 1
#        print 'h=%s' % h
        if h > threshold:
            return False
        return True


# XXX: Use imagehash's impl instead.
def avhash(image):
        im = image.resize((8, 8), Image.ANTIALIAS).convert('L')
        avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
        return reduce(lambda x, (y, z): x | (z << y),
                      enumerate(map(lambda i: 0 if i <
                                    avg else 1, im.getdata())),
                      0)


# XXX: Similarity threshold is heavily dependent on distance measure.
def clustering(input_dir, threshold):
        image_paths = get_image_paths(input_dir)

        # XXX: After this many it gets super slow.
        num_files = len(image_paths)
        max_files = 1000
        if num_files > max_files:
            image_paths = image_paths[:max_files]

        clusters = []
        count = 0
        step = 20
        for image_path in image_paths:
            found_similar = False
            try:
                image = Image.open(image_path)
                h = avhash(image)  # FIXME: use other imagehash here
            except:
                continue
            finally:
                image.close()

            # XXX: currently poor-man's seeding of initial centroids,
            # should change it to proper kmeans or kmeans++ instead
            for cluster in clusters:
               if is_similar(cluster.centroid, h, threshold):
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
    threshold = kwargs.get('threshold')
    threshold = 20 if threshold is None else float(threshold)
    clustering(input_dir, threshold)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Outputs clusters of similar '
                                     'images.')
    parser.add_argument('-i', '--input_dir',
                        help='Relative path of directory with input images.',
                        required=True)

    args = parser.parse_args()
    main(**vars(args))
