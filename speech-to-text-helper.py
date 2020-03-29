import wave
import contextlib

def audioLength(filename):
    """ Takes in a .wav file in the format 'filename.wav' and returns the length of
    the audio file in seconds """
    with contextlib.closing(wave.open(filename,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration

def textRead(filename):
    """ Takes in a .txt file (speech-to-text) in the format 'filename.txt' and 
    returns the text as an array of split up words"""
    f = open(filename, "r")
    text = f.read()
    f.close()
    text = text.split()
    return text

def returnAttribuates(audioFile, txtFile):
    """ Takes in a .wav file and a .txt file and returns the average words per minute (wpm)
    of the audio file (considering that the .txt file is the corresponding speech to text).
    Also returns a list of "hot words" that the speaker said too often (currently set at 
    more than 3% of words said) """

    duration = audioLength(audioFile)
    text = textRead(txtFile)

    wpm = len(text)*60/duration
    hotwords = []
    hotwordTrigger = .1 #If a person says a word more than 10% of the time, that word gets triggered
    for word in text:
        if text.count(word) >= len(text)*hotwordTrigger:
            hotwords.append(word)
    
    return wpm, hotwords
