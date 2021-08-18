import os
import time
import socket
from scipy.io import wavfile
from psutil import net_if_addrs
import audioProcessing.audioTransform as auTrans
import imageProcessing.imageTransform as imgTrans

# audio
T_AUDIO_PATH = 0
T_SAMPLERATE = 1

# DWT
WAVELETS_LEVEL = 1

# scrambling
SCRAMBLING_TECHNIQUES = ["arnold", "lower", "upper"]
BINARY = 0
GRAYSCALE = 1
NO_ITERATIONS = 1
TRIANGULAR_PARAMETERS = [5, 3, 1]  # c,a,d


def createDir(dirPath):
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)


def getHostIp():
    """
    查询本机ip地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def getHostMac():
    # 获取mac地址
    # addr_num = hex(uuid.getnode())[2:]
    # mac = "-".join(addr_num[i: i + 2] for i in range(0, len(addr_num), 2))
    # print(mac)
    res = list()
    # 获取本机所有网卡的mac地址
    for k, v in net_if_addrs().items():
        for item in v:
            address = item[1]
            if "-" in address and len(address) == 17:
                res.append(address)
                # print(address)
    return res


def getUserInfo():
    name = "一位不知名的意呆利炼丹人"
    currentTime = time.asctime(time.localtime(time.time()))
    macAddr = getHostMac()
    # dict = {'name': 1, 'publishTime': currentTime, 'publishIP': getHostIp()}
    res = "name:" + name + '\n'
    res = res + "publishTime:" + currentTime + '\n'
    res = res + "publishIP:" + getHostIp() + '\n'
    res = res + "publishMAC:"
    for i in range(len(macAddr)):
        res = res + macAddr[i] + '\n'
    return res


def getDir(path):
    res = os.path.dirname(path)
    return res
    # fileName = prefix + "-" + fileName
    # res = os.path.join(dirName, fileName)
    # os.getcwd()  # 获取当前工作目录路径
    # os.path.abspath('.')  # 获取当前工作目录路径
    # os.path.abspath('test.txt')  # 获取当前目录文件下的工作目录路径
    # os.path.abspath('..')  # 获取当前工作的父目录 ！注意是父目录路径
    # os.path.abspath(os.curdir)  # 获取当前工作目录路径


def getFileName(path):
    res = os.path.basename(path)
    return res


def toWav(path):
    res = path[0:len(path) - 3] + "wav"
    return res


def toPng(path):
    res = path[0:len(path) - 3] + "png"
    return res


def getAudio(path):
    tupleAudio = auTrans.readWavFile(path)
    audioData = auTrans.audioData(tupleAudio)
    if not auTrans.isMono(audioData):
        tupleAudio = auTrans.joinAudioChannels(path)
        audioData = auTrans.audioData(tupleAudio)
    return audioData, tupleAudio


def getDwt(audioData, type, mode):
    waveletsFamilies = auTrans.getWaveletsFamilies()
    DWTFamilies = auTrans.filterWaveletsFamilies(waveletsFamilies)
    waveletsModes = auTrans.getWaveletsModes()
    coeffs = auTrans.dwt(audioData, DWTFamilies[DWTFamilies.index(type)], waveletsModes[waveletsModes.index(mode)],
                         WAVELETS_LEVEL)
    return coeffs


def getScrambling(img):
    image = imgTrans.grayscale(img)
    image = imgTrans.mappingTransform("lower", image, NO_ITERATIONS, TRIANGULAR_PARAMETERS[0], TRIANGULAR_PARAMETERS[1],
                                      TRIANGULAR_PARAMETERS[2])
    # image = imgTrans.arnoldTransform(image, NO_ITERATIONS)
    return image


def getIScrambling(img):
    image = imgTrans.iMappingTansform("lower", img, NO_ITERATIONS, TRIANGULAR_PARAMETERS[0],
                                      TRIANGULAR_PARAMETERS[1],
                                      TRIANGULAR_PARAMETERS[2])
    # image = imgTrans.iArnoldTransform(img, NO_ITERATIONS)
    return image


def getStego(data, tupleAudio, outputAudioPath):
    nData = auTrans.normalizeForWav(data)
    print(tupleAudio)
    wavfile.write(outputAudioPath, tupleAudio[T_SAMPLERATE], nData)
    # auTrans.saveWavFile(tupleAudio[T_AUDIO_PATH], tupleAudio[T_SAMPLERATE], , outputAudioPath)


def getPayload(image, outputImagePath):
    # fileName = makeFileName(outputImageName, outputImagePath)
    imgTrans.saveImage(image, outputImagePath)


if __name__ == "__main__":
    data, info = getAudio('../audioDataset/piano.wav')
    # print(data)
    # print(info)
    # print(getHostMac())
    # print(getDir('./test.txt'))
    # print(getFileName('./test.txt'))
    # print(toWav('./test.txt'))
