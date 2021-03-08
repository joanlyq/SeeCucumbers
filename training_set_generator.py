import json
import os
import glob
import numpy as np

from tqdm import tqdm

# directory of json files and destination folders
json_dir = 'model_data/gt/json/'
jsons = glob.glob(json_dir + '*.json')
out = 'model_data/ann/'  # folder name
gt_out = 'model_data/gt/'
img_dir = 'images/cropped/'
img_subdir = sorted(glob.glob(img_dir+"*"))

# create desination folder
if not os.path.exists(out):
    os.mkdir(out)
if not os.path.exists(gt_out):
    os.mkdir(gt_out)

# create annotation compilation,
single_class_ann = open(out + 'sc_annotations' + '.txt', 'w')

# convert ground truth '*.json' to keras-yolo3 format.
# every line, separate bbox with ' ', and coordinate by ','
# i.e. image_directory xmin1,ymin1,xmax1,ymax1,class1 xmin2,ymin2,xmax2,ymax2,class2
for subdir in tqdm(sorted(img_subdir), desc="Extract ground truths"):
    tifs = glob.glob(subdir+"/*.tif")
    for tif in sorted(tifs):
        img = tif[-17:-4]
        fn = img_dir+tif[-17:-9]+'/'+tif[-17:]   # directory in folder, change accordingly
        ground_truth = open(gt_out + img + '.txt', 'w') # create ground truth txt for every image
        json_file = json_dir+img+'.json'
        # find json
        # write image directory if there's no ground truth bbox
        if json_file not in jsons:
            single_class_ann.write('%s' % (fn))
        # write image directory & ground true bbox
        else:
            single_class_ann.write('%s' % (fn))
            f = open(json_file)
            data = json.load(f)
            for item in data['shapes']:
                if not item:
                    continue
                else:
                    cls_sc = 0
                    cls_name = 'Sea_cucumber'
                    box = item['points']
                    x1 = int(box[0][0])
                    y1 = int(box[0][1])
                    x2 = int(box[1][0])
                    y2 = int(box[1][1])
                    xmin = min(x1, x2)
                    xmax = max(x1, x2)
                    ymin = min(y1, y2)
                    ymax = max(y1, y2)
                    ground_truth.write('%s %d %d %d %d\n' % (cls_name, xmin, ymin, xmax, ymax))  #write ground truth for mAP calculation
                    single_class_ann.write(' %d,%d,%d,%d,%g' % (xmin, ymin, xmax, ymax, cls_sc))
        single_class_ann.write('\n')

        ground_truth.close()
single_class_ann.close()


# create training data set
sc_txt = open(out+"sc_annotations.txt", 'r')
train_sc = open(out + 'train_sc' + '.txt', 'w')
test_sc = open(out + 'test_sc' + '.txt', 'w')

# random select training&validation subset
lines_sc = sc_txt.readlines()
step = 6000/6804     #change the training dateset size accordingly, 1000,2000,3000...
np.random.seed(10101)   #pseudo random
np.random.shuffle(lines_sc)
num_train = int(len(lines_sc) * step)
for i in tqdm(range(num_train), desc="selecting training images"):
    line_sc = lines_sc[i]
    train_sc.write(line_sc)

for i in tqdm(range(6000,6804), desc="selecting validation images"):
    line_remain = lines_sc[i]
    test_sc.write(line_remain)

train_sc.close()
test_sc.close()
