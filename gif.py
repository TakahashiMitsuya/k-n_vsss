import glob
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.animation as animation

if __name__ == "__main__":

	folderName = "key"

	#画像ファイルの一覧を取得
	picList = glob.glob(folderName + "\*.png")

	#figオブジェクトを作る
	fig = plt.figure()
	ax = plt.subplot(1,1,1)

	#空のリストを作る
	ims = []

	#画像ファイルを順々に読み込んでいく
	for i in range(len(picList)):
 
		#1枚1枚のグラフを描き、appendしていく
		tmp = Image.open(picList[i])
		ims.append([plt.imshow(tmp)])     

	#アニメーション作成    
	ani = animation.ArtistAnimation(fig, ims, interval=1, repeat_delay=0.01)	
	plt.show()

	ax.spines["right"].set_color("none")  # 右消し
	ax.spines["left"].set_color("none")   # 左消し
	ax.spines["top"].set_color("none")    # 上消し
	ax.spines["bottom"].set_color("none") # 下消し
	ax.tick_params(labelbottom="off",bottom="off") # x軸の削除
	ax.tick_params(labelleft="off",left="off") # y軸の削除
	ax.set_xticklabels([])
	
	ani.save("ani_VSSS.gif", writer="imagemagick")
	
	
