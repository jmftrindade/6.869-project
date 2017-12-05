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

Say for example, that you pick the first one from results above.  Then, to look at the clusters from each alexnet layer where it falls into:

```
$ ./show_clusters_for_image.sh val/00009802.jpg

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_avg_conv1_activations.txt"...
saving montage under /tmp/00009802-cluster-val_avg_conv1_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_avg_conv2_activations.txt"...
saving montage under /tmp/00009802-cluster-val_avg_conv2_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_avg_conv3_activations.txt"...
saving montage under /tmp/00009802-cluster-val_avg_conv3_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_avg_conv4_activations.txt"...
saving montage under /tmp/00009802-cluster-val_avg_conv4_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_avg_conv5_activations.txt"...
saving montage under /tmp/00009802-cluster-val_avg_conv5_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_max_conv1_activations.txt"...
saving montage under /tmp/00009802-cluster-val_max_conv1_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_max_conv2_activations.txt"...
saving montage under /tmp/00009802-cluster-val_max_conv2_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_max_conv3_activations.txt"...
saving montage under /tmp/00009802-cluster-val_max_conv3_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_max_conv4_activations.txt"...
saving montage under /tmp/00009802-cluster-val_max_conv4_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_max_conv5_activations.txt"...
saving montage under /tmp/00009802-cluster-val_max_conv5_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_top10%_conv1_activations.txt"...
saving montage under /tmp/00009802-cluster-val_top10%_conv1_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_top10%_conv2_activations.txt"...
saving montage under /tmp/00009802-cluster-val_top10%_conv2_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_top10%_conv3_activations.txt"...
saving montage under /tmp/00009802-cluster-val_top10%_conv3_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_top10%_conv4_activations.txt"...
saving montage under /tmp/00009802-cluster-val_top10%_conv4_activations.jpg...

retrieving cluster for image "val/00009802.jpg" from "clusters-kmeans/val_top10%_conv5_activations.txt"...
saving montage under /tmp/00009802-cluster-val_top10%_conv5_activations.jpg...

class=/i/iceberg 57

resnet predictions:
val/00009802.jpg 4 80 98 29 88 68 35 61 57 84 97 30 43 9 49 40 92 79 51 6 85 55 99 21 72 93 71 42 69 31 52 96 2 44 66 0 5 8 77 27 39 46 82 24 67 32 56 94 73 36 23 50 81 14 16 11 83 74 19 53 13 34 89 87 3 15 12 86 17 37 22 41 95 33 70 10 75 63 38 28 18 90 64 78 26 76 7 65 1 47 25 54 58 59 62 45 20 48 60 91

inception predictions:
val/00009802.jpg 4 98 68 35 55 57 84 97 31 61 80 21 29 2 77 79 43 24 96 93 46 3 88 76 40 49 52 99 9 82 27 67 94 89 5 12 42 85 56 44 14 0 32 30 92 13 71 72 39 53 36 86 8 7 41 74 54 11 87 65 10 51 95 83 81 63 78 19 15 62 23 33 22 6 37 16 47 45 73 38 50 34 17 1 26 25 90 66 75 18 48 64 28 91 69 60 58 70 20 59
```
