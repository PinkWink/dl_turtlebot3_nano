import serial
import time
import io

ser = serial.Serial(port='/dev/ttyACM0', baudrate=57600)
ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), newline="\r", line_buffering = True)

while True:
	command = "0,0\n"
	ser.write(command.encode())
	time.sleep(1)