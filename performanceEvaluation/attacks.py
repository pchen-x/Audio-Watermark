import subprocess as sp
import platform
import os
import numpy as np
import sys

sys.path.append("..")
from universalTools.utils import makeFileName


# The audio amplitude is scaling of factor t
def amplitudeScaling(data, t):
    return data * t


# The audio is resampled
def resampling(path, sampleRate):
    name = makeFileName(str(sampleRate), path)
    sample = makeFileName("ReSample", path)
    if platform.system() == "Linux":
        cmdffmpegL = "ffmpeg -y -i {} -ar {} -f wav {}" \
            .format(path, sampleRate, name)
        os.system(cmdffmpegL)
    elif platform.system() == "Windows":
        cmdffmpegW = "C:/Users/admin/Desktop/Watermark/code/ffmpeg/bin/ffmpeg.exe -y -i {} -ar {} -f wav {}" \
            .format(path, sampleRate, name)
        sp.call(cmdffmpegW)
        cmdffmpegW = "C:/Users/admin/Desktop/Watermark/code/ffmpeg/bin/ffmpeg.exe -y -i {} -ar {} -f wav {}" \
            .format(name, 44100, sample)
        sp.call(cmdffmpegW)
    return name


# It calculates the Low Pass Butterworth based on its mathematic formula (it's used in frequency domain)
def butterLPFilter(data, frequency, n=1):  # n is order filter
    mask = np.zeros(data.size)
    for i in range(int(len(mask) / 2)):
        mask[i] = 1 / (1 + (i / frequency) ** (2 * n))
        mask[len(mask) - 1 - i] = mask[i]
    return mask * data


def gaussianNoise(data, sigma):
    noise = np.random.normal(0.0, sigma, data.size)
    return data + noise


# if __name__ == "__main__":
#     filepath = "./testData/New-CruelSummer-60s.wav"
#     sampleRate = 22050
#     resampling(filepath, sampleRate)
