# -*- coding: utf-8 -*-
from PIL import Image
import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cv2

key1 = cv2.imread("key/key1.png", 0)
key2 = cv2.imread("key/key2.png", 0)
height, width = key1.shape
dec = np.empty((height,width))

def dec_not_change():
	#そのまま復号
	for h in range(height):
		for w in range(width):
			if key1[h][w]==0 or key2[h][w]==0:
				dec[h][w] = 0
			else:
				dec[h][w] = 255

def dec_change():
	#見やすく復号
	for h in range(height):
		for w in range(width):
			if key1[h][w]==0 and key2[h][w]==255:
				dec[h][w] = 0
			elif key1[h][w]==255 and key2[h][w]==0:
				dec[h][w] = 0
			elif key1[h][w]==0 and key2[h][w]==0:
				dec[h][w] = 255
			else:
				dec[h][w] = 255


def main():
	

	#二つの鍵画像を透明にして重ねる
	#dst = cv2.addWeighted(key1, 0.5, key2, 0.5, 0)
	#key1.paste(key2)
	#size = key1.shape
	#mask = Image.new("L", key1.size, 128)
	#key = Image.composite(key1, key2, mask)
	
	dec_not_change()
	#dec_change()
	fig = plt.figure()
	plt.gray()
	plt.imshow(dec)
	plt.show()

if __name__=='__main__':
	main()
