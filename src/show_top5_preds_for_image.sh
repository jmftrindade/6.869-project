#!/bin/sh

# e.g., "val/00000001.jpg"
image=$1
predictions=predictions/val_predictions.txt
miniplaces_dir=../externals/miniplaces_challenge
miniplaces_data_dir=$miniplaces_dir/data

preds_numbers=`grep $image $predictions | cut -d' ' -f2-6`
PREDS=()
for class_number in $preds_numbers; do
    class=`grep " $class_number$" $miniplaces_data_dir/categories.txt | cut -d' ' -f1 | cut -d'/' -f3`
    PREDS+=($class)
done

echo "predictions=${PREDS[@]}"
echo "predictions_numbers=${preds_numbers}"
