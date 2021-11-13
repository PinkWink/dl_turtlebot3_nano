import cv2
import serial
import keyboard

import os
import io
import time

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

def get_drive_data(go, turn):

  command = str(go) + ',' + str(turn) + "\n"
  ser.write(command.encode())
  time.sleep(0.5)
  
  print("speed : {}, turn : {}".format(go, turn))


def save_image(save_path, resize, index, go, turn):

  capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
  ret, frame = capture.read()
  time.sleep(0.5)

  img_rgb = frame.copy()
  color_img_resize = cv2.resize(img_rgb, dsize=(resize, resize), interpolation=cv2.INTER_AREA)

  cv2.imwrite(save_path + 'drive_%s_%s_%s_.jpg' %(i, go, turn), color_img_resize)
  capture.release() 
  time.sleep(0.5)
  print("save img finish")
  

if __name__ == "__main__":
  ### input parameter ####################################
  data_save_path = '/home/kiro/data/'
  resize_value = 24
  ########################################################

  file_list = os.listdir(data_save_path)
  file_num = len(file_list)
  i = file_num

  go = 0
  turn = 0

  ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
  ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), newline="\r", line_buffering = True)

  while 1: 
    if keyboard.is_pressed('w'):
      go += 2 
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('a'):
      turn += 2 
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('d'):
      turn -= 2 
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('x'):
      go -= 2 
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('s'):
      go = 0
      turn = 0
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('o'):
      print("\nDrive Finish")
      go = 0 
      turn = 0 
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1
      break
