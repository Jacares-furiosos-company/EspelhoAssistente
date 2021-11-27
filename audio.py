from gtts import gTTS
from playsound import  playsound

def criaAudio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/coordenadora.mp3')

    playsound('audios/coordenadora.mp3')

criaAudio('É a Zirlene, além de maravilhosa, ela da apoio e nós incentiva a fazer o nosso melhor, Por isso ela é a melhor coordenadora')