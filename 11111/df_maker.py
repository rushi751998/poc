import cv2
import numpy as np
from keras.models import model_from_json

import argparse
from deepface import DeepFace
import os
import uuid
import pandas as pd
import datetime

import tensorflow as tf

import glob
from tqdm._tqdm_notebook import tqdm_notebook as tqdm

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Convolution2D, Dropout, Dense,MaxPooling2D
from keras.layers import BatchNormalization
from keras.layers import MaxPooling2D
from keras.layers import Flatten

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D

from keras.models import Model
from tensorflow.keras.models import Model

import matplotlib.pyplot as plt
from keras.applications import vgg16


# pass here your video path
# you may download one from here : https://www.pexels.com/video/three-girls-laughing-5273028/
cap = cv2.VideoCapture("C:/Users/Vision/Desktop/New folder/django_video_upload/11111/trim_video_2.mp4")
#cap.set(cv2.CAP_PROP_FPS, 2.0)

# get width and height
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )


# count the number of frames
frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)


# calculate duration of the video
seconds = round(frames / fps)
video_time = datetime.timedelta(seconds=seconds)
print(f"Number of frames in the video: {frames}, Fps :{fps}, Duration : {video_time} width: {width} height : {height}")


# Define a list to store the face embeddings of all unique faces seen in the video
whole_face_embeddings = []
seen_face_embeddings = []
seen_face_id = []
final_data=[]
threshold = 0.8
models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
frame_img_array = []

suspecious_model = tf.keras.models.load_model('C:/Users/Vision/Desktop/New folder/django_video_upload/11111/my_model.h5')



def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))



# choose codec according to format needed
#fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
#video = cv2.VideoWriter('video.avi', fourcc, 1, (640, 480))
#cap = cv2.VideoCapture(...) # open a video file or camera
frame_no=0
person_id=0
assert cap.isOpened(), "file/camera could not be opened!"


    
                        
  
while True:
  (success, img) = cap.read() # cap.read() always returns a tuple of two things
  #img = cv2.resize(img, (720, 600))
  if not success: 
    break # you absolutely must check this
  else:
      #print("Frame_no",str(frame_no))
      frame_no=int(frame_no)+int(1)

      #cv2_imshow(img)
      #cv2.imshow("Video", img)
      try:
          objs = DeepFace.analyze(img, actions = ['age', 'gender', 'race', 'emotion'])
          for obj in objs:
            #print(obj)
            x,y,w,h=obj['region']['x'],obj['region']['y'],obj['region']['w'],obj['region']['h']
            #print(obj['region'])
            gender=obj['dominant_gender']
            emotion=obj['dominant_emotion']
            race=obj['dominant_race']
            age=obj['age']

            # Crop the face from the image
            cropped_img = img[y:y + h, x:x + w]

            resize_image = cv2.resize(cropped_img, (224, 224))
            test_array = []
            test_array.append(resize_image)
            test_single_image = np.array(test_array)
            prob_suspecious = suspecious_model.predict(test_single_image) 
            prob_class = int(prob_suspecious.argmax(axis=-1)[0])
            print(prob_class)


            embedding=DeepFace.represent(cropped_img, model_name = models[1], enforce_detection = False)
            face_embedding = embedding[0]['embedding']
            whole_face_embeddings.append(face_embedding)
            


            # Check if the face embedding is similar to any of the seen face embeddings
            similar = False
            for seen_embedding in seen_face_embeddings:
                cos_distance=cosine_similarity(np.array(face_embedding), np.array(seen_embedding))
                #print('cosine_distance',cos_distance)

                # Set a threshold for the distance, below which the two face embeddings are considered similar
                if cos_distance > threshold:
                    similar = True
                    break

            # If the face embedding is not similar to any face embeddings we have
            # seen so far, add it to the list of seen face embeddings
            if not similar:
                  #user_id=uuid.uuid4()
                  seen_face_id.append(person_id)
                  seen_face_embeddings.append(face_embedding)
                  data=[person_id,x,y,w,h,gender,emotion,race,age,frame_no,prob_class]
                  final_data.append(data)
                  person_id=int(person_id)+int(1)

          for index,seen_embedding in enumerate(seen_face_embeddings,start=0):
            cos_distance=cosine_similarity(np.array(face_embedding), np.array(seen_embedding))
            if cos_distance > 0.8:
              id=seen_face_id[index]
              data=[id,x,y,w,h,gender,emotion,race,age,frame_no,prob_class]
              final_data.append(data)
            

            cv2.rectangle(img, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
            cv2.putText(img, f"{obj['dominant_gender']},{obj['dominant_emotion']},{obj['age']}", (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
          frame_img_array.append(img)
        
          #cv2_imshow(img)
      except Exception as e:
          print(str(e))
      
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break
cap.release()

cv2.destroyAllWindows()
# Print the number of unique faces in the video
# print("Number of unique faces in the video: ", len(seen_face_embeddings))
# print("Number of unique faces ID in the video: ", len(seen_face_id))
# print("Number of total embedding: ", len(whole_face_embeddings))
# print(seen_face_embeddings)

# Create the pandas DataFrame
df = pd.DataFrame(final_data, columns=['Face ID', 'X','Y','W','H','Gender','Emotion','Race','Age','Frame No','Suspecious'])



