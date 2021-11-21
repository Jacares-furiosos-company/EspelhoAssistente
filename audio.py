from gtts import gTTS
from subprocess import call

def criaAudio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/naoentendi.mp3')

    call(['aplay', 'audios/naoentendi.mp3'])

criaAudio('não entendi o que disse, fale novamente')