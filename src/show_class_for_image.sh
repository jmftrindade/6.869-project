#!/bin/sh

# e.g., "val/00000001.jpg"
image=$1
miniplaces_dir=../externals/miniplaces_challenge
miniplaces_data_dir=$miniplaces_dir/data
images_dir=$miniplaces_data_dir/images/

class_number=`grep $image $miniplaces_data_dir/*txt | cut -d' ' -f2`
class=`grep " $class_number" $miniplaces_data_dir/categories.txt | cut -d' ' -f1 | cut -d'/' -f3`
echo "class=$class"
echo "class_number=$class_number"
