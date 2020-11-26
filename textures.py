
#import matplotlib.pyplot as plt
#import time
#import random
#import numpy as np
import cv2
import math
import mahotas

k=13

class Node():
    def __init__(self, point):
        self.point = point
        self.axis = None
        self.left = None
        self.right = None
        self.tipo = None

class Cola():
	def __init__(self, cant):
		self.n = cant
		self.lis=[]
	def insertar(self, distancia,x):
		for i in range(len(self.lis)):
			if(self.lis[i][1]==x):
				return
		if(len(self.lis)==self.n):
			if(self.lis[self.n-1][0]>distancia):
				self.lis[self.n-1]=[distancia,x]
				self.lis.sort(key=lambda tup: tup[0])
		else:
			self.lis.append([distancia,x])
			self.lis.sort(key=lambda tup: tup[0])
	def top(self):
		return self.lis[len(self.lis)-1][0]
	def llena(self):
		if(len(self.lis)!=self.n):
			return False
		return True

def build_kdtree(points, depth=0):
	if not points:
		return None
	#Para saber si dividir por el eje x o y
	axis = depth % k

	points.sort(key=lambda tup: tup.point[axis])

	median = len(points)//2

	node = points[median]
	node.axis=axis

	node.left=build_kdtree(points[:median],depth+1)
	node.right=build_kdtree(points[median+1:],depth+1)

	return node

def distanceSquared(a, b):
	distance = 0
	for i in range(k):
		distance = distance + pow((a[i]-b[i]),2)
	return math.sqrt(distance)

def closest_point(node, point, depth , cola):
	if(node == None):
		return
	axis = depth % k
	next_branch = None
	opposite_branch = None
	cola.insertar(distanceSquared(point, node.point),node)
	if(point[axis] < node.point[axis]):
		next_branch = node.left
		opposite_branch = node.right
	else:
		next_branch = node.right
		opposite_branch = node.left
	closest_point(next_branch, point, depth+1, cola)
	if(not(cola.llena()) or (cola.top() > abs(point[axis]-node.point[axis]))):
		closest_point(opposite_branch, point, depth+1, cola)

def nearest(root, point, count):
	cola = Cola(count)
	closest_point(root, point, 0, cola)
	return cola.lis
def haralick(name, clase, size=(16, 16)):
    image = cv2.imread(name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, size)
    features = mahotas.features.haralick(image).mean(0)
    point = features
    node = Node(point)
    node.tipo = clase
    return node

def test(name, root, size=(16, 16)):
    image = cv2.imread(name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, size)
    features = mahotas.features.haralick(image).mean(0)
    point =features
    resultado = nearest(root, point, 10)
    tipo1=0
    tipo2=0
    for i in resultado:
     if(i[1].tipo=="cocodrilo"):
         tipo1=tipo1+1
     else:
         tipo2=tipo2+1

    if(tipo1==tipo2):
        print("50/50")
        image = cv2.imread(name)
        cv2.putText(image,"50/50", (20, 30),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0,255,0),3)
        cv2.imshow('IMAGE',image)
        cv2.waitKey(0)
        
    elif(tipo1>tipo2):
        print("Es cocodrilo")
        image = cv2.imread(name)
        cv2.putText(image,"cocodrilo", (20, 30),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0,255,0),3)
        cv2.imshow('IMAGE',image)
        cv2.waitKey(0)
    else:
        print("Es tortuga")
        image = cv2.imread(name)
        cv2.putText(image,"tortuga", (20, 30),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0,255,0),3)
        cv2.imshow('IMAGE',image)
        cv2.waitKey(0)
    
    print(tipo1,tipo2)    
    
def main():
    points=[]
    for i in range(1,21):
        name = r'C:\Users\user\.spyder-py3\kdtreee\Nueva carpeta\cocodrilos\cocodrilo'+str(i)+'.png'
        points.append(haralick(name,"cocodrilo"))
    for i in range(1,21):
        name = r'C:\Users\user\.spyder-py3\kdtreee\Nueva carpeta\tortugas\tortuga'+str(i)+'.png'
        points.append(haralick(name,"tortuga"))

    root=build_kdtree(points)
    
    for i in range(1,6):
        name = r'C:\Users\user\.spyder-py3\kdtreee\Test\tortuga'+str(i)+'.png'
        test(name, root)
    print("-----------------")
    for i in range(1,6):
        name = r'C:\Users\user\.spyder-py3\kdtreee\Test\cocodrilo'+str(i)+'.png'
        test(name, root)
main()
