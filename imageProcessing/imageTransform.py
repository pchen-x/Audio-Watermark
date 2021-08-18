from PIL import Image
import numpy as np
import math
import sys

sys.path.append("..")
from universalTools.utils import imodule, coprime


# from watermark_embedding_extraction import LSB

# Return numpy array from a Image file
# 从图像文件中返回一个numpy数组
def loadImage(path=""):
    if path is "":
        sys.exit("LOAD IMAGE: Path must not be None!")

    img = Image.open(path)
    return img


# Show image from array or path
# 展示图像
def showImage(img):
    # print('Test show image')
    if type(img) is not str:
        img.show()
    else:
        if img is "":
            sys.exit("SHOW IMAGE: Path must not be None!")
        # Image.open(img).show()
        img.show()


# Save image from array or Image file
# 保存图像
def saveImage(img, path):
    if path is "":
        sys.exit("SHOW IMAGE: Path must not be None!")
    img.save(path)


# 转化为灰度图像
def grayscale(img):
    return img.convert(mode="L")


# Return binarized image
# 返回二值化的图像
def binarization(img):
    """ img.convert(mode=None, matrix=None, dither=None, palette=0, colors=256)
    PIL有九种不同模式: 1（二值图），L（灰度图），P，RGB，RGBA，CMYK，YCbCr，I，F
    matrix：可选的转换矩阵。如果给定，则应为包含浮点值的4元组或12元组。
    dither：抖动方法，在从模式“RGB”转换为“ P”或从“ RGB”或“ L”转换为“1”时使用。可用的方法有：data：`NONE`或：data：`FLOYDSTEINBERG`（默认）。
    请注意，在提供matrix时不使用此选项。
    palette：从模式“ RGB”转换为“ P”时使用的调色板。可用的调色板是WEB或ADAPTIVE。
    colors：用于“ ADAPTIVE”调色板的颜色数。 默认值为256。"""

    return img.convert(mode="1", dither=0)


# Return image size
# 返回图像尺寸
def imgSize(img):
    if type(img) is np.ndarray:
        width, height = (img.shape[1], img.shape[0])
        # 图像的宽和高
    else:
        width, height = img.size
    return width, height


# Arnold transform
# arnold 变换
def arnoldTransform(img, iteration):
    width, height = imgSize(img)
    if width != height:
        sys.exit("ARNOLD TRANSFORM: Image must be square!")
    side = width
    toTransform = img.copy()
    transformed = img.copy()

    for iterate in range(iteration):
        for i in range(side):
            for j in range(side):
                newX = (i + j) % side
                newY = (i + 2 * j) % side
                value = toTransform.getpixel(xy=(i, j))
                transformed.putpixel(xy=(newX, newY), value=value)
        toTransform = transformed.copy()

    return transformed


# Inverse Arnold transform
# 逆Arnold变换
def iArnoldTransform(img, iteration):
    width, height = imgSize(img)
    if width != height:
        sys.exit("I_ARNOLD TRANSFORM: Image must be square!")
    side = width
    transformed = img.copy()
    toTransform = img.copy()

    for iterate in range(iteration):
        for i in range(side):
            for j in range(side):
                newX = (2 * i - j) % side
                newY = (-i + j) % side
                value = toTransform.getpixel(xy=(i, j))
                transformed.putpixel(xy=(newX, newY), value=value)
        toTransform = transformed.copy()
    return transformed


# 2D lower triangular mapping
# 二维下三角映射
def lowerTriangularMappingTransform(img, iteration, c, a=-1, d=-1):
    width, height = imgSize(img)
    coprime_mode = "first"
    if a == -1 and d == -1:
        a = coprime(width, coprime_mode)
        d = coprime(height, coprime_mode)

    transformed = img.copy()
    toTransform = img.copy()

    for iterate in range(iteration):

        for i in range(width):
            for j in range(height):
                newX = (a * i) % width
                newY = (c * i + d * j) % height
                value = toTransform.getpixel(xy=(i, j))
                transformed.putpixel(xy=(newX, newY), value=value)

        toTransform = transformed.copy()

    return transformed


# 2D inverse lower triangular mapping
# 二维逆下三角映射
def iLowerTriangularMappingTransform(img, iteration, c, a=-1, d=-1):
    width, height = imgSize(img)
    coprime_mode = "first"
    if a == -1 and d == -1:
        a = coprime(width, coprime_mode)
        d = coprime(height, coprime_mode)

    transformed = img.copy()
    toTransform = img.copy()
    i_a = imodule(a, width)
    i_d = imodule(d, height)
    for iterate in range(iteration):

        for i in range(width):
            for j in range(height):
                newX = (i_a * i) % width
                newY = (i_d * (j + (math.ceil(c * width / height) * height) - (c * newX))) % height
                value = toTransform.getpixel(xy=(i, j))
                transformed.putpixel(xy=(newX, newY), value=value)

        toTransform = transformed.copy()
    return transformed


# 2D upper triangular mapping
# 二维上三角映射
def upperTriangularMappingTransform(img, iteration, c, a=-1, d=-1):
    width, height = imgSize(img)
    coprime_mode = "first"
    if a == -1 and d == -1:
        a = coprime(width, coprime_mode)
        d = coprime(height, coprime_mode)

    transformed = img.copy()
    toTransform = img.copy()

    for iterate in range(iteration):

        for i in range(width):
            for j in range(height):
                newX = (a * i + c * j) % width
                newY = (d * j) % height
                value = toTransform.getpixel(xy=(i, j))
                transformed.putpixel(xy=(newX, newY), value=value)

        toTransform = transformed.copy()

    return transformed


# 2D inverse upper triangular mapping
# 二维逆上三角映射
def iUpperTriangularMappingTransform(img, iteration, c, a=-1, d=-1):
    width, height = imgSize(img)
    coprime_mode = "first"
    if a == -1 and d == -1:
        a = coprime(width, coprime_mode)
        d = coprime(height, coprime_mode)

    transformed = img.copy()
    toTransform = img.copy()
    i_a = imodule(a, width)
    i_d = imodule(d, height)
    for iterate in range(iteration):

        for i in range(width):
            for j in range(height):
                newY = (i_d * j) % height
                newX = (i_a * (i + (math.ceil(c * height / width) * width) - (c * newY))) % width
                value = toTransform.getpixel(xy=(i, j))
                transformed.putpixel(xy=(newX, newY), value=value)

        toTransform = transformed.copy()
    return transformed


def mappingTransform(mode, img, iteration, c, a=-1, d=-1):
    if mode is "lower":
        mapped = lowerTriangularMappingTransform(img, iteration, c, a, d)
    elif mode is "upper":
        mapped = upperTriangularMappingTransform(img, iteration, c, a, d)
    else:
        sys.exit("MAPPING TRANSFORM: Mode must be lower or upper!")
    return mapped


def iMappingTansform(mode, img, iteration, c, a=-1, d=-1):
    if mode is "lower":
        mapped = iLowerTriangularMappingTransform(img, iteration, c, a, d)
    elif mode is "upper":
        mapped = iUpperTriangularMappingTransform(img, iteration, c, a, d)
    else:
        sys.exit("MAPPING TRANSFORM: Mode must be lower or upper!")
    return mapped


'''
TESTING
'''
'''
if __name__ == "__main__":
    photo = load_image("./right.png")
    # 载入图像
    img_r = load_image("./07.jpg")
    # 转为二值图
    # img_r = binarization(img_r)
    # img_r = grayscale(img_r)

    # t = arnold_transform(photo, iteration=1)
    # show_image(t)

    # it = i_arnold_transform(t, iteration=1)
    # show_image(it)

    # m = mapping_transform(mode="lower", img=img_r, iteration=1, c=3, a=5)
    # show_image(m)
    # # saveImage(m, "triangular_2_iterations.png")

    # im = i_mapping_transform(mode="lower", img=m, iteration=1, c=3, a=5)
    # show_image(im)

    # m1 = mapping_transform(mode="upper", img=img_r, iteration=1, c=3)
    # show_image(m1)
    # # saveImage(m, "triangular_2_iterations.png")

    # im1 = i_mapping_transform(mode="upper", img=m1, iteration=1, c=3)
    # show_image(im1)
'''
