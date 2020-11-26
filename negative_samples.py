import urllib.request
import requests
import cv2
import numpy as np
import os
import shutil

def store_raw_images():
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n02807133'   
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1
    
    if not os.path.exists('negatives'):
        os.makedirs('negatives')
        
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            response = requests.get(i, timeout=4, stream=True)
            f = open("negatives/"+str(pic_num)+".jpg", 'wb')
            f.write(response.content)
            pic_num += 1
            
        except Exception as e:
            print(str(e)) 

store_raw_images()