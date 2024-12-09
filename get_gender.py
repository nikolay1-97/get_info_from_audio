"""Модуль определения гендера спикера"""
from os import path, getcwd, listdir
from pickle import load

import numpy as np
from scipy.io.wavfile import read
import python_speech_features as mfcc
from sklearn import preprocessing
import warnings


warnings.filterwarnings("ignore")

# функция извлекает характеристики из аудио
def get_MFCC(sr,audio):
    features = mfcc.mfcc(audio,sr, 0.025, 0.01, 13,appendEnergy = False)
    feat     = np.asarray(())
    for i in range(features.shape[0]):
        temp = features[i,:]
        if np.isnan(np.min(temp)):
            continue
        else:
            if feat.size == 0:
                feat = temp
            else:
                feat = np.vstack((feat, temp))
    features = feat
    features = preprocessing.scale(features)
    return features

# функция определяет гендер спикера
def get_gender(
        path_to_audio_file: str,
        modelpath: str = getcwd() + '\\trained_models\\',
) -> str:
    modelpath = modelpath.replace('\\', '/')
    gmm_files = [path.join(modelpath,fname) for fname in
              listdir(modelpath) if fname.endswith('.gmm')]
    models = [load(open(fname,'rb')) for fname in gmm_files]
    genders = [fname.split("/")[-1].split(".gmm")[0] for fname
              in gmm_files]
    sr, audio  = read(path_to_audio_file)
    features = get_MFCC(sr, audio)
    scores = None
    log_likelihood = np.zeros(len(models))

    for i in range(len(models)):
        gmm = models[i]
        scores = np.array(gmm.score(features))
        log_likelihood[i] = scores.sum()
    winner = np.argmax(log_likelihood)

    return genders[winner]
 