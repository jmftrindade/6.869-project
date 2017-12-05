#!/bin/sh

# e.g., "val/00000001.jpg"
image=$1
miniplaces_dir=../externals/miniplaces_challenge
miniplaces_data_dir=$miniplaces_dir/data
images_dir=$miniplaces_data_dir/images/

for f in clusters-kmeans/*; do
  cluster=`cat $f | grep "$image"`;
  cluster_montage=/tmp/$(basename ${image%.*})-cluster-$(basename ${f%.*}).jpg
  echo ""
  echo "retrieving cluster for image \"$image\" from \"$f\"..."
  cmd="python image_montage.py -ix 128 -iy 128 -o $cluster_montage -i $cluster"
#  echo "running $cmd"
  eval $cmd
#  echo "$f:"
#  echo "$cluster"
done

class_number=`grep $image $miniplaces_data_dir/*txt | cut -d' ' -f2`
class=`grep " $class_number" $miniplaces_data_dir/categories.txt`
echo ""
echo "class=$class"

preds_dir=$miniplaces_dir/weighted_majority/validation
resnet_preds=$preds_dir/resnet_predictions.txt
inception_preds=$preds_dir/inception_predictions.txt

echo ""
echo "resnet predictions:"
grep $image $resnet_preds

echo ""
echo "inception predictions:"
grep $image $inception_preds
