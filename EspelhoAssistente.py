from datetime import datetime
from googletrans import Translator
import os
import random
import randfacts
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


##### CONFIGURAÇÕES #####
hotword = 'espelho meu'


##### FUNÇÕES PRINCIPAIS #####

def existe(terms, trigger):
    for item in terms:
        if item in trigger:
            return True

def responde(arquivo):
    try:
        playsound('audios/'+ arquivo +'.mp3')
    except:
        responde('erro')

def cria_audio(audio):
    try:
        if audio != '':
            tts = gTTS(audio, lang='pt-br')
            r = random.randint(1, 20000000)
            audio_file = 'audios/' + str(r) + '.mp3'
            tts.save(audio_file)
            playsound(audio_file)
            print(f"Espelho: {audio}")
            os.remove(audio_file)
        else:
            pass
    except:
        pass

def executa_comandos(trigger):
    if existe(['notícias', 'últimas notícas'], trigger):
        ultimas_noticias()

    elif existe(['pesquisa'], trigger):
        pesquisar(trigger)

    elif existe(['maravilhosa do que'], trigger):
        responde('maravilhosa')

    elif existe(['alguém mais princesa'], trigger):
        responde('unicaprincesa')

    elif existe(['horas'], trigger):
        horaAtual()

    elif existe(['fato', 'curiosidade', 'alguma coisa'], trigger):
        fatoAleatorio()

    elif existe(['belo', 'bela'], trigger):
        responde('maisBela')

    elif 'liga luz' in trigger:
        publica_mqtt('office/iluminacao/status', '1')

    elif 'desativa luz' in trigger:
        publica_mqtt('office/iluminacao/status', '0')

    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem)
        print('C. INVÁLIDO', mensagem)
        responde('comando_invalido')


##### FUNÇÕES COMANDOS #####
def publica_mqtt(topic, payload):
    publish.single(topic, payload=payload, qos=1, retain=True,
                   hostname='broker.mqttdashboard.com', port=12892,
                   client_id='espelho',
                   auth={'username': 'xxxxxxxx', 'password': 'xxxxxxxx'})
    if payload == '1':
        responde('luzLigada')
    elif payload == '0':
        responde('luzDesligada')

def horaAtual():
    horaatual = datetime.now().strftime('%H: %M')
    cria_audio('A hora atual é ' + horaatual)

def fatoAleatorio():
    fato = randfacts.get_fact()
    tradutor = Translator()
    traducao = tradutor.translate(fato, dest='pt', src='en')
    print(traducao.text)
    cria_audio(traducao.text)

def ultimas_noticias():
    try:
        site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
        noticias = BeautifulSoup(site.text, 'html.parser')
        for item in noticias.findAll('item')[:2]:
            mensagem = item.title.text
            cria_audio(mensagem)
    except urllib3.exceptions.NewConnectionError:
        responde('erro_conexao')



def pesquisar(trigger):
    pesquisa = ''
    try:
        if 'pesquisa' in trigger:
            pesquisa = trigger.replace('espelho espelho meu pesquisa ', '')
        wikipedia.set_lang("pt")
        info = wikipedia.summary(pesquisa, 1)
        print(info)
        cria_audio(info)
    except:
        cria_audio('Não encontrei sua pesquisa')
        print('Problema na pesquisa')



responde('bem_vindo')


##### MICROFONE #####
def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google(audio, language='pt-br')
                trigger = trigger.lower()
                if hotword in trigger:
                    print('COMANDO: ', trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break
                elif 'ok google' in trigger:
                    responde('okGoogle')
                elif 'alexa' in trigger:
                    responde('alexa')

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger

def main():
    while True:
        monitora_audio()


main()



def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        trigger = recognizer.recognize_google(audio, language='pt-br')
        trigger = trigger.lower()
        if hotword in trigger:
            responde('feedback')
            executa_comandos(trigger)
        print("Google acha que você falou" + recognizer.recognize_google(audio, language='pt-br'))
    except sr.UnknownValueError:
        print("não entendeu o que você disse")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


#r = sr.Recognizer()
#m = sr.Microphone()
#with m as source:
   # r.adjust_for_ambient_noise(source)

#stop_listening = r.listen_in_background(m, callback)

#for _ in range(50): time.sleep(0.1)


#while True: time.sleep(0)

