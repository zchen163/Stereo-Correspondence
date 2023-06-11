import os
import cv2
import numpy as np
import final_proj as fp
import time
from maxflow import fastmin
import logging

'''use PyMaxflow is allowed https://piazza.com/class/kdkhb9uhbfpn?cid=350_f4,
https://github.com/pmneila/PyMaxflow
'''

'''
if want to run other images, search for the topic in this .py file and replace all with the new topic. For example, replace all 'flower' to 'umbrella'.

Note that this is using a 1/4th resizing of original images for faster calculation. The output images are normalized to [0, 255] in grayscale.
'''

IMG_DIR = "input_images/"
OUT_DIR = "flower_output/"
if not os.path.isdir(OUT_DIR): os.makedirs(OUT_DIR)

def optimize_wsize():
    image0, image1 = fp.load_img('flower', 4)
    dmax = 150
    for w_size in range(3, 10, 2):
        dispar, ssd = fp.disparity(image0, image1, w_size = w_size, dmax = dmax, left2right = True)
        fname_out = 'wsize' + str(w_size) + '_dmax'+ str(dmax) + '.png'
        cv2.imwrite(os.path.join(OUT_DIR, fname_out), fp.norm_img(dispar))

def optimize_dmax():
    image0, image1 = fp.load_img('flower', 4)
    w_size = 3
    for dmax in range(50, 201, 50):
        dispar, ssd = fp.disparity(image0, image1, w_size = w_size, dmax = dmax, left2right = True)
        fname_out = 'wsize' + str(w_size) + '_dmax'+ str(dmax) + '.png'
        cv2.imwrite(os.path.join(OUT_DIR, fname_out), fp.norm_img(dispar))

def simple_disparity():
    image0, image1 = fp.load_img('flower', 4)
    w_size = 3
    dmax = 150
    dispar, ssd = fp.disparity(image0, image1, w_size = w_size, dmax = dmax, left2right = True)
    fname_out = 'simple_disparity_left.png'
    cv2.imwrite(os.path.join(OUT_DIR, fname_out), fp.norm_img(dispar))
    dispar1, ssd1 = fp.disparity(image0, image1, w_size = w_size, dmax = dmax, left2right = False)
    fname_out1 = 'simple_disparity_right.png'
    cv2.imwrite(os.path.join(OUT_DIR, fname_out1), fp.norm_img(dispar1))

def potts():
    w_size = 3
    dmax = 150
    image0, image1 = fp.load_img('flower', 4)
    dispar, ssd = fp.disparity(image0, image1, w_size = w_size, dmax = dmax, left2right = True)
    cv2.imwrite(os.path.join(OUT_DIR, 'simple.png'), fp.norm_img(dispar))
    D = np.copy(ssd).astype(np.float64)
    dmax = D.shape[2]
    labels = np.copy(dispar) # initial labaling from simple disparity
    v = np.ones((dmax, dmax))
    for i in range(dmax):
        v[i, i] = 0
    factorlst = [1, 10, 20]
    for i in factorlst:
        V = v * i / (255**2)
        # logging.basicConfig(level=logging.INFO)
        sol = fastmin.aexpansion_grid(D, V, max_cycles = 1, labels = labels)
        fname_out1 = 'flower_aexpansion_cycle1_factor' + str(i) + '_potts.png'
        cv2.imwrite(os.path.join(OUT_DIR, fname_out1), fp.norm_img(sol))
        # time.sleep(60)

def abs_dist():
    w_size = 3
    dmax = 150
    image0, image1 = fp.load_img('flower', 4)
    dispar, ssd = fp.disparity(image0, image1, w_size = w_size, dmax = dmax, left2right = True)
    D = np.copy(ssd).astype(np.float64)
    dmax = D.shape[2]
    labels = np.copy(dispar) # initial labaling from simple disparity
    X,Y = np.mgrid[:dmax, :dmax]
    v = np.float_(np.abs(X-Y))
    factorlst = [1, 10, 20]
    for i in factorlst:
        V = v * i / (255**2)
        # logging.basicConfig(level=logging.INFO)
        sol = fastmin.aexpansion_grid(D, V, max_cycles = 1, labels = labels)
        fname_out1 = 'flower_aexpansion_cycle1_factor' + str(i) + 'AbsDist.png'
        cv2.imwrite(os.path.join(OUT_DIR, fname_out1), fp.norm_img(sol))
        # time.sleep(1)

def ATD(K):
    w_size = 3
    dmax = 150
    image0, image1 = fp.load_img('flower', 4)
    dispar, ssd = fp.disparity(image0, image1, w_size = w_size, dmax = dmax, left2right = True)
    D = np.copy(ssd).astype(np.float64)
    dmax = D.shape[2]
    labels = np.copy(dispar) # initial labaling from simple disparity
    X,Y = np.mgrid[:dmax, :dmax]
    v = np.float_(np.abs(X-Y))
    v = np.clip(v, 0, K)
    factorlst = [1, 10, 20]
    for i in factorlst:
        V = v * i / (255**2)
        # logging.basicConfig(level=logging.INFO)
        sol = fastmin.aexpansion_grid(D, V, max_cycles = 1, labels = labels)
        fname_out1 = 'flower_aexpansion_cycle1_factor' + str(i) + '_truncmax' + str(K) + 'AbsTruncDist.png'
        cv2.imwrite(os.path.join(OUT_DIR, fname_out1), fp.norm_img(sol))
        # time.sleep(180)

def QTD(K):
    w_size = 3
    dmax = 150
    image0, image1 = fp.load_img('flower', 4)
    dispar, ssd = fp.disparity(image0, image1, w_size = w_size, dmax = dmax, left2right = True)
    D = np.copy(ssd).astype(np.float64)
    dmax = D.shape[2]
    labels = np.copy(dispar) # initial labaling from simple disparity
    X,Y = np.mgrid[:dmax, :dmax]
    v = np.float_(np.abs(X-Y))
    v = np.clip(v, 0, K) **2
    factorlst = [1, 10, 20]
    for i in factorlst:
        V = v * i / (255**2)
        # logging.basicConfig(level=logging.INFO)
        sol = fastmin.aexpansion_grid(D, V, max_cycles = 1, labels = labels)
        fname_out1 = 'flower_aexpansion_cycle1_factor' + str(i) + '_truncmax' + str(K) + 'QuadTruncDist.png'
        cv2.imwrite(os.path.join(OUT_DIR, fname_out1), fp.norm_img(sol))
        # time.sleep(180)


def evaluate(topic, subfolder):
    gtf = 'input_images/' + str(topic) + '_gt.png'
    folder = str(topic) + '_output/' + str(subfolder)
    images_files = [f for f in os.listdir(folder) if f.endswith(".png")]
    images_files.sort()
    for i in images_files:
        corr_rate, abs_diff = fp.compare(os.path.join(folder, i), gtf)
        print('-----------')
        print('image: ', i)
        print('Correct Rate: {:5.2f}'.format(corr_rate))
        print('Average of SAD: {:5.2f}'.format(abs_diff))


if __name__ == "__main__":
    optimize_wsize()
    # evaluate(topic = 'flower', subfolder = 'wsize_optimize')
    optimize_dmax()
    # evaluate(topic = 'flower', subfolder = 'dmax_optimize')
    # simple_disparity()
    abs_dist()
    # evaluate(topic = 'flower', subfolder = 'abs_dist')
    for K in [10, 30, 50]:
        ATD(K)
    # evaluate(topic = 'flower', subfolder = 'abs_trunc_dist')
    for K in [10, 30, 50]:
        QTD(K)
    # evaluate(topic = 'flower', subfolder = 'quad_trunc_dist')
    potts()
    # evaluate(topic = 'flower', subfolder = 'potts')
