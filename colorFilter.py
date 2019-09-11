import cv2
import numpy as np
import os

images_folder_path = #path to folder holding images
base_image_path = #path to base image file

def read_as_hsv(path):
  return cv2.cvtColor(cv2.imread(path, cv2.IMREAD_COLOR), cv2.COLORBGR2HSV)

def load_images():
  out_list = []
  
  out_list.append(read_as_hv(base_image_path))
  
  for i in os.listdir(images_folder_path):
    out_list.append(read_as_hsv(images_folder_path + i))
    
   return out_list
    
files = load_images() #loads an n-dim list of filenames with the base image at index 0
    
def find_not_range():
  min_range_base = min(files[0].flat)
  max_range_base = max(files[0].flat)
  std_dev_base = np.std(files[0].flat)
  
  min_
    
    
