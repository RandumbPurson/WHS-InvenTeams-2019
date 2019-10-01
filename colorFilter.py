
#imports
import numpy as np
import matplotlib.pyplot as plt

import cv2

from skimage import *
from skimage.restoration import (denoise_tv_chambolle, estimate_sigma)
import skimage.segmentation as seg

### Fidgety variable ###
sd_weight = 3.3
### ---------------- ###

#function for displaying images with matplotlib
plt_count = 0
def plt_image(img):
    global plt_count
    plt.subplots(0,plt_count)
    plt.imshow(img)
    plt_count += 1

#process images - resize, denoise
def process(image):
    sigma_est = estimate_sigma(image, multichannel=True, average_sigmas=True)
    
    image_rescaled = transform.rescale(image, 0.1, anti_aliasing = True, multichannel = True, mode='constant') #resize
    denoised = denoise_tv_chambolle(image_rescaled, multichannel=True, weight=0.1) #denoise
    return denoised, sigma_est

#find color range of the sand
def not_range(image):
    tri_channel_img = np.transpose(image).reshape(3, -1) #format img array
    
    #find median and std deviation
    med_base = tuple([np.median(tri_channel_img[i]) for i in range(3)])
    std_dev_base = tuple([np.std(tri_channel_img[i])*sd_weight for i in range(3)])
    
    #find lower and upper bounds
    not_lower = tuple([med_base[i]-std_dev_base[i] for i in range(len(med_base))])
    not_upper = tuple([med_base[i]+std_dev_base[i] for i in range(len(med_base))])
    return not_lower, not_upper

#returns image after removing sand
def check_mask(image, low, high):
    pre_mask = cv2.inRange(image, low, high) #construct mask of sand
    mask = cv2.bitwise_not(pre_mask) #invert mask
    plastics = cv2.bitwise_and(image, image, mask=mask) #apply mask to image
    return plastics

#main
if __name__ == __main__:
    raw_image = io.imread('Sand/sand3.jpg') #import image
    image, noise_l = process(raw_image) #process
    low, high = not_range(image) #find range of sand
    plastics = check_mask(image, low, high) #apply mask to image
    
    #display important images
    plt_image(raw_image)
    plt_image(image)
    plt_image(plastics)
    plt.show()
