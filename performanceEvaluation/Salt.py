from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy
import os
import math

class ImageData:
    'width,height为图像的宽和高，array为像素矩阵'
    width = -1
    height = -1
    array = []

    def __init__(self, w, h,arr):
        self.width = w
        self.height = h
        self.array = arr

def get_img_data(url):
    isExit = os.path.isfile(url)
    if isExit == False:
        print("打开失败!")
    # 打开图像并转化为数字矩阵
    img=Image.open(url)
    w,h = img.size
    array = np.array(img)
    # print(array.shape)
    # 图片展示
    # plt.figure(url)
    # plt.imshow(img)
    # plt.axis('off')
    # plt.show()
    # print(w,h)
    return ImageData(w,h,array)

def add_Salt(url,proportion):
    matrix = np.array(Image.open(url))
    # 随机生成椒盐
    rows, cols = matrix.shape
    length = math.ceil(rows * cols * proportion)
    # print(int(length))
    # print(length/(rows*cols))
    flag = np.ones((rows, cols), dtype=np.int32)
    for i in range(int(length)):
        test = 0
        while(test == 0):
            x = np.random.randint(0, rows)
            y = np.random.randint(0, cols)
            test=flag[x][y]
        flag[x][y] = 0
        if(matrix[x, y] == 255):
            matrix[x, y] = 0
        else:
            matrix[x, y] = 255
    img = Image.fromarray(matrix)
    img.save('./photo/salt.png')


add_Salt('./photo/灰度图.png',0.2)
# print(type(ber))