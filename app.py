from flask import Flask
from flask import request
import base64

from os import environ, path, system

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
def handle_form():
    data = request.data

    decoded = base64.b64decode(request.json['base'])
    media_write = open('test.m4a', 'w')
    media_write.write(decoded)

    phonemes = phonemes_for_audio()
    print(phonemes)
    return 'response'


def phonemes_for_audio():
    system("ffmpeg -i test.m4a -ar 16000 -ac 1 using.wav")

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
