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

n = input("n: ")
n = int(n)
k = 3
B = [[0 for w in range(n-2)]for h in range(n)]
I = [[0 for w in range(n)]for h in range(n)]
BI = [[0 for w in range(2*n-2)]for h in range(n)]
cBI = [[0 for w in range(2*n-2)]for h in range(n)]

for h in range(n):
	for w in range(n-2):
		B[h][w] = 1

for h in range(n):
	for w in range(n):
		if h==w:
			I[h][w] = 1
		else:
			I[h][w] = 0

BI = B
for i in range(n):
	BI[i].extend(I[i])

for h in range(n):
	for w in range(2*n-2):
		if BI[h][w] == 0:
			cBI[h][w] = 255
		else:
			BI[h][w] = 255
			cBI[h][w] = 0


key = [[[0 for w in range(width*(2*n-2))]for h in range(height)]for i in range(n)]
resize_key = [[0 for w in range(width*(2*n-2))]for h in range(height*(2*n-2))]

dec = np.empty((height,width)) #復号画像

#解像度
pic_dpi = 350

#print(height,width)
#print(gray)
l = list(range(2*n-2))
r = [[0]*(2*n-2)]*n

def pattern(bw, h, w):
	random.shuffle(l)
	
	if bw==0:
		for i in range(n): #BIの列をランダムに並び替えてrに格納する。
			for j in range(2*n-2):
				r[i][j] = BI[i][l[j]]
				key[i][h][w*(2*n-2)+j] = r[i][j]
		
	elif bw==255:
		for i in range(n): #cBIの列をランダムに並び替えてrに格納する。
			for j in range(2*n-2):
				r[i][j] = cBI[i][l[j]]
				key[i][h][w*(2*n-2)+j] = r[i][j]
		

	"""
	if bw==0:
		for i in range(k): #行
			r = random.randrange(k)
			for j in range(n): #key
				key[j][h+i][w+r] = 255

	elif bw==255:
		l0 = list(range(k))
		random.shuffle(l0)
		for i in range(k): #行
			l = list(range(k))
			random.shuffle(l)
			for j in range(k): #key(k個)
				key[j][h+i][w+l[j]] = 255
		for i in range(k): #行
			for j in range(k, n): #key(n-k個)
				for m in range(k): #列
					key[j][h+i][w+m] = key[(j-k+i)%k][h+i][w+m]
	"""
			
	"""
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
		"""

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

	for h in range(height):
		for w in range(width):
			if err[h][w]==0:
				pattern(0, h, w)
			elif err[h][w]==255:
				pattern(255, h, w)

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

def display_keys(key):
	plt.gca().spines['right'].set_visible(False) # 右消し
	plt.gca().spines['left'].set_visible(False)
	plt.gca().spines['bottom'].set_visible(False)
	plt.gca().spines['top'].set_visible(False)
	plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
	plt.tick_params(color='white')
	#ax.tick_params(labelbottom="off",bottom="off") # x軸の削除
	#ax.tick_params(labelleft="off",left="off") # y軸の削除
	#ax.set_xticklabels([])
	#fig1.patch.set_alpha(0.5)
	plt.imshow(key)
	#plt.savefig('Gray_pic/key1.png')

def resize_keys(key):
	for h in range(height):
		for i in range(2*n-2):
			for w in range((2*n-2)*width):
				resize_key[h*(2*n-2)+i][w] = key[h][w] #画像のアスペクト比をもとに戻す
	plt.imshow(resize_key)

def main(): 

	error_dif() #グレースケール画像を二値画像に変換
	draw_key() #鍵を2つ作成する
	display_orig_pic() #グレースケール画像を表示
	display_err_dif_pic() #二値画像を表示

	
	for i in range(n):
		fig = plt.figure(figsize=(1,1),dpi=pic_dpi)
		plt.plot()
		resize_keys(key[i])
		display_keys(resize_key) #鍵画像1を表示
		fig.savefig('key/key'+ str(i+1) +'.png')
	
	#fig2, ax2 = plt.subplots(dpi=pic_dpi*2)
	#display_keys(key2, ax2) #鍵画像2を表示
	#fig2.savefig('key/key2.png')

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
