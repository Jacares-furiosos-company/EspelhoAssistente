from gtts import gTTS
import speech_recognition as sr
from subprocess import call     # MAC / LINUX
#from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
import webbrowser as browser
from paho.mqtt import  publish

##### CONFIGURAÇÕES #####
hotword = 'espelho'

with open('mirror-3663d-7396063fa192.json') as credenciais_google:
    credenciais_google = credenciais_google.read()


##### FUNÇÕES PRINCIPAIS #####

def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-BR')
                trigger = trigger.lower()
                if hotword in trigger:
                    print('COMANDO: ', trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger

def responde(arquivo):
    call(['afplay', 'audios/' + arquivo + '.mp3'])
    #playsound('audios/' + arquivo + '.mp3')

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

def main():
    while True:
        monitora_audio()

main()

#publica_mqtt('office/iluminacao/status', '1')



