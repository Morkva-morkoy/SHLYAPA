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

opts = {
    'names': ('шляпа', 'шляпы', 'шляпу'),
    'tbr': ('сколько', 'какое'),
    'cmds': {
        'cdate': ('сегодня число', 'число'),
        'ctime': ('сейчас времени', 'сейчас время', 'время', 'времени'),
        'web_search': ('найди', 'найти'),
        'sublime': ('запусти', 'открой'),
        'doll_course': ('курс доллара', 'курс'),
        'eur_course': ('курс евро', 'dsad'),
        'v-bucks': ('курс'),
        'pesnya': ('подрубай', 'adadadsad'),
        'corona': ('случаев коронавируса'),
        'send': ('отправь', 'dsadasdasdsa'),
        'note': ('напомни мне', 'dasdsadsa')
    }
}

names = {'dasd': 879796568, 'мамe': 2139749, 'роме': 617562550, 'мне': 370300823, 'духи': 310799106, 'витя': 429372253,
         'вове': 97233590}

list_months = ['bruh', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
               'ноябрь', 'декабрь']
r = sr.Recognizer()
m = sr.Microphone(device_index=0)

with open('vk_token.txt') as file:
    token = file.read()

with m as source:
    r.adjust_for_ambient_noise(source)


def speak(what):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
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


DOLLAR_RUB = 'https://www.cbr.ru/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
full_page = requests.get(DOLLAR_RUB, headers=headers)
soup = BeautifulSoup(full_page.content, 'html.parser')
convert = soup.find_all('div', {'class': 'col-md-2 col-xs-9 _right mono-num'})
with open('notes.txt', 'r') as file:
    try:
        text_for_print = file.read()
        text = text_for_print.split()
        lent = len(text)
        time_for_note = text[lent - 1].replace(':', ' ').split()
        hour_note = int(time_for_note[0])
        minute_note = int(time_for_note[1])
        hour_now = datetime.datetime.now().hour
        minute_now = datetime.datetime.now().minute

        minute_now += hour_now * 60
        minute_note += hour_note * 60

        time_diff = minute_note - minute_now

        if time_diff >= 0:
            print(f'У вас осталось {time_diff // 60} часов {time_diff % 60} минут до того, чтобы {text_for_print}')
        else:
            print('Вы прошляпили свой план')
        if hour_note > hour_now:
            if minute_now > minute_note:
                f = (hour_note - hour_now) * 60
                v = f + minute_note - minute_now
                print('У вас осталось ' + str(v // 60) + ' часов ' + str(
                    v % 60) + ' минут' + ' до того чтобы ' + text_for_print)
            else:
                print('У вас осталось ' + str(hour_note - hour_now) + ' часов ' + str(
                    minute_note - minute_now) + ' минут' + ' до того чтобы ' + text_for_print)
        else:
            print('Вы прошляпили свой план')
    except IndexError:
        pass
    except ValueError:
        pass


def sent(user_id, messagee):
    vk = vk_api.VkApi(token=token).get_api()
    vk.messages.send(
        user_id=user_id,
        message=messagee,
        random_id=0
    )


def execute_cmd(cmd, voice):
    now = datetime.datetime.now()
    if cmd == 'cdate':
        speak(str('Сейчас' + str(now.day) + ',' + list_months[now.month]))
    elif cmd == 'ctime':
        speak('Сейчас' + str(now.hour) + ':' + str(now.minute))
    elif cmd == 'web_search':
        webbrowser.open_new_tab(
            'https://www.google.com/search?q={}'.format('+'.join(str(voice).replace('шляпа найди', '').split())))
    elif cmd == 'sublime':
        voice_for_apps = voice.split()
        voice_for_apps = voice_for_apps[2:]
        voice_for_apps = ' '.join(voice_for_apps)
        os.startfile(('C:\\Users\\SHLYAPA\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\{}').format(
            voice_for_apps))
    elif cmd == 'doll_course':
        speak(convert[0].text + ' рубля')
    elif cmd == 'eur_course':
        speak(convert[2].text + ' рубля')
    elif cmd == 'send':
        try:
            voice_for_vk = voice.split()
            voice_for_id = voice_for_vk[2]
            voice_for_id = names[voice_for_id]
            voice_for_message = voice_for_vk[3:]
            voice_for_message = ' '.join(voice_for_message)
            sent(voice_for_id, voice_for_message)
        except Exception:
            pass
    elif cmd == 'pesnya':
        webbrowser.open_new_tab('https://www.youtube.com/watch?v=KReAKK9SUbQ')
    elif cmd == 'note':
        voice = voice.split()
        lent = len(voice)
        voice_for_note = voice[3:]
        voice_for_note = ' '.join(voice_for_note)
        voice_for_time = voice[lent - 1]
        with open('notes.txt', 'w') as file:
            file.writelines(voice_for_note)


print('bruh')
stop_listening = r.listen_in_background(m, callback)
while True:
    time.sleep(0.1)
