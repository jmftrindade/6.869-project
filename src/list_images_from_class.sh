#!/bin/sh

class_name=$1
miniplaces_data_dir='../externals/miniplaces_challenge/data/'
images_dir=$miniplaces_data_dir/images/

class_number=`grep $class_name $miniplaces_data_dir/categories.txt | cut -d' ' -f2`

echo "All validation images of \"$class_name\":"
grep " $class_number" $miniplaces_data_dir/val.txt | cut -d' ' -f1

echo ""
echo "$class_name $class_number"
