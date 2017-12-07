#!/bin/sh

d='../externals/miniplaces_challenge/data/images/'

for f in feature_vectors/val*txt; do
  cmd="python cluster_by_feature_vector-kmeans.py -i $d -fv $f > clusters-kmeans/$(basename $f)"
  echo "Running \"$cmd\""
  eval $cmd
done
