import serial
import time
import io
import sys 

ser = serial.Serial(port='/dev/ttyACM0', baudrate=57600)
ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), newline="\r", line_buffering = True)

forward_vel = sys.argv[0]
rotate_vel = sys.argv[1]

while True:
	command = str(forward_vel)+','+str(rotate_vel)+"\n"
	ser.write(command.encode())
	time.sleep(1)