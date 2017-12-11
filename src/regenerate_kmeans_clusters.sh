#!/bin/sh

d='../externals/miniplaces_challenge/data/images'

# Clustering over feature vectors that were obtained from summary of activations.
for f in feature_vectors/val*txt; do
  cmd="python cluster_by_feature_vector-kmeans.py -i $d -fv $f > clusters-kmeans/$(basename $f)"
  echo "Running \"$cmd\""
  eval $cmd
done

# Baseline: clustering using perceptual hashes.
num_clusters=256
echo "generating ahash clusters..."
python cluster_by_image.py -i ${d}/val/ -ih ahash -nc $num_clusters > clusters-kmeans/ahash_${num_clusters}_clusters.txt

echo "generating dhash clusters..."
python cluster_by_image.py -i ${d}/val -ih dhash -nc $num_clusters > clusters-kmeans/dhash_${num_clusters}_clusters.txt

echo "generating phash clusters..."
python cluster_by_image.py -i ${d}/val -ih phash -nc $num_clusters > clusters-kmeans/phash_${num_clusters}_clusters.txt

echo "generating whash clusters..."
python cluster_by_image.py -i ${d}/val -ih whash -nc $num_clusters > clusters-kmeans/whash_${num_clusters}_clusters.txt

echo "done."
