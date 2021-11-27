from gtts import gTTS
from playsound import  playsound

def criaAudio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/espelhomeu.mp3')

    playsound('audios/espelhomeu.mp3')

criaAudio('tô aqui, pode falar')