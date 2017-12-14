#!/bin/sh

layer=conv5
class=36

# Temp text files.
cat ../externals/miniplaces_challenge/data/val.txt | cut -d' ' -f1,2 > /tmp/labels.txt
cat predictions/val_predictions.txt | cut -d' ' -f2 > /tmp/preds.txt
cat feature_vectors/val_avg_${layer}_activations.txt | cut -d' ' -f2- > /tmp/avg_${layer}.txt
paste -d' ' /tmp/labels.txt /tmp/preds.txt /tmp/avg_conv1.txt  > /tmp/histogram.txt

# Generate histograms (saved under /tmp).
out_dir=/tmp/histograms/${layer}
mkdir -p $out_dir
python compute_per_class_histograms.py -i /tmp/histogram.txt -c $class -o $out_dir #--normalize_counts

# Cleanup temp text files.
rm /tmp/labels.txt /tmp/avg_${layer}.txt /tmp/preds.txt /tmp/histogram.txt
