import serial
import time
#通讯所需的import
from numpy import *;#导入numpy的库函数
import numpy as np; #这个方式使用numpy的函数时，需要以np.开头。
#运动学所用的矩阵的import
import cv2 as cv
#初始化
ser=serial.Serial('/dev/cu.usbmodem1411',9600)#串口
coord1={100,100,0}
Time=5/2000
def interpolation_line(coord1,coord2,v,t,Time,N):#直线插补，输入两点的xyz坐标，速度，插补间隔时间，总时间，插补次数
	L=np.sqrt(np.square(coord1[0]-coord2[0])+np.square(coord1[1]-coord2[1])+np.square(coord1[2]-coord2[2]))
	#L通过两点距离公式计算
	variation[3]={(coord1[0]-coord2[0])/N,(coord1[1]-coord2[1])/N,(coord1[2]-coord2[2])/N}
	#计算每次插补xyz变化量
	point=np.zeros((N,3))#依次为第一个点x（0），y（1），z（2）
	for i in range(1,N+1):
		point[i,0]=coord1[0]+(i-1)*variation[0]
		point[i,1]=coord1[1]+(i-1)*variation[1]
		point[i,2]=coord1[2]+(i-1)*variation[2]
	return point[]

def interpolation_arc(coord1,coord2,v,t,Time,N):#圆弧插补，输入两点的xyz坐标，速度，插补间隔时间，总时间，插补次数
	
	return point[]

def inverseKinematics(T):#逆运动学，输入位姿矩阵
	return pos[]

def sendMessage(pos[]):#串口通讯，输入角度
	for i in range(1,7):
		password+=str(pos[i])
	show=password.encode(encoding='utf-8')#转为二进制
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

def main():
	while(1):
		if cv.waitKey(20) & 0xFF == 27:#按下esc结束程序
			break
		interpolation_line(coord1,coord2)
		sendMessage(inverseKinematics(T))
		time.sleep(Time)

main()




