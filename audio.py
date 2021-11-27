from gtts import gTTS
from playsound import  playsound

def criaAudio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/chamon.mp3')

    playsound('audios/chamon.mp3')

criaAudio('João Paulo Chamon, 50 anos só de profissão, nascido e criado na UCL, está sempre aparecendo nos jornais locais, o cara é fera')