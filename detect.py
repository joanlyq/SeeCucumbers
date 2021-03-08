import sys
import argparse
from yolo import YOLO
from PIL import Image
import os
import numpy as np
import shutil

annotation_path = 'model_data/ann/sc_annotations.txt'  #change the directory to 'model_data/test_sc.txt' for mAP calculation.
dr_img_path = 'detected_result/'
det_result_path = 'mAP/input/detection-results/'

def detect_img(yolo):
    if os.path.exists(det_result_path):
        shutil.rmtree(det_result_path)
        os.makedirs(det_result_path)
    else:
        os.makedirs(det_result_path)

    if os.path.exists(dr_img_path):
        shutil.rmtree(dr_img_path)
        os.makedirs(dr_img_path)
    else:
        os.makedirs(dr_img_path)

    f = open(annotation_path)
    lines = f.readlines()

    for annotation in lines:
        # print(annotation)
        img_path = annotation.split(' ')[0].strip()
        print('img_path',img_path)
        img = Image.open(img_path)
        r_image, r_detections = yolo.detect_image(img)
        image_name = os.path.basename(img_path)
        print('image_name',image_name)
        result_name = image_name.replace('.tif','')
        r_image.save(dr_img_path + result_name + ".png")     # save images with detected bounding boxes
        result = open(det_result_path + result_name+'.txt','w')    # save detected result in txt file with bounding box (left, top, right, bottom)
        for i in r_detections:
            i=i[0]
            print(i)
            result.write("%s\n" % (i))
        result.close()
    yolo.close_session()

FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    FLAGS = parser.parse_args()
    detect_img(YOLO(**vars(FLAGS)))
    
  
