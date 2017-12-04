#!/bin/sh

# e.g., "val/00000001.jpg"
image=$1
miniplaces_data_dir='../externals/miniplaces_challenge/data/'
images_dir=$miniplaces_data_dir/images/

for f in clusters-kmeans/*; do
  cluster=`cat $f | grep "$image"`;
  echo "$f:";
  echo "$cluster";
  echo "";
done

class_number=`grep $image $miniplaces_data_dir/*txt | cut -d' ' -f2`
class=`grep " $class_number" $miniplaces_data_dir/categories.txt`
echo "class=$class"
