#!/bin/sh

miniplaces_path='../externals/miniplaces_challenge'

# categories file
categories_path=$miniplaces_path/data/categories.txt

# class accuracies files
acc_path=$miniplaces_path/weighted_majority/validation/
resnet_acc=$acc_path/resnet_train_class_accuracies.txt
inception_acc=$acc_path/inception_class_accuracies.txt

# reverse sort by top1 and top5 class accuracy
top1_idx=2
top5_idx=3
cat $resnet_acc | sort -nrk $top1_idx | head -n 20 | sort -nk 1 | cut -d' ' -f1 > /tmp/highest_acc_top1_resnet.txt
cat $inception_acc | sort -nrk $top1_idx | head -n 20 | sort -nk 1 | cut -d' ' -f1 > /tmp/highest_acc_top1_inception.txt
cat $resnet_acc | sort -nrk $top5_idx | head -n 20 | sort -nk 1 | cut -d' ' -f1 > /tmp/highest_acc_top5_resnet.txt
cat $inception_acc | sort -nrk $top5_idx | head -n 20 | sort -nk 1 | cut -d' ' -f1 > /tmp/highest_acc_top5_inception.txt

echo "classes that were in the top 20 top1 accuracies for both resnet and inception:"
for class in `sort /tmp/highest_acc_top1_* | uniq -d`; do grep $class $categories_path; done

echo ""
echo "classes that were in the top 20 top5 accuracies for both resnet and inception:"
for class in `sort /tmp/highest_acc_top5_* | uniq -d`; do grep $class $categories_path; done

# cleanup
rm /tmp/highest_acc_top*txt
