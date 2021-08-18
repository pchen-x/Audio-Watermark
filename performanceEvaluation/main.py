# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import numpy as np
from math import ceil

import imageProcessing.qrCode as qr
import universalTools.toolBox as tool
import imageProcessing.imageTransform as imgTrans
import audioProcessing.audioTransform as auTrans
import audioProcessing.watermark as watermark
from universalTools.utils import makeFileName, ImageToFlattedArray, fixSizeImg

audioLocation = ""
swTitle = "原创音乐保护音频水印系统"

# audio
LEN_FRAMES = 4
# DWT
WAVELET_TYPE = "db1"
WAVELET_MODE = "symmetric"


# 水印嵌入函数
# 参数：水印图片地址，待嵌入音乐地址
def embed(audioPath):
    img = qr.createQrcode(tool.getUserInfo())
    # qr.show_qrcode(img)
    qrPath = "C:/Users/admin/Desktop/image/Group-01/" + tool.toPng(tool.getFileName(audioPath))
    img.save(qrPath)
    fp = open(qrPath, 'rb')
    img = qr.openQrcode(img, fp)
    # qr.show_qrcode(img)
    print('Embedding...', audioPath)

    outputDir = tool.getDir(audioPath) + "/"
    outputAudioPath = outputDir + "New-" + tool.toWav(tool.getFileName(audioPath))

    print('!!!embedding algorithm starts here!!!')

    # 算法调用部分
    print('!!!01 Loading audio file!!!')
    audioData, tupleAudio = tool.getAudio(audioPath)

    print('!!!02 Running DWT on audio file!!!')
    DWTCoeffs = tool.getDwt(audioData, WAVELET_TYPE, WAVELET_MODE)
    cA, cD1 = DWTCoeffs

    print('!!!03 Dividing by frame!!!')
    frameLength = LEN_FRAMES
    cA = auTrans.audioToFrame(cA, frameLength)  # LEN_FRAMES)
    # DCTCoeffs = np.copy(cA)
    # LEN = len(cA)
    # width = ceil(LEN / LEN_FRAMES)
    # padLength = width * LEN_FRAMES - LEN
    # print(LEN, padLength, width)
    # cA = np.pad(cA, (0, padLength), 'constant', constant_values=(0))
    # DCTCoeffs = np.pad(DCTCoeffs, (0, padLength), 'constant', constant_values=(0))
    # DCTCoeffs = DCTCoeffs.reshape(width, LEN_FRAMES)

    print('!!!04 Running DCT on DWT coeffs!!!')
    DCTCoeffs = np.copy(cA)
    for i in range(cA.shape[0]):
        DCTCoeffs[i] = auTrans.runDct(cA[i])
    # i = 0
    # while i + LEN_FRAMES < width:
    #     DCTCoeffs[i] = auTrans.runDct(cA[i:i + LEN_FRAMES])
    #     i += LEN_FRAMES

    print('!!!05 Scrambling image watermark!!!')
    payload = tool.getScrambling(img)

    print('!!!06 embedding bruteGray watermark!!!')
    wCoeffs = watermark.bruteGray(DCTCoeffs, payload)

    print('!!!07 running iDCT!!!')
    iWCoeffs = np.copy(wCoeffs)
    for i in range(wCoeffs.shape[0]):
        iWCoeffs[i] = auTrans.runIDct(wCoeffs[i])

    print('!!!08 Joining audio frames!!!')
    # iWCoeffs = iWCoeffs.reshape(LEN + padLength)
    # iWCoeffs = iWCoeffs[0:LEN]
    # tool.getStego(iWCoeffs, tupleAudio, outputDir + "beforeIdwt.WAV")
    iWCoeffs = np.copy(wCoeffs)
    for i in range(wCoeffs.shape[0]):
        iWCoeffs[i] = auTrans.runIDct(wCoeffs[i])
    iWCoeffs = auTrans.frameToAudio(iWCoeffs)

    print('!!!09 Running iDWT')
    DWTCoeffs = iWCoeffs, cD1  # level 1
    iWCoeffs = auTrans.iDwt(DWTCoeffs, WAVELET_TYPE, WAVELET_MODE)

    print('!!!10 Saving new audio file!!!')
    tool.getStego(iWCoeffs, tupleAudio, outputAudioPath)

    print('!!!ends!!!')
    # qr.deleteQrcode()
    fp.close()

    return wCoeffs  # return information for extraction


# 水印提取函数
# 参数：已嵌入水印的音频地址
def extract(audioPath):
    print('Extracting...', audioPath)

    '''提取算法'''
    print('!!!01 Loading watermarked audio file!!!')
    audioData, tupleAudio = tool.getAudio(audioPath)
    stegoAudioData, stegoTupleAudio = tool.getAudio(audioPath)

    print('!!!02 Running DWT on audio file!!!')
    DWTCoeffs = tool.getDwt(audioData, WAVELET_TYPE, WAVELET_MODE)
    cA, cD1 = DWTCoeffs  # level 1

    stegoDWTCoeffs = tool.getDwt(stegoAudioData, WAVELET_TYPE, WAVELET_MODE)
    stegocA, stegocD1 = stegoDWTCoeffs  # level 1

    print('!!!03 Dividing by frame!!!')
    frameLength = LEN_FRAMES
    cA = auTrans.audioToFrame(cA, frameLength)
    print('!!!04 Running DCT on DWT coeffs!!!')
    DCTCoeffs = np.copy(cA)
    for i in range(cA.shape[0]):
        DCTCoeffs[i] = auTrans.runDct(cA[i])

    stegocA = auTrans.audioToFrame(stegocA, frameLength)  # LEN_FRAMES)
    stegoDCTCoeffs = np.copy(stegocA)
    for i in range(stegocA.shape[0]):
        stegoDCTCoeffs[i] = auTrans.runDct(stegocA[i])

    print('!!!05 Extracting image watermark!!!')
    payload = watermark.ibruteGray(stegoDCTCoeffs)

    # print(payload)
    print('!!!06 Inverting scrambling of payload!!!')
    payload = tool.getIScrambling(payload)
    qr.show_qrcode(payload)
    # print(payload)
    print('!!!07 Decoding image!!!')
    qrPath = "C:/Users/admin/Desktop/image/Group-01/" + tool.toPng(tool.getFileName(audioPath))
    payload.save(qrPath)
    fp = open(qrPath, 'rb')
    # qr.show_qrcode(img)
    img = qr.openQrcode(payload, fp)
    print(" ")
    print(" ")
    print("水印信息如下：")
    print(qr.decodeQrcode(img))
    # fp.close()
    # qr.deleteQrcode()


# 音频文件选择函数
def chooseFile():
    global audioLocation
    # 提示信息
    messagebox.showinfo(swTitle, "Make sure the file is a .wav format")
    # 在用户选择正确文件之前，一直搜寻
    searching = True
    while searching:
        audioLocation = ''
        audioLocation = filedialog.askopenfilename()  # 读取文件
        soundFormatSuffix = audioLocation[len(audioLocation) - 3:len(audioLocation)]  # 音频格式后缀
        soundFormatSuffix = soundFormatSuffix.lower()
        if soundFormatSuffix != "wav" and soundFormatSuffix != "":
            messagebox.showwarning("Error", "The audio has to be .wav format")
        else:
            searching = False
    if audioLocation != "":
        messagebox.showinfo(swTitle, "Sound Selected!")


# ============================以下是UI相关的对象定义======================================


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


# Hide picture page
class HidePicture(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        button2 = tk.Button(self, text="Choose Audio to Hide In", command=lambda: chooseFile())
        button3 = tk.Button(self, text="Go", command=lambda: embed(audioLocation))
        button2.pack(side="top", fill="both", expand=True)
        button3.pack(side="top", fill="both", expand=True)


# Extraction page
class ExtractPicture(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        button1 = tk.Button(self, text="Choose Sound File", command=lambda: chooseFile())
        button2 = tk.Button(self, text="Go", command=lambda: extract(audioLocation))
        button1.pack(side="top", fill="both", expand=True)
        button2.pack(side="top", fill="both", expand=True)


# Framework for pages
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = HidePicture(self)
        p2 = ExtractPicture(self)

        buttonFrame = tk.Frame(self)
        container = tk.Frame(self)
        buttonFrame.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonFrame, text="Hide a picture", command=p1.lift)
        b2 = tk.Button(buttonFrame, text="Extract a picture", command=p2.lift)

        b1.pack(side="left", fill="x", expand=True)
        b2.pack(side="left", fill="x", expand=True)

        p1.show()


# ============================以下是运行起点======================================
def main():
    # global swTitle
    root = tk.Tk()
    root.wm_title(swTitle)
    mainframe = MainView(root)
    mainframe.pack(side="top", fill="both", expand=True)
    root.wm_geometry("960x540")
    root.mainloop()


if __name__ == '__main__':
    print('here!')
    main()
    # qr.create_qrcode('test', './图片.png')
