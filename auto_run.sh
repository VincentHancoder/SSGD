
# CONFIG=./configs_defect_screen/faster_rcnn/faster_rcnn_full.py
# bash ./tools/dist_train.sh $CONFIG 4

# CONFIG=./configs_defect_screen/faster_rcnn/faster_rcnn_full_v2.py
# bash ./tools/dist_train.sh $CONFIG 4

CONFIG=./configs_defect_screen/faster_rcnn/faster_rcnn_lb101_fold1.py
bash ./tools/dist_train.sh $CONFIG 4

# bash ./tools/dist_test.sh $CONFIG /home/yr2/project/mmdetection_2_25_0/work_dirs/faster_rcnn_full_v2/epoch_12.pth 4 --eval bbox
