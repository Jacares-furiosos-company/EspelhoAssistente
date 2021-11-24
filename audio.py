from gtts import gTTS
from playsound import  playsound

def criaAudio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/AssistenteErrado.mp3')

    playsound('audios/AssistenteErrado.mp3')

criaAudio('Tá usando o assistente errado, é espelho espelho meu')