import functions
import os
import speech_recognition as sr
import datetime
import pyttsx3
import time
from fuzzywuzzy import fuzz
import webbrowser
import pathlib
import requests
from bs4 import BeautifulSoup
import vk_api
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

opts = {
    'names': ('шляпа', 'шляпы', 'шляпу'),
    'tbr': ('сколько', 'какое'),
    'cmds': {
        'ctime': ('сейчас времени', 'сейчас время', 'время', 'времени'),
        'cdate': ('сегодня число', 'число'),
        'web_search': ('найди', 'найти'),
        'course_usd': ('курс доллара', 'доллар в рублях'),
        'course_eur': ('курс евро', 'евро в рублях'),
        'apps': ('открой', 'asdasdasd'),
        'send': ('отправь', 'dsadasdasdsa'),
        'note': ('напомни', 'напомни мне'),
        'note1': ('мои планы', 'что у меня запланировано'),
        'off': ('dasdasd', 'выключи компьютер'),
        'temp': ('dasdahs', 'какая сейчас температура'),
        'sky': ('dasdas', 'какие сейчас осадки'),
        'wind_speed': ('dasdasd', 'какая сейчас ветeр'),
        'if_rain': ('dasdsad', 'сейчас есть дождь'),
        'humidity': ('dasdja', 'какое сейчас давление')
    }
}
vk_names = {'dasd': 879796568, 'мамe': 2139749, 'роме': 617562550, 'мне': 370300823, 'духи': 310799106,
            'витя': 429372253, 'вове': 97233590, 'королю': 332716512}
list_months = ['bruh', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
               'ноябрь', 'декабрь']

r = sr.Recognizer()
m = sr.Microphone(device_index=0)

with m as source:
    r.adjust_for_ambient_noise(source)


def speak(what):
    engine = pyttsx3.init()
    engine.say(what)
    engine.runAndWait()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language='ru-RU').lower()
        print('[log] Распознано: ' + voice)
        if voice.startswith(opts['names']):
            cmd = voice
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'], voice)

    except sr.UnknownValueError:
        print('[log] Голос не распознан')
    except sr.RequestError:
        print('[log] Bruh')


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():
        for i in v:
            vrt = fuzz.ratio(cmd, i)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


with open('notes.txt', 'r') as file:
    text_for_print = file.read()

note_time = functions.note()

time_now = '{}:{}'.format(datetime.datetime.now().hour, datetime.datetime.now().minute)

dollar_eur = 'https://www.cbr.ru/'
weather = 'https://www.gismeteo.ru/weather-sankt-peterburg-4079/now/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.66 Safari/537.36'}

course_page = requests.get(dollar_eur, headers=headers)
soup = BeautifulSoup(course_page.content, 'html.parser')
convert = soup.find_all('div', {'class': 'col-md-2 col-xs-9 _right mono-num'})
weather_for = soup.find_all('div', {'class': 'date xs fadeIn data-tz'})
pass


def execute_cmd(cmd, voice):
    now = datetime.datetime.now()
    if cmd == 'cdate':
        speak(str('Сейчас' + str(now.day) + ',' + list_months[now.month]))
    if cmd == 'ctime':
        speak('Сейчас' + str(now.hour) + ':' + str(now.minute))
    if cmd == 'web_search':
        webbrowser.open_new_tab('https://www.google.com/search?q={}'.format('+'.join(voice.split()[2:])))
    if cmd == 'course_usd':
        speak('{} рублей'.format(convert[0].text))
    if cmd == 'course_eur':
        speak('{} рублей'.format(convert[2].text))
    if cmd == 'apps':
        try:
            voice_for_apps = voice.split()
            voice_for_apps = voice_for_apps[2:]
            voice_for_apps = ' '.join(voice_for_apps)
            os.startfile('C:\\Users\\SHLYAPA\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\{}'.format(
                voice_for_apps))
        except Exception:
            pass
    if cmd == 'send':
        try:
            voice_for_vk = voice.split()
            voice_for_id = voice_for_vk[2]
            voice_for_id = vk_names[voice_for_id]
            voice_for_message = voice_for_vk[3:]
            voice_for_message = ' '.join(voice_for_message)
            functions.sent(voice_for_id, voice_for_message)
        except Exception:
            pass
    if cmd == 'note':
        voice = voice.split()
        voice_for_note = voice[3:]
        voice_for_note = ' '.join(voice_for_note)
        with open('notes.txt', 'w') as file:
            file.writelines(voice_for_note)
    if cmd == 'note1':
        functions.note()
    if cmd == 'off':
        os.system("shutdown /p")
    if cmd == 'temp':
        print(functions.get_weather()['temp'])
    if cmd == 'sky':
        print('w.detailed_status')
    if cmd == 'wind':
        print(functions.get_weather1().wind())
    if cmd == 'if_rain':
        print(functions.get_weather1().rain)
    if cmd == 'humidity':
        print(functions.get_weather1().humidity)


stop_listening = r.listen_in_background(m, callback)

while True:
    time.sleep(0.1)
    time_now = '{}:{}'.format(datetime.datetime.now().hour, datetime.datetime.now().minute)
    if time_now == note_time:
        print('Вам пора {}'.format(' '.join(text_for_print.split()[0:-2])))
        speak('Вам пора {}'.format(' '.join(text_for_print.split()[0:-2])))
        open('notes.txt', 'w').close()
        time.sleep(60)
