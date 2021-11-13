import cv2
import time
import numpy as np
import tensorflow as tf
import serial
import io

def gstreamer_pipeline(
    capture_width=320,
    capture_height=180,
    display_width=320, #1280,
    display_height=180, #720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
    

def drive(go, turn):
  command = str(go) + ',' + str(turn) + "\n"
  ser.write(command.encode())
  time.sleep(0.5)

  print("speed : {}, turn : {}".format(go, turn))


def road_detection(save_model_path):

  model = tf.keras.models.load_model(save_model_path)

  while True:
    capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
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
  save_model_path = 'mobile_robot.h5'
  ################################################################### 

  ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
  ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), newline="\r", line_buffering = True)
  
  road_detection(save_model_path)