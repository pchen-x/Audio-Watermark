# import ffmpeg
import librosa
import soundfile as sf

name = 'embedded党章'
filename = './audio/人声/' + name + '.wav'
newFilename = './audio/' + name + 'ReSample.wav'
y, sr = librosa.load(filename, sr=48000)
y_8k = librosa.resample(y,sr,30000)
sf.write(newFilename,y_8k, 48000, 'PCM_24')

# librosa.output.write_wav(newFilename, y_8k, 8000)

# ffmpeg.input(filename).output(newFilename, ar=16000).run()