from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random

#画像読み込み
file_name = input("File name: ")
gray = cv2.imread(file_name,0)
height, width = gray.shape #解像度 縦,横
err = np.empty((height,width)) #誤差拡散法の画像
key1 = np.empty((height*2,width*2)) #鍵画像1
key2 = np.empty((height*2,width*2)) #鍵画像2
dec = np.empty((height,width)) #復号画像

#解像度
pic_dpi = 350

#print(height,width)
#print(gray)

def pattern(bw, h, w, key1, key2):
	r = random.randrange(2)
	if bw==0: #1画素が黒のとき
		if r==0:
			key1[h][w] = 255 #左上 白
			key1[h][w+1] = 0 #右上 黒
			key1[h+1][w] = 0
			key1[h+1][w+1] = 255
			key2[h][w] = 0
			key2[h][w+1] = 255
			key2[h+1][w] = 255
			key2[h+1][w+1] = 0
		elif r==1:
			key1[h][w] = 0 #左上 黒
			key1[h][w+1] = 255 #右上 白
			key1[h+1][w] = 255
			key1[h+1][w+1] = 0
			key2[h][w] = 255
			key2[h][w+1] = 0
			key2[h+1][w] = 0
			key2[h+1][w+1] = 255

	elif bw==255:
		if r==0:
			key1[h][w] = 255 #左上 白
			key1[h][w+1] = 0 #右上 黒
			key1[h+1][w] = 0
			key1[h+1][w+1] = 255
			key2[h][w] = 255
			key2[h][w+1] = 0
			key2[h+1][w] = 0
			key2[h+1][w+1] = 255
		elif r==1:
			key1[h][w] = 0 #左上 黒
			key1[h][w+1] = 255 #右上 白
			key1[h+1][w] = 255
			key1[h+1][w+1] = 0
			key2[h][w] = 0
			key2[h][w+1] = 255
			key2[h+1][w] = 255
			key2[h+1][w+1] = 0
		

def draw_key():
	#グレースケール反転
	"""
	for h in range(height):
		for w in range(width):
			key1[h][w] = 255 - gray[h][w]
	"""

	#グレースケール分散
	"""
	for h in range(height): #高さ
		for w in range(width): #幅
			r = random.randrange(gray[h][w])
			key1[h][w] = r
			key2[h][w] = gray[h][w] - r
	"""

	for h in range(0, height*2, 2):
		for w in range(0, width*2, 2):
			if err[h//2][w//2]==0:
				pattern(0, h, w, key1, key2)
			elif err[h//2][w//2]==255:
				pattern(255, h, w, key1, key2)

def error_dif():
	
	#繰り返し法
	"""
	x = 0 #仮変数
	for h in range(height):
		for w in range(width):
			x = x + gray[h][w] 
	#グレースケールの1画素の諧調が255を超えれば白、越えなければ黒を格納する。
			if x >= 128:
				err[h][w] = 255
				x = x - 255
			else:
				err[h][w] = 0
	"""

	#誤差拡散法
	
	x = 0 #仮変数
	for h in range(height):
		for w in range(width):
			x = x + gray[h][w] 
	#グレースケールの1画素の諧調が255を超えれば白、越えなければ黒を格納する。
			if x >= 128:
				err[h][w] = 255
				x = x - 255
			else:
				err[h][w] = 0
				
			if w != width-1:
				err[h][w+1] += x*5//16
			if h != height-1 and w != 0:
				err[h+1][w-1] += x*3//16
			if h != height-1:
				err[h+1][w] += x*5//16
			if h != height-1 and w != width-1:
				err[h+1][w+1] += x*3//16


def display_orig_pic():
	fig, ax = plt.subplots()
	plt.imshow(gray)
	plt.gray()

def display_err_dif_pic():
	fig, ax = plt.subplots()
	plt.imshow(err)
	#fig.savefig('bw.png')

def display_keys(key, ax):
	ax.spines["right"].set_color("none")  # 右消し
	ax.spines["left"].set_color("none")   # 左消し
	ax.spines["top"].set_color("none")    # 上消し
	ax.spines["bottom"].set_color("none") # 下消し
	ax.tick_params(labelbottom="off",bottom="off") # x軸の削除
	ax.tick_params(labelleft="off",left="off") # y軸の削除
	ax.set_xticklabels([])
	
	#fig1.patch.set_alpha(0.5)
	plt.imshow(key)
	#plt.savefig('Gray_pic/key1.png')

def main(): 

	error_dif() #グレースケール画像を二値画像に変換
	draw_key() #鍵を2つ作成する
	display_orig_pic() #グレースケール画像を表示
	display_err_dif_pic() #二値画像を表示

	
	
	fig1, ax1 = plt.subplots(dpi=pic_dpi*2)
	display_keys(key1, ax1) #鍵画像1を表示
	fig1.savefig('key/key1.png')
	
	fig2, ax2 = plt.subplots(dpi=pic_dpi*2)
	display_keys(key2, ax2) #鍵画像2を表示
	fig2.savefig('key/key2.png')

	plt.show()


if __name__=='__main__':
	main()

"""
#画像の読み込み
im1 = np.array(Image.open('falilv4,jpg').convert('L'))
im2 = np.array(Image.open('falilv5.jpg').convert('L'))
#画像をarrayに変換
#im_list = np.asarray(im)
#貼り付け
"""
"""
th = 125
im_bin_128 = (im > th)*255
"""
"""
fig = plt.figure()
plt.imshow(im1)
fig = plt.figure()
plt.imshow(im2)
#表示
plt.show()
"""
