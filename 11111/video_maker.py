import numpy as np
import skvideo.io
from df_maker import *

#libx264
output_params={'-vcodec': 'libx264', '-crf':'15','-preset': 'ultrafast', '-pix_fmt': 'yuv444p','-r':'16'}   
out_video =  np.empty([len(frame_img_array), int(height), int(width), 3], dtype = np.uint8)
out_video =  out_video.astype(np.uint8)
  
for i in range(len(frame_img_array)):
    #cv2_imshow(frame_img_array[i])
    #img = cv2.imread(str(i) + '.png')
    rgb_image = cv2.cvtColor(frame_img_array[i], cv2.COLOR_BGR2RGB)
    out_video[i] = rgb_image

# Writes the the output image sequences in a video file
skvideo.io.vwrite("suman.mp4", out_video,outputdict=output_params)