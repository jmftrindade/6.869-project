#!/bin/sh

d='../externals/miniplaces_challenge/data/images/'
for f in feature_vectors/*txt; do
  cmd="nohup python -u cluster_by_feature_vector-kmeans.py -i $d -fv $f > clusters-kmeans/$(basename $f) 2>&1"
  echo "Running:"
  echo "$cmd"
  echo ""
  eval $cmd
done
