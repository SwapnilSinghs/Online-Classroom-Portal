# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:34:06 2020

@author: Naveen
"""

import cv2
import os
import numpy as np
from PIL import Image
import pickle

#reading base directory 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#getting the path from where we are going to read images 
image_dir = "media/images/"
#laoding pre provided file by open CV
face_cascade = cv2.CascadeClassifier('exam/haarcascade_frontalface_alt2.xml')
#loding cv algo to train face recognition
recognizer = cv2.face.LBPHFaceRecognizer_create()
print(image_dir)

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        print(file)
        #currently reading image with this formate only 
        if file.endswith("png") or file.endswith("jpg") or  file.endswith("jpeg") or file.endswith("JPEG"):
            path = os.path.join(root, file)
            # label = os.path.basename(root).replace(" ", "-").lower()
            label = file.split(".")[0]
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            #careting a lable with the folder name ex. name:lable
            id_ = label_ids[label]

            pil_image = Image.open(path).convert("L")  # grayscale
            size = (550, 550)
            #resizing the image 
            final_image = pil_image.resize(size, Image.ANTIALIAS)
            #converting the image in numpy array 
            image_array = np.array(final_image, "uint8")
            # print(image_array)            #detecting face 
            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = image_array[y:y + h, x:x + w]
                x_train.append(roi)
                y_labels.append(id_)

with open("exam/labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)



recognizer.train(x_train, np.array(y_labels))
recognizer.save("exam/trainner.yml")
