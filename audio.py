from gtts import gTTS
from playsound import  playsound

def criaAudio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/alexa.mp3')

    playsound('audios/alexa.mp3')

criaAudio('Não fale alexa, é espelho espelho meu')