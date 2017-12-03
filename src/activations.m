%% original at https://www.mathworks.com/help/nnet/examples/visualize-activations-of-a-convolutional-neural-network.html

% pretrained alexnet
net = alexnet;

% load sample test image
im_file = fullfile(matlabroot, 'examples', 'nnet', 'face.jpg');
%im_file = 'test_images/living_room_orig.png';
figure(1); imshow(im_file)
im = imread(im_file);
%im = imresize(im, [227, 227]);  % model expects a 227 x 277 image

im_file_modified = 'test_images/living_room_no_couch.png';
figure(2); imshow(im_file_modified)
im_file_modified = imread(im_file_modified);
im_modified = imresize(im_file_modified, [227, 227]);

%imshow(im)
imgSize = size(im);
imgSize = imgSize(1:2);
net.Layers;

%% activation images for all neurons on a given layer
act1 = activations(net,im,'conv1','OutputAs','channels');
sz = size(act1);
act1 = reshape(act1,[sz(1) sz(2) 1 sz(3)]);
montage(mat2gray(act1),'Size',[8 12])

%% activation image for specific neuron in the layer
act1ch32 = act1(:,:,:,32);
act1ch32 = mat2gray(act1ch32);
act1ch32 = imresize(act1ch32,imgSize);
imshowpair(im,act1ch32,'montage')

%% strongest activation image for conv1 layer
[maxValue,maxValueIndex] = max(max(max(act1)));
act1chMax = act1(:,:,:,maxValueIndex);
act1chMax = mat2gray(act1chMax);
act1chMax = imresize(act1chMax,imgSize);
imshowpair(im,act1chMax,'montage')

%% activation images for conv5 layer
act5 = activations(net,im,'conv5','OutputAs','channels');
sz = size(act5);
act5 = reshape(act5,[sz(1) sz(2) 1 sz(3)]);
montage(imresize(mat2gray(act5),[48 48]))

%% strongest activation image of conv5 layer; for deeper layers, the
% strongest activation image is not as interesting (expected).
[maxValue5,maxValueIndex5] = max(max(max(act5)));
act5chMax = act5(:,:,:,maxValueIndex5);
imshow(imresize(mat2gray(act5chMax),imgSize))


%% and in the tutorial, channels 3 and 5 are more interesting
montage(imresize(mat2gray(act5(:,:,:,[3 5])),imgSize))

%% look at activations from ReLu layer, which are more useful to understand
act5relu = activations(net,im,'relu5','OutputAs','channels');
sz = size(act5relu);
act5relu = reshape(act5relu,[sz(1) sz(2) 1 sz(3)]);
montage(imresize(mat2gray(act5relu),[48 48]))

%% what concepts are being learned in channels 3 and 5 from relu
act5relu = activations(net,im,'relu5','OutputAs','channels');
sz = size(act5relu);
act5relu = reshape(act5relu,[sz(1) sz(2) 1 sz(3)]);
montage(imresize(mat2gray(act5relu(:,:,:,[3 5])),imgSize))

imClosed = imread(fullfile(matlabroot,'examples','nnet','face_pirate.jpg'));
%imshow(imClosed)
% FIXME: yuck
%imClosed = im_modified;
imshow(im)
act5Closed = activations(net,imClosed,'relu5','OutputAs','channels');
sz = size(act5Closed);
act5Closed = reshape(act5Closed,[sz(1),sz(2),1,sz(3)]);
channelsClosed = repmat(imresize(mat2gray(act5Closed(:,:,:,[3 5])),imgSize),[1 1 3]);
channelsOpen = repmat(imresize(mat2gray(act5relu(:,:,:,[3 5])),imgSize),[1 1 3]);
montage(cat(4,im,channelsOpen*255,imClosed,channelsClosed*255));
title('Input Image, Channel 3, Channel 5');
