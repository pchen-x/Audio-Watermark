import os
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import dct, idct, fft, fftfreq, ifft
import subprocess as sp
import platform
import pywt
import sys

sys.path.append("..")
from universalTools.utils import makeFileName, withoutExtensionFile

AUDIO_PATH = 0
SAMPLERATE = 1
AUDIO_DATA = 2
WAVELETS_LEVEL = 2

DWT_SET = {"haar", "bior1.1", "bior1.3", "bior1.5", "bior2.2", "bior2.4", "bior2.6", "bior2.8", "bior3.1", "bior3.3",
           "bior3.5", "bior3.7", "bior3.9", "bior4.4", "bior5.5", "bior6.8", "coif1", "coif2", "coif3", "coif4",
           "coif5", "coif6", "coif7", "cdb3oif8", "coif9", "coif10", "coif11", "coif12", "coif13", "coif14", "coif15",
           "coif16", "coif17", "db1", "db2", "db3", "db4", "db5", "db6", "db7", "db8", "db9", "db10", "db11", "db12",
           "db13", "db14", "db15", "db16", "db17", "db18", "db19", "db20", "db21", "db22", "db23", "db24", "db25",
           "db26", "db27", "db28", "db29", "db30", "db31", "db32", "db33", "db34", "db35", "db36", "db37", "db38",
           "dmey", "rbio1.1", "rbio1.3", "rbio1.5", "rbio2.2", "rbio2.4", "rbio2.6", "rbio2.8", "rbio3.1", "rbio3.3",
           "rbio3.5", "rbio3.7", "rbio3.9", "rbio4.4", "rbio5.5", "rbio6.8", "sym2", "sym3", "sym4", "sym5", "sym6",
           "sym7", "sym8", "sym9", "sym10", "sym11", "sym12", "sym13", "sym14", "sym15", "sym16", "sym17", "sym18",
           "sym19", "sym20"}


# Read the file audio.wav from path
# 读取WAV文件并一（路径，采样率，数据）元组形式输出
def readWavFile(path=""):
    if path == "":
        sys.exit("READ WAV FILE must have valid path!")
    samplerate, data = wavfile.read(path)
    tupleWav = (path, samplerate, data)
    return tupleWav


# Print some information about file audio
# 以元组形式打印读入音频的信息
def printMetadata(entry):
    print("Path: {}".format(entry[AUDIO_PATH]))
    print("\tsamplerate: {}".format(entry[SAMPLERATE]))
    print("\t#samples: {}".format(entry[AUDIO_DATA].shape))


# Check the number of channels of audio file
# mono - 单声道的
def isMono(data_audio):
    return True if len(data_audio.shape) == 1 else False


# Normalize data signal in int16 suitable for wav library
def normalizeForWav(data):
    return np.int16(data.real)


# Save processed file audio with wav format
def saveWavFile(path, samplerate, signal, prefix):
    # print(path)
    path = makeFileName(prefix, path)
    # print(path)
    wavfile.write(path, samplerate, signal)


# Join audio channels to only one
# 被音乐人暗鲨函数
def joinAudioChannels(path):
    outPath = makeFileName("mono", path)
    print("输入路径：", path)
    if platform.system() == "Linux":
        cmd_ffmpeg_L = "ffmpeg -y -i {} -ac 1 -f wav {}".format(path, outPath)
        os.system(cmd_ffmpeg_L)
    elif platform.system() == "Windows":
        cmd_ffmpeg_W = "C:/Users/admin/Desktop/Watermark/code/ffmpeg/bin/ffmpeg.exe -y -i {} -ac 1 -f wav {}".format(
            path, outPath)
        sp.call(cmd_ffmpeg_W)
    tupleMono = readWavFile(outPath)
    return tupleMono


# Return array of data audio
def audioData(audio):
    return audio[AUDIO_DATA]


# Divide audio in frames
# 对音频进行分帧，audio为数据，length为单帧长度
def audioToFrame(audio, length):
    # print('!!')
    # print('original audio:', audio)
    print('original audio shape:', len(audio))
    numFrames = math.ceil(audio.shape[0] / length)
    frames = list()
    # print(audio[0 * length: (0 * length) + length])
    for i in range(numFrames):
        frames.append(audio[i * length: (i * length) + length])
    # l = len(frames) - 1
    # padLength = length - frames[l].shape[0]
    # frames[l] = np.pad(frames[l], (0, padLength), 'constant', constant_values=(0))
    # print('last frame:', frames[l])

    res = np.asarray(frames)
    # print(res.shape)
    # print(res)
    return res


# Join frames to single array
# 将多个帧合并为单个音频数据数组
def frameToAudio(frames):
    audio = []
    LEN = len(frames)
    # tmp = frames[0]
    for i in range(LEN):
        audio = np.concatenate((audio, frames[i]))
        # if i == 0:
        #     continue
        # elif i % 10 == 0 or LEN - i < 10:
        #
        #     tmp = frames[i]
        # else:
        #     tmp += frames[i]
        if i % 10000 == 0:
            print(i)
    # if(LEN-1) % 10 == 0:
    #     audio = np.concatenate((audio, frames[LEN-1]))
    # print('reassembled audio:', audio)
    print('reassembled audio shape:', len(audio))
    return audio


# Plot the waveform of input audio file
# 将音频文件使用matplotlib绘制出来并保存图像
# namefile保存路径与代码相同
# name保存路径与音频相同
def waveform(entry):
    plt.figure()
    plt.plot(entry[AUDIO_DATA][:1000])
    plt.title("Waveform: {}".format(entry[AUDIO_PATH]))
    nameFile = makeFileName("1000", entry[AUDIO_PATH])
    # nameFile = withoutExtensionFile(entry[AUDIO_PATH], "1000")
    # print(entry[AUDIO_PATH])
    l = len(nameFile)
    name = nameFile[0:l - 3] + 'png'
    plt.savefig(name)
    # plt.savefig(nameFile)
    plt.show()


# Get the list of all wavelets
# pywt.wavelist(family = None, kind = 'all')
# family：小波族的名称
# kind：可以查看小波族下全部、离散、连续的小波
def getWaveletsFamilies():
    return pywt.wavelist()  # 查看每个小波族中提供的系数


# Get the list of all signal extension modes
def getWaveletsModes():
    return pywt.Modes.modes


def filterWaveletsFamilies(families):
    DWT_Families = list(filter(lambda w: w in DWT_SET, families))
    # print('Test is here: ', DWT_Families)
    return DWT_Families


# Multilevel  decomposition DWT
def dwt(data, wavelet, mode, level):
    coeffs = pywt.wavedec(data, wavelet, mode, level)
    # cA2, cD2, cD1 = co_effs
    return coeffs


# Multilevel recomposition DWT
def iDwt(coeffs, wavelet, mode):
    data = pywt.waverec(coeffs, wavelet, mode)
    return data


# Get DCT of data
def runDct(data):
    dctData = dct(data, type=3, norm="ortho")
    # print(dctData)
    return dctData


# Get inverse of DCT of data
def runIDct(data):
    i_dctData = idct(data, type=3, norm="ortho")
    return i_dctData


# Get FFT of data
def runFft(tuple_audio):
    data_fft = fft(tuple_audio[AUDIO_DATA])
    fft_abs = abs(data_fft)
    ttl = list(tuple_audio[AUDIO_DATA].shape)  # to extract tuple's values as int first it converts into list
    shape = ttl.pop()  # and then it is popped the single element of list
    freq = fftfreq(shape, 1. / tuple_audio[SAMPLERATE])
    t = (fft_abs, freq, data_fft)
    return t


# Get the inverse of FFT
def iFft(data):
    return ifft(data)


def indexFrequency(freq_fft, samplerate, frequency):
    return int((frequency / samplerate) * freq_fft.size)


'''
TESTING
'''
'''
if __name__ == "__main__":
    # read_wav_file()
    tupleAudio = read_wav_file("./audioTest/enchanted/enchanted.wav")
    print_metadata(tupleAudio)
    print("Is the audio mono? ", is_mono(tupleAudio[AUDIO_DATA]))  # false

    save_wav_file(tupleAudio[AUDIO_PATH], tupleAudio[SAMPLERATE], tupleAudio[AUDIO_DATA], "original")
    tupleAudio = join_audio_channels(tupleAudio[AUDIO_PATH])
    print_metadata(tupleAudio)
    # print(tupleAudio[AUDIO_DATA][0])
    print("Is the audio mono? ", is_mono(tupleAudio[AUDIO_DATA]))  # true

    FRAMES = audio_to_frame(tupleAudio[AUDIO_DATA], length=1000)
    print("Number of frames:", FRAMES.shape)  # 303 ca
    # test = frame_to_audio(FRAMES)
    # print(test[0])
    # print(test)

    waveform(tupleAudio)
    waveletsFamilies = get_wavelets_families()
    DWTFamilies = filter_wavelets_families(waveletsFamilies)
    print("DWT Families: ", DWTFamilies)
    print("len DWT Families = ", len(DWTFamilies))

    waveletsModes = get_wavelets_modes()
    COEFFS = dwt(tupleAudio[AUDIO_DATA], DWTFamilies[DWTFamilies.index("haar")],
                 waveletsModes[waveletsModes.index("symmetric")], WAVELETS_LEVEL)
    print("wavelets coeffs: ", COEFFS)

    cA2, cD2, cD1 = COEFFS
    # print("cA2: ", cA2, "\ncD2: ", cD2, "\ncD1: ", cD1)
    # cA2 = abs(cA2)
    # cD2 = abs(cD2)
    # scD1 = abs(cD1)
    COEFFS = cA2, cD2, cD1
    DATA = i_dwt(COEFFS, waveletsFamilies[0], waveletsModes[0])
    print("iDWT data: ", DATA)

    DATA = normalize_for_wav(DATA)
    print("iDWT == data audio? ", DATA == tupleAudio[AUDIO_DATA])

    save_wav_file(tupleAudio[AUDIO_PATH], tupleAudio[SAMPLERATE], DATA, "dwt")
    dct_coeff = run_dct(cA2)
    print("DCT Coeff: ", dct_coeff)

    i_dct_coeff = run_i_dct(dct_coeff)
    # print("iDCT Coeff: ", i_dct_coeff)
    print("cA2 == i_dct_Coeff? ", cA2 == i_dct_coeff)

    COEFFS = i_dct_coeff, cD2, cD1
    DATA = i_dwt(COEFFS, waveletsFamilies[0], waveletsModes[0])
    DATA = normalize_for_wav(DATA)
    print("iDWT + iDCT == data audio? ", DATA == tupleAudio[AUDIO_DATA])

    save_wav_file(tupleAudio[AUDIO_PATH], tupleAudio[SAMPLERATE], DATA, "dwt-dct")
    FFT_tuple = run_fft(tupleAudio)
    DATA = normalize_for_wav(i_fft(FFT_tuple[2]))
    save_wav_file(tupleAudio[AUDIO_PATH], tupleAudio[SAMPLERATE], DATA, "fft")
'''
