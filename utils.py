#!/usr/bin/env python3
"""
Utils file containing functions mapping text and audio to features.
"""
import spacy
import numpy as np
from typing import List
from xml.dom import minidom
from surfboard.sound import Waveform
from scipy.io.wavfile import read as wavread
nlp = spacy.load('en_core_web_sm')


def text_to_features(path: str) -> np.ndarray:
    """
    path: A path to the xml file since the conversations are represented in an xml file. 
    It can be from a local machine or stored on the cloud. 
    Uses spacy to extract word vectors for every word in the input
    text. Averages those word vectors.
    Args:
        text (str): A string input sentence or document.
    Returns:
        np.ndarray: The averaged word vectors for every word in the
            sentence.
    """
    doc = minidom.parse(path)
    words = doc.getElementsByTagName('w')
    #split_text: List[str] = text.split()
    text = [] #Store the words in a list for the text
    for word in words:
        text.append(word.firstChild.data)
    word_vectors: List[np.ndarray] = [nlp(word).vector for word in text] #get the representations of the words
    return np.mean(word_vectors, 0)

def audio_to_features(fName: str, sample_rate: int=44100):
    """
    fName: the file name/path of the audio file as a conversation. 
    Uses Surfboard to extract 13 averaged MFCCs over time.
    First load the waveform, then extract features.
    Args:
        fName(str): Name of the audio .wav file.
        sample_rate (int): The sample rate of the waveform.
    Returns:
        np.ndarray: The extracted audio features. 
    """
    _,X = wavread(fName) #Get the original sampling rate and the audio form as a vector of 1D data points.
    waveform: Waveform = Waveform(signal=X, sample_rate=sample_rate)
    #waveform: Waveform = Waveform(signal=audio, sample_rate=sample_rate)
    averaged_mfccs: np.ndarray = waveform.mfcc().mean(0)
    return averaged_mfccs


