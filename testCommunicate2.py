import serial
import time




ser=serial.Serial('/dev/cu.usbmodem1421',9600)

time.sleep(8)
def sendMessage(message):
	show=message.encode(encoding='utf-8')
	#print(show)

	try:
		
			#print(ser.readline())
			ser.write(show)
			time.sleep(0.01)
	except:
			print ('Failed to send')
	print(ser.readline())
	time.sleep(0.01)
	print(ser.readline())
	time.sleep(0.01)
	print(ser.readline())
	time.sleep(0.01)

'''
print(ser.readline())
time.sleep(0.01)
print(ser.readline())
time.sleep(0.01)
'''

sendMessage('094017052082033075')
sendMessage('094017052082033150')


ser.close()
