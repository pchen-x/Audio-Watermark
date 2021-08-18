from scipy.io import wavfile
import numpy as np




def crop_audio(name,start,end):
    audio = wavfile.read('./audio/' + name + '.wav')
    samplerate,array = audio
    start *= samplerate
    end *= samplerate
    wavfile.write('./audio/'+name+'Cropped.wav',samplerate,array[start:end])

def mix_audio(name_1,start_1,end_1,name_2,start_2,end_2):
    audio_1 = wavfile.read('./audio/' + name_1 + '.wav')
    samplerate_1, array_1 = audio_1
    start_1 *= samplerate_1
    end_1 *= samplerate_1

    audio_2 = wavfile.read('./audio/' + name_2 + '.wav')
    samplerate_2, array_2 = audio_2
    start_2 *= samplerate_2
    end_2 *= samplerate_2

    samplerate = max(samplerate_2,samplerate_1)
    mix = np.concatenate([array_1[start_1:end_1], array_2[start_2:end_2]])
    wavfile.write('./audio/' + name_1 + '&' + name_2 + 'Mixed.wav', samplerate, mix)

crop_audio('piano', 0, 3)
mix_audio('piano', 0, 3,'piano',1,4)