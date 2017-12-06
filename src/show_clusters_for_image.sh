#!/bin/sh

# e.g., "val/00000001.jpg"
image=$1
miniplaces_dir=../externals/miniplaces_challenge
miniplaces_data_dir=$miniplaces_dir/data
images_dir=$miniplaces_data_dir/images/

orig_class=`./show_class_for_image.sh $image | grep "class=" | cut -d'=' -f2`

for f in clusters-kmeans/*; do
  cluster=`cat $f | grep "$image"`;
  cluster_montage=/tmp/$(basename ${image%.*})-cluster-$(basename ${f%.*}).jpg
  echo ""
  echo "retrieving cluster for image \"$image\" from \"$f\"..."

  CLASS_NAMES=()
  for c in $cluster; do
    # XXX: Assumes validation images
    relative_name=val/$(basename ${c})
#    class_number=`./show_class_for_image.sh $relative_name | grep "number=" | cut -d'=' -f2`
    class=`./show_class_for_image.sh $relative_name | grep "class=" | cut -d'=' -f2`
    CLASS_NAMES+=($class)
  done
  cmd="python image_montage.py -ix 128 -iy 128 -o $cluster_montage -oc $orig_class -i $cluster -cn ${CLASS_NAMES[@]}"
#  echo "running $cmd"
  eval $cmd
done

echo ""
echo "image label:"
./show_class_for_image.sh $image

preds_dir=$miniplaces_dir/weighted_majority/validation
resnet_preds=$preds_dir/resnet_predictions.txt
inception_preds=$preds_dir/inception_predictions.txt

echo ""
echo "resnet top5 predictions:"
grep $image $resnet_preds | cut -d' ' -f1-6

echo ""
echo "inception top5 predictions:"
grep $image $inception_preds | cut -d' ' -f1-6
