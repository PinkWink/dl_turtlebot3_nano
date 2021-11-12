import cv2
import serial
import keyboard

import os
import io
import time


def get_drive_data(go, turn):

  command = "$cVW," + str(go*1000) + ',' + str(turn*1000) + "\r\n"
  ser.write(command.encode())
  time.sleep(0.5)
  
  print("speed : {}, turn : {}".format(go, turn))


def save_image(save_path, resize, index, go, turn):

  capture = cv2.VideoCapture(0)
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
  data_save_path = '/home/my_nano/211025_data/'
  resize_value = 24
  ########################################################

  file_list = os.listdir(data_save_path)
  file_num = len(file_list)
  i = file_num

  ser = serial.Serial(port='/dev/ttyTHS1', baudrate=115200)
  ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), newline="\r", line_buffering = True)

  while 1: 
    if keyboard.is_pressed('w'):
      print("\nup")
      go = -0.1
      turn = 0
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('i'):
      print("\nup fast")
      go = -0.2
      turn = 0
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('s'):
      print("\ndown")
      go = 0.1
      turn = 0
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('k'):
      print("\ndown fast")
      go = 0.2
      turn = 0
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('d'):
      print("\nright")
      go = -0.01
      turn = 0.15
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('l'):
      print("\nright big")
      go = -0.05
      turn = 0.5
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('a'):
      print("\nleft")
      go = -0.01
      turn = -0.15
      save_image(save_path=data_save_path, resize=resize_value, index=i, go=go, turn=turn)
      get_drive_data(go, turn)
      i += 1

    elif keyboard.is_pressed('j'):
      print("\nleft big")
      go = -0.05
      turn = -0.5
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