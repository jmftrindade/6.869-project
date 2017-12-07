import argparse
import operator
import os
from operator import itemgetter
import pandas as pd
import sklearn
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import sys


class Cluster:

        def __init__(self, image_paths):
            self.images = image_paths

        def __str__(self):
            return ' '.join([i for i in self.images])


# Copy-pasta from my util.py on model-diagnosis: use that module instead.
def cluster_kmeans(df, colnames_to_ignore=[], k=5):
    """
    df: DataFrame with one feature per column.
    colnames_to_ignore: Columns to ignore when fitting the k-means transform.
    k: Number of columns for k-means clustering.
    Returns:
    One Dataframe per cluster.
    """
    mat = df.drop(colnames_to_ignore, axis=1).as_matrix()
    # random_state set so that we deterministically return the same clusters.
    km = KMeans(n_clusters=k, random_state=42, init='k-means++')
    km.fit(mat)
    predict = km.predict(mat)

    df2 = df.copy()
    df2['cluster_label'] = pd.Series(predict, index=df2.index)

    return [d.drop('cluster_label', axis=1)
            for _, d in df2.groupby(['cluster_label'])]


def build_clusters(input_dir, feature_vector_file):
        clusters = []

        # XXX: Assumes feature vector is space separated file without header.
        df = pd.read_csv(feature_vector_file, sep=' ', header=None)
        df.dropna(inplace=True)

        colnames = ['unit_' + str(c - 1) for c in df.columns]
        colnames[0] = 'image_path'
        df.columns = colnames
        df['image_path'] = df['image_path'].apply(
            lambda x: os.path.join(input_dir, x))

        # Let's cluster these guys by the number of units on the layer.
        k = len(df.columns) - 1
        kc = cluster_kmeans(df, colnames_to_ignore=['image_path'], k=k)
        clusters = []
        for c in kc:
            # Remove the original feature_vector, now that we're not looking
            # at it (we're using kmeans to compute the clusters).
            clusters.append(Cluster(c['image_path']))
        print_clusters(clusters)


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
    feature_vector_file = kwargs.get('feature_vector_file')

    print 'clustering...'
    build_clusters(input_dir, feature_vector_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Outputs clusters of similar '
                                     'images.')
    parser.add_argument('-i', '--input_dir',
                        help='Relative path of directory with input images.',
                        required=True)
    parser.add_argument('-fv', '--feature_vector_file',
                        help='Relative path of file with images.',
                        required=True)

    args = parser.parse_args()
    main(**vars(args))
