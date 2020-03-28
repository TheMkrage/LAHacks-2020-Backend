from flask import Flask
from flask import request
import base64
import subprocess

from os import environ, path, system

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pronouncing

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
def handle_form():
    word = request.json['word']
    expected = pronouncing.phones_for_word(word)

    data = request.data
    decoded = base64.b64decode(request.json['base'])
    with open('test.m4a', 'w') as media_write:
        media_write.write(decoded)

    phonemes = phonemes_for_audio()
    score = score_for_pronunciation(expected, phonemes)
    return 'response'


def score_for_pronunciation(expected, actual):
    def filtering(seg):
        letters = ['SIL', '+SPN+']
        if (seg not in letters):
            return True
        else:
            return False
    expected_string = " ".join(expected).replace("1", "").replace("0", "").replace("2", "")
    actual = filter(filtering, actual)
    actual_string = " ".join(actual)

    expected_vowels, expected_cons = get_vowels_and_cons(expected[0].split(" "))
    actual_vowels, actual_cons = get_vowels_and_cons(actual)

    v_c_score = abs(expected_vowels-actual_vowels) + abs(expected_cons-actual_cons)


    print(expected_string)
    print(actual_string)

    print(v_c_score)
    print(levenshtein_distance(expected_string, actual_string))


def get_vowels_and_cons(phonemes):
    expected_vowels = 0
    expected_cons = 0
    is_last_vowel = False
    print(phonemes)
    for phoneme in phonemes:
        print(phoneme)
        print(phoneme[0])
        if phoneme[0] in ['A', 'E', 'I', 'O', 'U']:
            expected_vowels += 1
            is_last_vowel = True
        else:
            if (is_last_vowel):
                expected_cons += 1
            is_last_vowel = False
    return expected_vowels, expected_cons

def phonemes_for_audio():
    # system()
    subprocess.call(["ffmpeg", "-y", "-i", "test.m4a", "-ar", "16000", "-ac", "1", "using.wav"])
    MODELDIR = "model"
    DATADIR = ""

    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
    config.set_string('-allphone', path.join(MODELDIR, 'en-us/en-us-phone.lm.dmp'))
    config.set_float('-lw', 2.0)
    config.set_float('-beam', 1e-10)
    config.set_float('-pbeam', 1e-10)

    # Decode streaming data.
    decoder = Decoder(config)

    decoder.start_utt()
    stream = open(path.join(DATADIR, 'using.wav'), 'rb')
    while True:
      buf = stream.read(1024)
      if buf:
        decoder.process_raw(buf, False, False)
      else:
        break
    decoder.end_utt()

    hypothesis = decoder.hyp()
    print ('Phonemes: ', [seg.word for seg in decoder.seg()])
    return [seg.word for seg in decoder.seg()]

def levenshtein_distance(string1, string2):
    n = len(string1)
    m = len(string2)
    d = [[0 for x in range(n + 1)] for y in range(m + 1)]

    for i in range(1, m + 1):
        d[i][0] = i

    for j in range(1, n + 1):
        d[0][j] = j

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if string1[j - 1] is string2[i - 1]:
                delta = 0
            else:
                delta = 1

            d[i][j] = min(d[i - 1][j] + 1,
                          d[i][j - 1] + 1,
                          d[i - 1][j - 1] + delta)

    return d[m][n]
