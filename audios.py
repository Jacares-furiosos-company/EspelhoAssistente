from gtts import gTTS
from subprocess import call

def criaAudio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/comando_invalido.mp3')

    call(['aplay', 'audios/comando_invalido.mp3'])

criaAudio('Comando Inválido')
