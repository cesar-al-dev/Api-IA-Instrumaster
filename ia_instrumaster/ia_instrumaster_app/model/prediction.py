import os
from matplotlib import pyplot as plt
import tensorflow as tf 
import numpy as np
import tensorflow_io as tfio

data_dir = 'assets'
def load_wav_chords(filename):
    file_contents = tf.io.read_file(filename)
    wav, sample_rate = tf.audio.decode_wav(file_contents, desired_channels=1)
    wav = tf.squeeze(wav, axis=-1)
    sample_rate = tf.cast(sample_rate, dtype=tf.int64)
    wav = tfio.audio.resample(wav, rate_in=sample_rate, rate_out=16000)
    return wav
def preprocess(file_path):
    
    wav = load_wav_chords(file_path)
    wav = wav[:32000]
    zero_padding = tf.zeros([32000]-tf.shape(wav),dtype=tf.float32)
    wav = tf.concat([zero_padding, wav],0)
    spectogram = tf.signal.stft(wav, frame_length=200, frame_step=32)
    spectogram = tf.abs(spectogram)
    spectogram = tf.expand_dims(spectogram, axis=2)
    return spectogram
def HacerPrediccion(file_path):
    instrumentos = ['Am', 'C', 'Dm', 'Em', 'F', 'G']
    samplep = preprocess(file_path)
    samplep = np.expand_dims(samplep, axis=0)
    modeloCNN2=tf.keras.models.load_model('ia_instrumaster_app/model/modelochords.h5')
    prediction = modeloCNN2.predict(samplep)
    predicted_label = np.argmax(prediction, axis=1)
    instrumento = instrumentos[predicted_label[0]]
    print("Predijo que es:", instrumento)
    return instrumento