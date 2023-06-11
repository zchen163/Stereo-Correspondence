# Stereo Correspondence

This project aims at finding the disparity map between two views. The disparity map using simple algorithm, and a-expansion algorithm along with various penalty models are examined in this project. It is clear that the a-expansion algorithm is powerful when dealing with occluded edges. In piano case, the best disparity map is achieved under truncated squared distance model.  Different images show distinct optimization with the use of a-expansion algorithm. 

## Related work

Simple correspondence method searches for a patch around each pixel on the same epipolar line, compares the left the right image, and picks the position with minimum cost like sum of squared differences (SSD). However, this method has issues to find the best matches around edges and occluded areas [Deng, Kim]. 

Novel methods formulate stereo correspondence as an energy minimization problem. In this framework, we look for the labeling f that minimizes the energy [Boykov]

<img width="211" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/a9ae4073-4730-4965-ac49-9ea9cc06b8cb">

in which Esmooth measures the extent to which f is not piecewise smooth while Edata measures the disagreement between f and the observed data. Boykov and coworkers brought up the energies of the form: 

<img width="261" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/95b9ad56-56e1-4d34-8757-8f4cbc6068a9">

where p, q in N are nearby pixels, and Vp,q measures the interaction penalty. Dp is the measurement of data term disagreement like SSD or sum of absolute differences (SAD). This kind of energy term can be optimized using graph cuts. 

In this project I apply the a-expansion algorithm and optimize the disparity map especially around occluded edges. The a-expansion algorithm is a fast route towards energy minimization. Multiple interaction penalty functions are being examined. 

3. Method
1) Simple algorithm
Here we assume the image provided use calibrated camaras and the epipolar line for each pixel is just it’s horizontal line. Here I use the piano-perfect image from middlebury sample dataset[middlebury]. Other images are included in the discussion session later as comparison. Ground truth is provided by the dataset, and it’s converted to png format through an online converter[pfm2png].

A simple method calculating the disparity is to do a horizontal search based on SSD. The SSD is defined by the following, as stated in the project document: 

<img width="449" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/0a8370ce-1923-494b-b1b8-eda73ed36cf1">

First, I create a 3-dimentional array with the first two dimension as the image width and height, and the third dimension as the steps it moved. Then I apply a filter of a certain window size at each pixel, for the purpose of counting all pixels around. Last step is to search the minimum difference between each layer (3rd dimension) and the other image. 

The metric I use to evaluate the disparity map is two values:1) percentage of correctly calculated pixels and 2) average of SAD. It is worth mentioning that in the correct percentage part, pixels within 2 disparity are considered as correct. The average of SAD is calculated by SAD over total number of pixels. The higher correct percentage, the lower averaged SAD, the better the disparity mapping. 

A range of window size and depth values are tested to achieve best disparity map. The optimal window size for piano-perfect images is 15, and the best depth is 200 (see Figure 1). The plotted intensity is the calculated disparity value. Note that different images have distinct optimal window size and depth values.

<img width="400" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/143d21cf-c54b-491a-a5ac-971b9659d12b">
<img width="400" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/5524c93d-c253-4884-ac0a-4f7866d66681">

Figure 1. Simple disparity. The left image is mapping left view to right view, and the right image is mapping right view to left view. ![image](https://github.com/zchen163/Stereo-Correspondence/assets/48006055/db41863c-39e4-4db0-9318-4bfe8133b39b)


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

## Code printout
The experiment.py will generate print out of the metrics for comparison. The format is:
print('-----------')
print('image: ', i)
print('Correct Rate: {:5.2f}'.format(corr_rate))
print('Average of SAD: {:5.2f}'.format(abs_diff))

Those values are used for evaluation of disparity algorithms, compared to ground truth. Now logging printouts are suppressed. However, both experiment.py and other_images.py can generate logging info from the pymaxflow.fastmin module for debugging purpose, if activates all lines contains 'logging.basicConfig(level=logging.INFO)'.
