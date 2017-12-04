import argparse
import glob
import operator
import os
from operator import itemgetter
import sklearn
from sklearn import metrics

class Cluster:

        def __init__(self, image_path, feature_vector):
            self.centroid_feature_vector = feature_vector
            self.images = [image_path]

        def __str__(self):
            return ' '.join([i for i in self.images])

        def add_image(self, image):
            self.images.append(image)


def is_similar(centroid_feature_vector, image_feature_vector, threshold):
    cd = metrics.pairwise.cosine_distances(centroid_feature_vector,
            image_feature_vector)
    ed = metrics.pairwise.euclidean_distances(centroid_feature_vector,
            image_feature_vector)
    cs = metrics.pairwise.cosine_similarity(centroid_feature_vector,
            image_feature_vector)

#    print 'cos dist = %s, cos sim = %s, euclidean dist = %s' % (cd, cs, ed)

    return cd < threshold


# This is linear on the number of clusters created, which is of course
# correlated with the similarity threshold.
def build_clusters(input_dir, feature_vector_file, threshold):
        clusters = []
        count = 0
        step = 100

        with open(feature_vector_file) as f:
            for line in f:
                # <image_name> <fv_dim0> <fv_dim1> ... <fv_dimN>\n
                tokens = line.rstrip().split(' ')
                tokens = [t for t in tokens if t != '']
                if len(tokens) == 0:
                    continue

                image_path = os.path.join(input_dir, tokens[0])
                feature_vector = [tokens[1:]]
                if len(feature_vector) == 0:
                    sys.exit('Exiting: no feature vector for %s' % image_path)

                found_similar = False
                # XXX: currently poor-man's seeding of initial centroids,
                # should change it to proper kmeans or kmeans++ instead
                for cluster in clusters:
                   if is_similar(cluster.centroid_feature_vector,
                                 feature_vector,
                                 threshold):
                        cluster.add_image(image_path)
                        found_similar = True
                        break

                if not found_similar:
                    clusters.append(Cluster(image_path, feature_vector))

                count += 1
                if count % step == 0:
                    print 'finished processing %s images' % count

        print_clusters(clusters)


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
    feature_vector_file = kwargs.get('feature_vector_file')
    threshold = kwargs.get('threshold')

    # XXX: Cosine distance heuristic.
    threshold = 0.3 if threshold is None else float(threshold)

    build_clusters(input_dir, feature_vector_file, threshold)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Outputs clusters of similar '
                                     'images.')
    parser.add_argument('-i', '--input_dir',
                        help='Relative path of directory with input images.',
                        required=True)
    parser.add_argument('-fv', '--feature_vector_file',
                        help='Relative path of file with images.',
                        required=True)
    parser.add_argument('-t', '--threshold',
                        help='Similarity threshold for cosine distance.')

    args = parser.parse_args()
    main(**vars(args))
