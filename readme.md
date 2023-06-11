# Stereo Correspondence

* Edited by Chen Zhang, project finished in 2021. 

This project aims at finding the disparity map between two views. The disparity map using simple algorithm, and a-expansion algorithm along with various penalty models are examined in this project. It is clear that the a-expansion algorithm is powerful when dealing with occluded edges. In piano case, the best disparity map is achieved under truncated squared distance model.  Different images show distinct optimization with the use of a-expansion algorithm. 

## Related work

Simple correspondence method searches for a patch around each pixel on the same epipolar line, compares the left the right image, and picks the position with minimum cost like sum of squared differences (SSD). However, this method has issues to find the best matches around edges and occluded areas [Deng, Kim]. 

Novel methods formulate stereo correspondence as an energy minimization problem. In this framework, we look for the labeling f that minimizes the energy [Boykov]

<img width="211" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/a9ae4073-4730-4965-ac49-9ea9cc06b8cb">

in which Esmooth measures the extent to which f is not piecewise smooth while Edata measures the disagreement between f and the observed data. Boykov and coworkers brought up the energies of the form: 

<img width="261" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/95b9ad56-56e1-4d34-8757-8f4cbc6068a9">

where p, q in N are nearby pixels, and Vp,q measures the interaction penalty. Dp is the measurement of data term disagreement like SSD or sum of absolute differences (SAD). This kind of energy term can be optimized using graph cuts. 

In this project I apply the a-expansion algorithm and optimize the disparity map especially around occluded edges. The a-expansion algorithm is a fast route towards energy minimization. Multiple interaction penalty functions are being examined. 

## Method

1) Simple algorithm
Here we assume the image provided use calibrated camaras and the epipolar line for each pixel is just it’s horizontal line. Here I use the piano-perfect image from middlebury sample dataset[middlebury]. Other images are included in the discussion session later as comparison. Ground truth is provided by the dataset, and it’s converted to png format through an online converter[pfm2png].

A simple method calculating the disparity is to do a horizontal search based on SSD. The SSD is defined by the following, as stated in the project document: 

<img width="449" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/0a8370ce-1923-494b-b1b8-eda73ed36cf1">

First, I create a 3-dimentional array with the first two dimension as the image width and height, and the third dimension as the steps it moved. Then I apply a filter of a certain window size at each pixel, for the purpose of counting all pixels around. Last step is to search the minimum difference between each layer (3rd dimension) and the other image. 

The metric I use to evaluate the disparity map is two values:1) percentage of correctly calculated pixels and 2) average of SAD. It is worth mentioning that in the correct percentage part, pixels within 2 disparity are considered as correct. The average of SAD is calculated by SAD over total number of pixels. The higher correct percentage, the lower averaged SAD, the better the disparity mapping. 

A range of window size and depth values are tested to achieve best disparity map. The optimal window size for piano-perfect images is 15, and the best depth is 200 (see Figure 1). The plotted intensity is the calculated disparity value. Note that different images have distinct optimal window size and depth values.

<img width="400" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/143d21cf-c54b-491a-a5ac-971b9659d12b">
<img width="400" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/5524c93d-c253-4884-ac0a-4f7866d66681">

Figure 1. Simple disparity. The left image is mapping left view to right view, and the right image is mapping right view to left view. 

2) Advanced algorithms

Advanced algorithms consider both smoothness and data disagreement. Data disagreement term is represented by the SSD calculated in simple disparity. Now there are a few discontinuity preserving interaction penalty functions that might be interesting. The simplest one is just the penalty equals to the absolute distance between labels of neighbor pixels. 

However, a discontinuity preserving interaction term should have a bound on the largest possible penalty[Boykov], which prevents over-penalizing sharp jumps[Kim]. Examples include truncated absolute distance and truncated squared distance. These piecewise smooth models encourage labelings consisting of several regions where pixels in the same region have similar labels. 

Another type of discontinuity preserving interaction function is Potts model. T is 1 if its argument is true, and otherwise 0. This piecewise constant model encourages labelings consisting of several regions where pixels in the same region have equal labels. The abovementioned four types of functions are shown below. V stands for the penalty function of two labels alpha and beta. K is the cut-off value for truncated distances in (2) and (3). K is the factor in potts model (4)[Boykov].  

<img width="456" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/59f9d98f-4482-4536-82a4-e14f395cbdde">

The a-expansion algorithm described in Boykov paper can be represented in the following: 

<img width="317" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/31d71ba4-e797-46d0-8282-0e042d0c5c43">

Maxflow-Mincut algorithm in graph cuts is widely used to minimize energy functions of E(f) as mentioned above. So graph cuts is used to efficiently find f-hat for the key part of each algorithm in Step 3.1. This algorithm allows a large number of pixels to change their labels simultaneously. Note that here we start with not arbitrary labeling, but the label generated from simple disparity. In this study, I adopt the package pymaxflow[Pymaxflow] to calculate the graph cuts and compare the 4 penalty functions in the result. Even with a single cycle of alpha expansion the algorithm provides really good ‘smoothing’ of the disparity map. Due to the high computational cost, this study only use 1-cycle a-expansion and compare the result. 

<img width="557" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/a9a20cbc-f157-45f0-baad-dd0d05791b55">

Figure 2. Result comparison.  a) left view; b) right view; c) ground truth; d) simple disparity; e) absolute distance; f) truncated absolute distance; g) truncated squared distance; h) potts model. A representative occluded edge area is highlighted in red rectangle. 

3) Other images

Each image has its own best window size and depth. For example, the images with less edges and unique features require larger window size and higher depth, like the flower image. The a-expansion algorithm also provides huge improvement in umbrella(Figure 3 top). However, it is not working so well for images like flower with fine features (Figure 3 bottom). The a-expansion cannot restore the little house behind the flowers, the edges of flowers are blurry. I think this is related to ratio of data disagreement and neighbor penalty. Note that other images are using a resizing of one fourth of the original image for faster computation.

<img width="564" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/db2c60ea-26b6-4ffd-97d6-d39b09da1e93">

Figure 3. Disparity map for other images. Top is umbrella, bottom is flower. 

## References

1) [Boykov] Y. Boykov, O. Veksler and R. Zabih, Fast approximate energy minimization via graph cuts, IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, 2001, VOL. 23, PAGE 1222. 
2) [Deng] Y. Deng, Q. Yang, X. Lin and X. Tang, Stereo correspondence with occlusion handling in a symmetric patch-based graph-cuts model, IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, 2003, VOL. 29, PAGE 1068. 
3) [Kim] J. Kim, V. Kolmogorov, and R. Zabih, Visual Correspondence Using Energy Minimization and Mutual Information, Proceedings of the Ninth IEEE International Conference on Computer Vision, 2003 IEEE. 
4) [pfm2png] https://convertio.co/pfm-png/
5) [middlebury] http://vision.middlebury.edu/stereo/data/scenes2014/
6) [Pymaxflow] http://pmneila.github.io/PyMaxflow/tutorial.html

## Environment
This project is based on the provided environment cv_proj.yml. One additional package is required: PyMaxflow.

Installation of PyMaxflow is via pip:
$ pip install PyMaxflow

See their github for more information: https://github.com/pmneila/PyMaxflow

## Files
experiment.py: main file that contains all experiments, including optimization of window size and depth, and disparity images generated from simple disparity and advanced disparity algorithms.

final_proj.py: contains key functions that load images, calculate ssd and simple disparity, and generate metrics for comparison with ground truth.

other_images.py: contains similar codes to the experiment.py, but using other images than piano. see the first couple lines in this file for changing images.

formula.tex: contains latex code for all math formulas in the report.

input_images folder: contains images. Left view, right view, and ground truth images are named by 'topic_im0.png', topic_im1.png' and 'topic_gt.png', respectively. Topics contain piano, umbrella, flower and playtable. These images are downloaded from middlebury dataset. Note that the ground truth png images are converted from the pfm file using an online converter. pfm files are not included.

## Load images
Currently the images are named after topic. For example, piano_im0.png and piano_im1.png are two views of the piano. If TA wants to load other images, please make necessary changes on the file names, and put them under 'input_images' folder.

## Run code and output
$ python experiment.py
this will generate all images for piano-related disparity map. The output images will stored in a folder named 'piano_output'

$ python other_images.py
this will generate all images for disparity map under other topics. The output images will stored in a folder named 'topic_output' (e.g. flower_output).
