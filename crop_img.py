import os
import cv2

# Global variables
RAW_IMG_DIR = "images/raw/"  #original drone images directory
CROP_IMG_DIR = "images/cropped/"  #cropped image destination
RAW_SIZE = (4864, 3648)  #change according to your own dataset
CROP_SIZE = 416  # width and height pixels of cropped image
OVERLAP = 0  #pixel, if you need any overlap between images, change accordingly
STRIDE = CROP_SIZE - OVERLAP

# For each image file
for file in sorted(os.listdir(RAW_IMG_DIR)):
    if file.endswith(".JPG"):
        # Open image
        raw_img = cv2.imread(RAW_IMG_DIR + file)
        height, width = raw_img.shape[:2]

        # Create directory and save
        raw_img_name = file.replace(".JPG", "")
        os.mkdir(CROP_IMG_DIR + raw_img_name)

        # Iterate no sliding
        count = 0
        for i in range(0, height, 416):
            for j in range(0, width, 416):
                crop_img = raw_img[i:(i + STRIDE), j:(j + STRIDE)]

                # Pad black rows
                if (i + STRIDE) > height:
                    crop_img = cv2.copyMakeBorder(crop_img, 0, (i + STRIDE) - height, 0, 0, cv2.BORDER_CONSTANT, 0)

                # Pad black columns
                if (j + STRIDE) > width:
                    crop_img = cv2.copyMakeBorder(crop_img, 0, 0, 0, (j + STRIDE) - width, cv2.BORDER_CONSTANT, 0)

                # Save cropped images
                cv2.imwrite(CROP_IMG_DIR + raw_img_name + "/{}_{:04d}.tif".format(raw_img_name, count), crop_img)
                count = count + 1

print("done")
