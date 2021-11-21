import os
import random

import urllib3.exceptions
from gtts import gTTS
import speech_recognition as sr
from subprocess import call     # MAC / LINUX
from playsound import playsound
import time
from requests import get
from bs4 import BeautifulSoup
import webbrowser as browser
import wikipedia
from paho.mqtt import publish

with open('mirror-3663d-2f6e243aac6e.json') as credenciais_google:
    credenciais_google = credenciais_google.read()

##### CONFIGURAÇÕES #####
hotword = 'espelho'


##### FUNÇÕES PRINCIPAIS #####

def existe(terms, trigger):
    for item in terms:
        if item in trigger:
            return True

def responde(arquivo):
    try:
        call(['afplay', 'audios/' + arquivo + '.mp3'])
        #playsound('audios/'+ arquivo +'.mp3')
    except:
        responde('erro')

def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    r = random.randint(1, 20000000)
    audio_file = 'audios/' + str(r) + '.mp3'
    tts.save(audio_file)
    call(['aplay', 'audios/'+ str(r) +'.mp3'])
    #playsound(audio_file)
    print(f"Espelho: {audio}")
    os.remove(audio_file)

def executa_comandos(trigger):
    if existe(['notícias', 'últimas notícas'], trigger):
        ultimas_noticias()

    elif existe(['toca', 'youtub', 'youtube', 'música'], trigger):
        playlists('mais tocadas')

    elif existe(['pesquisa', 'quem é'], trigger):
        pesquisar(trigger)

    elif existe(['o que você faz'], trigger):
        responde('oqpodefazer')

    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem)
        print('C. INVÁLIDO', mensagem)
        responde('comando_invalido')


##### FUNÇÕES COMANDOS #####

def ultimas_noticias():
    try:
        site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
        noticias = BeautifulSoup(site.text, 'html.parser')
        for item in noticias.findAll('item')[:2]:
            mensagem = item.title.text
            cria_audio(mensagem)
    except urllib3.exceptions.NewConnectionError:
        responde('erro_conexao')
    except :
        responde('nao_entendi')



def playlists(album):
    if album == 'mais tocadas':
        browser.open('https://www.youtube.com/watch?v=TNIbXs_iNq8&list=PL2Q4-ZPcmbjAWEKoIqjIbGQgxPRsmlkUd')

def pesquisar(trigger):
    try:
        pessoa = ''
        if 'pesquisa' in trigger:
            pessoa = trigger.replace('espelho pesquisa ', '')
        elif 'quem é ' in trigger:
            pessoa = trigger.replace('espelho quem é ', '')
        wikipedia.set_lang("pt")
        info = wikipedia.summary(pessoa, 1)
        print(info)
        cria_audio(info)
    except:
        cria_audio('Não encontrei sua pesquisa')
        print('Problema na pesquisa')

responde('bem_vindo')
##### MICROFONE #####
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:

        #trigger = r.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-br')
        trigger = recognizer.recognize_google(audio, language='pt-br')
        if hotword in trigger:
            responde('feedback')
            executa_comandos(trigger)
        elif hotword not in trigger:
            responde('naoentendi')
        #print(r.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-br'))
        print("Google acha que você falou" + recognizer.recognize_google(audio, language='pt-br'))
    except sr.UnknownValueError:
        responde('naoentendi')
        print("não entendeu o que você disse")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)

stop_listening = r.listen_in_background(m, callback)

for _ in range(50): time.sleep(0.1)


while True: time.sleep(0.1)

