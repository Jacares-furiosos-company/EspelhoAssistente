from gtts import gTTS
from playsound import  playsound

def criaAudio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/maravilhosa.mp3')

    playsound('audios/maravilhosa.mp3')

criaAudio('impossível ter uma rainha mais maravilhosa que você')