import os
import qrcode
import pyzbar.pyzbar as pzb
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def add_logo(photo, codename):
    img = photo.make_image()
    img = img.convert("RGBA")  # 二维码设为彩色
    logo = Image.open('./1.jpg')  # 传gif生成的二维码也是没有动态效果的

    w, h = img.size
    logo_w, logo_h = logo.size
    factor = 4  # 默认logo最大设为图片的四分之一
    s_w = int(w / factor)
    s_h = int(h / factor)
    if logo_w > s_w or logo_h > s_h:
        logo_w = s_w
        logo_h = s_h

    logo = logo.resize((logo_w, logo_h), Image.ANTIALIAS)
    l_w = int((w - logo_w) / 2)
    l_h = int((h - logo_h) / 2)
    logo = logo.convert("RGB")
    img.paste(logo, (l_w, l_h), logo)
    show_qrcode(img)
    img.save(os.getcwd() + '/' + codename + '.png', quality=100)


def show_qrcode(picture):
    # picture.show()
    plt.figure("Image")  # 图像窗口名称
    plt.imshow(picture, cmap='gray')
    plt.axis('on')  # 关掉坐标轴为 off
    plt.title('image')  # 图像题目
    plt.show()
    print(np.asarray(picture))


def openQrcode(img, filePath='./tmp.png'):
    img = Image.open(filePath)
    return img


def deleteQrcode():
    filePath = './tmp.png'
    os.remove(filePath)


def imageScaling(origin):
    out = origin.resize((128, 128), Image.ANTIALIAS)  # resize image with high-quality
    return out


# def create_qrcode(content, file_path):
def createQrcode(content):
    qr = qrcode.QRCode(
        version=1,
        # 设置容错率为最高
        error_correction=qrcode.ERROR_CORRECT_H,  # 用于控制二维码的错误纠正程度
        box_size=1,  # 控制二维码中每个格子的像素数，默认为10
        border=1,  # 二维码四周留白，包含的格子数，默认为4
        # image_factory=None,  保存在模块根目录的image文件夹下
        # mask_pattern=None
    )

    qr.add_data(content)  # QRCode.add_data(data)函数添加数据
    qr.make(fit=True)  # QRCode.make(fit=True)函数生成图片
    img = qr.make_image()
    # show_qrcode(img)
    img = imageScaling(img)
    # show_qrcode(img)
    img = img.convert("L")
    # show_qrcode(img)
    # img.save(file_path)
    return img


# def decode_qr_code(code_img_path):
def decodeQrcode(img):
    # if not os.path.exists(code_img_path):
    #     raise FileExistsError(code_img_path)
    # Here, set only recognize QR Code and ignore other type of code
    # return pzb.decode(Image.open(code_img_path), symbols=[pzb.ZBarSymbol.QRCODE])
    img = img.convert("1")
    show_qrcode(img)
    context = pzb.decode(img)
    # print(context)
    data = ''
    if context:
        for i in context:
            # 二维码路径
            j = i.data.decode("utf-8")
            # print(barcodeData)
            data = j
    return data


if __name__ == '__main__':
    words = "上传者：XYX\n发表时间：2021.04.21\nMAC地址：fe80::3c3a:585c:4039:639b\nIP地址：10.132.246.23\n"
    path = "./灰度图.png"
    # IMG = create_qrcode(words, path)
    # IMG.save(path)
    # IMG = Image.open(path)
    # show_qrcode(IMG)
    # res = decodeQrcode(path)
    # print(res)
