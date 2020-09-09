# Speech to speech language translator 
# Daniel Chalmers | 08/09/20

from scipy.io.wavfile import write
from googletrans import Translator
from codes import ISO6391
from gtts import gTTS
import speech_recognition as SR
import sounddevice as SD
import wavio
import os

translator = Translator()

sampleRate = 44100 # 44.1KHz (Sample at same frequency as we speak)
duration = 7 # Duration of recording in seconds

print ('What language would you like your input to be translated into?')
validLang = False
while validLang == False:
    lang = input('> ')
    try:
        dest = ISO6391[lang.lower()]
    except KeyError:
        print ('Sorry, this language is currently not supported. Please enter another')
    else:
        try:
            translation = translator.translate('test.wav', dest=dest, src='en')
        except ValueError:
            print ('Sorry, this language is currently not supported. Please enter another')
        else:
            validLang = True

recording = SD.rec(int(duration * sampleRate), samplerate=sampleRate, channels=2)
print ('Recording has started')
SD.wait()
print ('Recording has ended')
wavio.write('input.wav', recording, sampleRate ,sampwidth=2) # Save audio as PCM WAV file (NB: Must be PCM. Other .wav formats don't work for some stupid reason)

inputSpeechFile = 'input.wav'
recogniser = SR.Recognizer()
with SR.AudioFile(inputSpeechFile) as src:
    # Load audio
    audio_data = recogniser.record(src)
    input = recogniser.recognize_google(audio_data)
    print('Input: '+input)

src = ((translator.detect(input)).lang)
translation = translator.translate(input, dest=dest, src=src) # x=x is a bit shit. Change var name?
text = (translation.text)
output = (translation.pronunciation)
if text != output:
    print (text, '('+output+')')
else:
    print ('Output: '+output)

tts = gTTS(text=text, lang=dest)
tts.save('output.mp3')
os.system('output.mp3')



