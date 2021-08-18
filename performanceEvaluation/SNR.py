import wave
import numpy as np
import math


def get_soundfile(url):
    # 打开wav文件 ，open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据。
    filetmp = wave.open(url, "rb")

    # 读取格式信息
    # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采
    # 样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
    params = filetmp.getparams()

    nchannels, sampwidth, framerate, nframes = params[:4]
    # 读取波形数据
    # 读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）
    str_data = filetmp.readframes(nframes)
    filetmp.close()

    # 将波形数据转换成数组
    # 需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组
    tmp_data = np.frombuffer(str_data, dtype=np.short, count=-1, offset=0)
    # print(tmp_data)
    # np.fromstring(str_data,dtype = np.short)

    # 将wave_data数组改为2列，行数自动匹配。在修改shape的属性时，需使得数组的总长度不变。
    tmp_data.shape = -1, 2
    # print(tmp_data)
    # 转置数据
    tmp_data = tmp_data.T
    # print(tmp_data)
    return tmp_data
    # #通过取样点数和取样频率计算出每个取样的时间。
    # time=np.arange(0,nframes)/framerate
    # #print(params)
    # plt.figure(1)
    # plt.subplot(2,1,1)
    # #time 也是一个数组，与wave_data[0]或wave_data[1]配对形成系列点坐标
    # plt.plot(time,wave_data[0])
    # plt.subplot(2,1,2)
    # plt.plot(time,wave_data[1],c="r")
    # plt.xlabel("time")
    # plt.show()


def wav_snr(ref_wav, in_wav):  # 如果ref wav稍长，则用0填充in_wav
    if abs(in_wav.shape[0] - ref_wav.shape[0]) < 10:
        pad_width = ref_wav.shape[0] - in_wav.shape[0]
        in_wav = np.pad(in_wav, (0, pad_width), 'constant')
    else:
        print("错误：参考wav与输入wav的长度明显不同")
        return -1

    # 计算 SNR
    norm_diff = np.square(np.linalg.norm(in_wav - ref_wav))
    if norm_diff == 0:
        print("错误：参考wav与输入wav相同")
        return -1

    ref_norm = np.square(np.linalg.norm(ref_wav))
    snr = 10 * np.log10(ref_norm / norm_diff)
    return snr


if __name__ == "__main__":
    ref_data = get_soundfile("./testData/mono-CruelSummer-60s.wav")
    in_data = get_soundfile("./testData/New-CruelSummer-60s.wav")
    SNR = wav_snr(ref_data, in_data)
    print('SNR:', SNR)
