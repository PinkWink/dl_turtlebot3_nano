import cv2
import time
import numpy as np
import tensorflow as tf
import serial
import io


def drive(go, turn):
  command = "$cVW," + str(go*1000) + ',' + str(turn*1000) + "\r\n"
  ser.write(command.encode())
  time.sleep(0.5)

  print("speed : {}, turn : {}".format(go, turn))


def road_detection(save_model_path):

  model = tf.keras.models.load_model(save_model_path)

  while True:
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    time.sleep(0.5)

    img_rgb = frame.copy()
    img_resize = cv2.resize(img_rgb, dsize=(24, 24), interpolation=cv2.INTER_AREA)
    tmp_img = np.reshape(img_resize, (1, 24, 24, 3))
    img = tf.image.convert_image_dtype(tmp_img, tf.float32)
    
    capture.release()
    tmp_action = model.predict(img)
    
    # Map's Goal
    if tmp_action[0][0]>-0.01 and tmp_action[0][0]<0.01 and tmp_action[0][1]>-0.1 and tmp_action[0][1]<0.1:
      break

    drive(tmp_action[0][0], tmp_action[0][1])


if __name__ == "__main__":
  ### input parameter ###############################################
  save_model_path = '211025_mobile_robot.h5'
  ################################################################### 

  ser = serial.Serial(port='/dev/ttyTHS1', baudrate=115200)
  ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), newline="\r", line_buffering = True)
  
  road_detection(save_model_path)