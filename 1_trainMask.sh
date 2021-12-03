export DARKNET=/home/kevin/Desktop/darknet
export PRJ_PATH=/home/kevin/Desktop/maskDetection_jetson

cd $DARKNET
time ./darknet detector train \
$PRJ_PATH/mask.data \
$PRJ_PATH/yolov4-tiny-custom.cfg \
darknet53.conv.74 \
-dont_show
