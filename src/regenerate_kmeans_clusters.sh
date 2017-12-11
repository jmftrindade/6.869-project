#!/bin/sh

d='../externals/miniplaces_challenge/data/images'

# Clustering over feature vectors that were obtained from summary of activations.
for f in feature_vectors/val*txt; do
  cmd="python cluster_by_feature_vector-kmeans.py -i $d -fv $f > clusters-kmeans/$(basename $f)"
  echo "Running \"$cmd\""
  eval $cmd
done

# Baseline: clustering using perceptual hashes.
echo "generating ahash clusters..."
python cluster_by_image.py -i ${d}/val/ -ih ahash -nc 100 > clusters-kmeans/ahash_100_clusters.txt

echo "generating dhash clusters..."
python cluster_by_image.py -i ${d}/val -ih dhash -nc 100 > clusters-kmeans/dhash_100_clusters.txt

echo "generating phash clusters..."
python cluster_by_image.py -i ${d}/val -ih phash -nc 100 > clusters-kmeans/phash_100_clusters.txt

echo "generating whash clusters..."
python cluster_by_image.py -i ${d}/val -ih whash -nc 100 > clusters-kmeans/whash_100_clusters.txt

echo "done."
