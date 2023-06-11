import cv2
import numpy as np
import os
import sys

IMG_DIR = "input_images/"

def norm_img(img):
    image_in = np.copy(img)
    out = cv2.normalize(image_in, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX).astype(np.uint8)
    return out

'''
loading images. Currently the images are named after topic. For example, piano_im0.png and piano_im1.png are two views of the piano. If TA wants to load other images, please make necessary changes.
'''

def load_img(fname, scale_f):
    # get file names
    fname_in0 = str(fname)  + '_im0.png'
    fname_in1 = str(fname)  + '_im1.png'
    # load images
    temp0 = cv2.imread(os.path.join(IMG_DIR, fname_in0), 0) # read in as grayscale
    temp1 = cv2.imread(os.path.join(IMG_DIR, fname_in1), 0)
    # resize image if necessary
    image0 = cv2.resize(temp0, (temp0.shape[1]//scale_f, temp0.shape[0]//scale_f))
    image1 = cv2.resize(temp1, (temp0.shape[1]//scale_f, temp0.shape[0]//scale_f))
    return image0, image1

def disparity(image_in0, image_in1, w_size, dmax, left2right = True):
    # resize image down to half
    image0 = np.copy(image_in0)/ 255
    image1 = np.copy(image_in1)/ 255
    h, w = image0.shape
    # build a kernel to sum up over a window
    kernel = np.ones((w_size, w_size)) /(w_size**2) # make a kernel around the window
    ssd = np.zeros((h, w, dmax))

    # shift, then calculate ssd
    if left2right == True: # move right-view image (image1) to right
        for i in range(dmax):
            # use copyMakeBorder to move right, then
            shifted = cv2.copyMakeBorder(image1[:, :(-i or None)], 0, 0, i, 0, cv2.BORDER_REPLICATE) # top bot left right
            diff = (image0 - shifted)**2 # sum of square diff
            ssd[:, :, i] = cv2.filter2D(diff, -1, kernel)
    elif left2right == False: # move left-view image (image0) to left
        for i in range(dmax):
            shifted = cv2.copyMakeBorder(image0[:, (i or None):], 0, 0, 0, i, cv2.BORDER_REPLICATE) # top bot left right
            diff = (image1 - shifted)**2 # sum of square diff
            ssd[:, :, i] = cv2.filter2D(diff, -1, kernel)

    # get disparity, argmin of the dmax axis
    dispar = np.argmin(ssd, axis = 2)
    # cv2.imshow('c', normed)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return dispar, ssd

def compare(resultf, gtf):
    result = cv2.imread(resultf, 0).astype(np.int)
    gt = cv2.imread(gtf, 0).astype(np.int)
    num_pixels = result.shape[0] * result.shape[1]
    diff = abs(result - gt)
    pos = np.where(diff <= 2)
    # pos = np.where(diff == 0)
    corr_rate = pos[0].shape[0] / num_pixels * 100
    abs_diff = np.sum(diff/num_pixels)
    return corr_rate, abs_diff
