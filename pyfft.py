import serial
import threading
import numpy as np
import matplotlib.pyplot as plt
SAMPLE_NUM = 2048
SAMPLE_RATE = 100

buffer0 = [0] * SAMPLE_NUM
buffer1 = [0] * SAMPLE_NUM
buffer_being_write = 0
bucket_step = SAMPLE_RATE * 60 / SAMPLE_NUM
data_x = np.array([i * bucket_step for i in range(SAMPLE_NUM // 2 + 1)])

def plot_FFT():
	global buffer0
	global buffer1
	global buffer_being_write
	global SAMPLE_NUM
	global data_x

	print("Updating FFT...")

	if buffer_being_write == 0:
		data = np.array(buffer1)
	else:
		data = np.array(buffer0)

	result = np.absolute(np.fft.rfft(data))
	
	data_y = result
	plt.plot(data_x[10:], data_y[10:])
	plt.xlim(24, 180)

def show_FFT():
	plt.clf()
	plot_FFT()
	plt.savefig('foo.png')

def update_FFT():
	plt.clf()
	plot_FFT()
	plt.savefig('foo.png')


def readData():
	global buffer0
	global buffer1
	global buffer_being_write
	global SAMPLE_NUM

	ser = serial.Serial("/dev/tty.usbmodem14112", 9600)
	print(ser.name)
	idx = 0;
	ser.readline()
	while True:
		# print(int(ser.readline()))
		if buffer_being_write == 0:
			buffer0[idx] = int(ser.readline())
		else:
			buffer1[idx] = int(ser.readline())
		idx += 1
		if idx == SAMPLE_NUM:
			print("Switching buffer...")
			buffer_being_write = 1 - buffer_being_write
			idx = 0
			fftThrd = threading.Thread(target=update_FFT)
			fftThrd.start()

show_FFT()
dataThrd = threading.Thread(target=readData)
dataThrd.start()

print("Thread launched")