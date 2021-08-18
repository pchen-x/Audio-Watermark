from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import math


class ImageData:
    'width,height为图像的宽和高，array为像素矩阵'
    width = -1
    height = -1
    array = []

    def __init__(self, w, h, arr):
        self.width = w
        self.height = h
        self.array = arr


def get_img_data(url):
    isExit = os.path.isfile(url)
    if isExit == False:
        print("打开失败!")
    # 打开图像并转化为数字矩阵
    img = Image.open(url)
    img = img.convert("1")
    w, h = img.size
    array = np.array(img)
    print(array)
    # 图片展示
    # plt.figure(url)
    # plt.imshow(img)
    # plt.axis('off')
    # plt.show()
    # print(w,h)
    return ImageData(w, h, array)


def judge(x, y):
    flag = False
    if x != y:
        flag = True
    return flag


def BER(ref_url, in_url):
    reference = get_img_data(ref_url)
    input = get_img_data(in_url)
    if reference.width != input.width or reference.height != input.height:
        return '图像尺寸不符'
    i = j = 0
    res = float(0)
    # print(type(res))
    w = reference.width
    h = reference.height
    # print(w, h)

    while i < w:
        j = 0
        while j < h:
            if judge(reference.array[i][j], input.array[i][j]):
                res += float(1)
                # if i == 21 and j == 117:
                #     print(int(res), ":", i, j, reference.array[i][j], input.array[i][j])
            j += 1
        i += 1

    print(res, w * h)
    res /= float(w * h)
    return res
    # print(ref_data)


if __name__ == "__main__":
    # ber = BER('./testData/CruelSummer-60s.png', './testData/New-CruelSummer-60s.png')
    # print('BER:%0.6f' % ber)

    img = Image.open('./testData/CruelSummer-60s.png')
    img = img.convert("1")
    img.save('./testData/CruelSummer-60s-binary.png')

    img = Image.open('./testData/New-CruelSummer-60s.png')
    img = img.convert("1")
    img.save('./testData/New-CruelSummer-60s-binary.png')
# print(type(ber))
