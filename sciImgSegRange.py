import numpy as np
import matplotlib.pyplot as plt

import cv2

from skimage import *
from skimage.restoration import (denoise_tv_chambolle, estimate_sigma)
import skimage.segmentation as seg

sd_weight = 0.2

plt_count = 0
def plt_image(img):
    global plt_count
    plt.subplots(0,plt_count)
    plt.imshow(img)
    plt_count += 1

def process(image):
    sigma_est = estimate_sigma(image, multichannel=True, average_sigmas=True)
    
    image_rescaled = transform.rescale(image, 0.1, anti_aliasing = True, multichannel = True, mode='constant')
    denoised = denoise_tv_chambolle(image_rescaled, multichannel=True, weight=0.1) #tv denoise
    return denoised, sigma_est

def not_range(image):
    tri_channel_img = np.transpose(image).reshape(3, -1)
    med_base = tuple([np.median(tri_channel_img[i]) for i in range(3)])
    std_dev_base = tuple([np.std(tri_channel_img[i])*sd_weight for i in range(3)])
    not_lower = tuple([med_base[i]-std_dev_base[i] for i in range(len(med_base))])
    not_upper = tuple([med_base[i]+std_dev_base[i] for i in range(len(med_base))])
    return not_lower, not_upper

def check_mask(image, low, high):
    '''
    lowMask = cv2.inRange(image, (0,0,0), low)
    highMask = cv2.inRange(image, high, (1, 1, 1))
    mask = cv2.bitwise_or(lowMask, highMask)
    '''
    pre_mask = cv2.inRange(image, low, high)
    mask = cv2.bitwise_not(pre_mask)
    plastics = cv2.bitwise_and(image, image, mask=mask)
    return plastics


raw_image = io.imread('Sand/sand3.jpg')
image, noise_l= process(raw_image)
sd_weight = 3.3
low, high = not_range(image)

plastics= check_mask(image, low, high)
plt_image(raw_image)
plt_image(image)
#plt_image(mask)
plt_image(plastics)
#print("{0}, {1}".format(low, high))

plt.show()
