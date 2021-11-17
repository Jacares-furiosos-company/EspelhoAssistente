from gtts import gTTS
import speech_recognition as sr
from subprocess import call     # MAC / LINUX
from playsound import playsound
import time
from requests import get
from bs4 import BeautifulSoup
import webbrowser as browser
from paho.mqtt import  publish

##### CONFIGURAÇÕES #####
hotword = 'espelho'

with open('mirror-3663d-7396063fa192.json') as credenciais_google:
    credenciais_google = credenciais_google.read()


##### FUNÇÕES PRINCIPAIS #####

def responde(arquivo):
    #all(['afplay', 'audios/' + arquivo + '.mp3'])
    playsound('audios/' + arquivo + '.mp3')

def cria_audio(mensagem):
    tts = gTTS(mensagem, lang='pt-br')
    tts.save('audios/mensagem.mp3')
    print('Espelho: ', mensagem)
    call(['afplay', 'audios/mensagem.mp3']) # OSX
    #playsound('audios/mensagem.mp3')


def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()
    elif 'toca' in trigger:
        playlists('mais tocadas')


    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem)
        print('C. INVÁLIDO', mensagem)
        responde('comando_invalido')


##### FUNÇÕES COMANDOS #####

def ultimas_noticias():
    site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:2]:
        mensagem = item.title.text
        cria_audio(mensagem)

def playlists(album):
    if album == 'mais tocadas':
        browser.open('https://www.youtube.com/watch?v=TNIbXs_iNq8&list=PL2Q4-ZPcmbjAWEKoIqjIbGQgxPRsmlkUd')


def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        trigger = recognizer.recognize_google(audio, language='pt-br')
        if hotword in trigger:
            responde('feedback')
            executa_comandos(trigger)
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio, language='pt-br'))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)

stop_listening = r.listen_in_background(m, callback)

for _ in range(50): time.sleep(0.1)


while True: time.sleep(0.1)





