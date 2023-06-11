# Stereo Correspondence

This project aims at finding the disparity map between two views. The disparity map using simple algorithm, and a-expansion algorithm along with various penalty models are examined in this project. It is clear that the a-expansion algorithm is powerful when dealing with occluded edges. In piano case, the best disparity map is achieved under truncated squared distance model.  Different images show distinct optimization with the use of a-expansion algorithm. 

## Environment
This project is based on the provided environment cv_proj.yml. One additional package is required: PyMaxflow.

Installation of PyMaxflow is via pip:
$ pip install PyMaxflow

See their github for more information: https://github.com/pmneila/PyMaxflow

## Related work

Simple correspondence method searches for a patch around each pixel on the same epipolar line, compares the left the right image, and picks the position with minimum cost like sum of squared differences (SSD). However, this method has issues to find the best matches around edges and occluded areas [Deng, Kim]. 

Novel methods formulate stereo correspondence as an energy minimization problem. In this framework, we look for the labeling f that minimizes the energy [Boykov]

<img width="157" alt="image" src="https://github.com/zchen163/Stereo-Correspondence/assets/48006055/1ea9e553-08ca-48f5-9a03-ee43814b101e">
  
in which Esmooth measures the extent to which f is not piecewise smooth while Edata measures the disagreement between f and the observed data. Boykov and coworkers brought up the energies of the form: 
 
where p, q in N are nearby pixels, and Vp,q measures the interaction penalty. Dp is the measurement of data term disagreement like SSD or sum of absolute differences (SAD). This kind of energy term can be optimized using graph cuts. 

In this project I apply the a-expansion algorithm and optimize the disparity map especially around occluded edges. The a-expansion algorithm is a fast route towards energy minimization. Multiple interaction penalty functions are being examined. 


# Files
experiment.py: main file that contains all experiments, including optimization of window size and depth, and disparity images generated from simple disparity and advanced disparity algorithms.

final_proj.py: contains key functions that load images, calculate ssd and simple disparity, and generate metrics for comparison with ground truth.

other_images.py: contains similar codes to the experiment.py, but using other images than piano. see the first couple lines in this file for changing images.

formula.tex: contains latex code for all math formulas in the report.

input_images folder: contains images. Left view, right view, and ground truth images are named by 'topic_im0.png', topic_im1.png' and 'topic_gt.png', respectively. Topics contain piano, umbrella, flower and playtable. These images are downloaded from middlebury dataset. Note that the ground truth png images are converted from the pfm file using an online converter. pfm files are not included.

# Load images
Currently the images are named after topic. For example, piano_im0.png and piano_im1.png are two views of the piano. If TA wants to load other images, please make necessary changes on the file names, and put them under 'input_images' folder.

# Run code and output
$ python experiment.py
this will generate all images for piano-related disparity map. The output images will stored in a folder named 'piano_output'

$ python other_images.py
this will generate all images for disparity map under other topics. The output images will stored in a folder named 'topic_output' (e.g. flower_output).

# Code printout
The experiment.py will generate print out of the metrics for comparison. The format is:
print('-----------')
print('image: ', i)
print('Correct Rate: {:5.2f}'.format(corr_rate))
print('Average of SAD: {:5.2f}'.format(abs_diff))

Those values are used for evaluation of disparity algorithms, compared to ground truth.
If TA doesn't want to see the printouts, please comment those lines out.

Now logging printouts are suppressed. However, both experiment.py and other_images.py can generate logging info from the pymaxflow.fastmin module for debugging purpose, if activates all lines contains 'logging.basicConfig(level=logging.INFO)'.

# deliverables under code session
experiment.py
final_proj.py
other_images.py
readme.txt
input_images.zip(a zipped folder contains left view, right view and ground truth of piano, flower and umbrella)

# deliverables under report session
final_report.pdf
