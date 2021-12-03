export DARKNET=/home/kevin/Desktop/darknet
export PRJ_PATH=/home/kevin/Desktop/maskDetection_jetson

cd $DARKNET
./darknet detector demo \
$PRJ_PATH/mask.data \
$PRJ_PATH/yolov4-tiny-custom.cfg \
$PRJ_PATH/backup/yolov4-tiny-custom_last.weights \
"nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, width=1280, height=720, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink" -thresh 0.4
