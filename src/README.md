# Data requirements

Download image data from https://drive.google.com/drive/folders/1aueyNJUNkPuhXQ9n4eMapsHkoHjpeOz3

# Workflow for image clustering experiments

Select a candidate image, perhaps from a class where both resnet and inception perform well:

```
$ ./classes_with_high_accuracy.sh

classes that were in the top 20 top1 accuracies for both resnet and inception:
/c/cockpit 36
/c/corn_field 40
/g/gas_station 50
/i/ice_skating_rink/outdoor 56
/i/iceberg 57
/k/kindergarden_classroom 58
/l/laundromat 60
/r/rock_arch 80
/t/track/outdoor 95

classes that were in the top 20 top5 accuracies for both resnet and inception:
/c/cockpit 36
/c/conference_room 38
/c/corridor 41
/i/iceberg 57
/k/kindergarden_classroom 58
/l/laundromat 60
```

Assuming you picked class ``iceberg'', then choose an image from validation set with that label:

```
$ ./list_images_from_class.sh iceberg | tail -n 5
val/00009802.jpg
val/00009856.jpg
val/00009906.jpg

iceberg 57
```

Say, for example, that you pick `val/00009856.jpg'.  To look at the clusters from each alexnet layer where it falls into:

```
$ ./show_clusters_for_image.sh val/00009856.jpg

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_avg_conv1_activations.txt"...
saving montage under /tmp/00009856-cluster-val_avg_conv1_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_avg_conv2_activations.txt"...
saving montage under /tmp/00009856-cluster-val_avg_conv2_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_avg_conv3_activations.txt"...
saving montage under /tmp/00009856-cluster-val_avg_conv3_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_avg_conv4_activations.txt"...
saving montage under /tmp/00009856-cluster-val_avg_conv4_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_avg_conv5_activations.txt"...
saving montage under /tmp/00009856-cluster-val_avg_conv5_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_max_conv1_activations.txt"...
saving montage under /tmp/00009856-cluster-val_max_conv1_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_max_conv2_activations.txt"...
saving montage under /tmp/00009856-cluster-val_max_conv2_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_max_conv3_activations.txt"...
saving montage under /tmp/00009856-cluster-val_max_conv3_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_max_conv4_activations.txt"...
saving montage under /tmp/00009856-cluster-val_max_conv4_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_max_conv5_activations.txt"...
saving montage under /tmp/00009856-cluster-val_max_conv5_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_top10%_conv1_activations.txt"...
saving montage under /tmp/00009856-cluster-val_top10%_conv1_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_top10%_conv2_activations.txt"...
saving montage under /tmp/00009856-cluster-val_top10%_conv2_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_top10%_conv3_activations.txt"...
saving montage under /tmp/00009856-cluster-val_top10%_conv3_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_top10%_conv4_activations.txt"...
saving montage under /tmp/00009856-cluster-val_top10%_conv4_activations.jpg...

retrieving cluster for image "val/00009856.jpg" from "clusters-kmeans/val_top10%_conv5_activations.txt"...
saving montage under /tmp/00009856-cluster-val_top10%_conv5_activations.jpg...

class=/i/iceberg 57

resnet top5 predictions:
val/00009856.jpg 57 35 52 4 19

inception top5 predictions:
val/00009856.jpg 57 35 52 61 84
```
