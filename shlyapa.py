from functions import *
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
from covid import Covid
import getpass

opts = {
    "names": ("шляпа", "шляпы", "шляпу"),
    "tbr": ("сколько", "какое", "блин", "выключи"),
    "cmds": {
        "cdate": ("dakjds", "сегодня число"),
        "ctime": ("dasda", "сейчас времени"),
        "off": ("dadads", "компьютер"),
        "course_usd": ("курс доллара", "доллар в рублях"),
        "course_eur": ("курс евро", "евро в рублях"),
        "apps": ("открой", "запусти"),
        "send": ("отправь", "сообщение"),
        "note": ("напомни", "напомни мне"),
        "note1": ("мои планы", "планы"),
        "temp": ("температура", "сейчас температура"),
        "sky": ("осадки", "сейчас осадки"),
        "wind_speed": ("ветер", "скорость ветра"),
        "if_rain": ("дождь", "сейчас есть дождь"),
        "humidity": ("влажность", "сейчас влажность"),
        "corona": ("коронавирус", "случаев короновируса"),
        "student": ("ddsadas", "работа студентом в этом есть прикол"),
        "web_search": ("найди", "dasdasd"),
    },
}

vk_names = {
    "dasd": 879796568,
    "роме": 617562550,
    "мне": 350291456,
    "духи": 310799106,
    "витя": 429372253,
    "вове": 97233590,
    "арсению": 526584669,
}
list_months = [
    "bruh",
    "январь",
    "февраль",
    "март",
    "апрель",
    "май",
    "июнь",
    "июль",
    "август",
    "сентябрь",
    "октябрь",
    "ноябрь",
    "декабрь",
]
counties = {
    "россии": "Russia",
    "украине": "Ukraine",
    "америке": "US",
    "индии": "India",
    "бразилии": "Brazil",
    "франции": "France",
    "великобритании": "United Kingdom",
}

cities = {"санкт-петербурге": "Saint Petersburg, RU", "москве": "Moscow, RU"}
days = {
    "завтра": datetime.datetime.now().day + 1,
    "послезавтра": datetime.datetime.now().day + 2,
}

user_name = getpass.getuser()

r = sr.Recognizer()
m = sr.Microphone(device_index=0)

with m as source:
    r.adjust_for_ambient_noise(source)


def speak(what):
    engine = pyttsx3.init()
    engine.say(what)
    engine.runAndWait()


def recognize_cmd(cmd):
    RC = {"cmd": "", "percent": 0}
    for c, v in opts["cmds"].items():
        for i in v:
            vrt = fuzz.ratio(cmd, i)
            if vrt > RC["percent"]:
                RC["cmd"] = c
                RC["percent"] = vrt
    return RC


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)
        if voice.startswith(opts["names"]):
            cmd = voice
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd["cmd"], voice, counties, cities, days)

    except sr.UnknownValueError:
        print("[log] Голос не распознан")
    except sr.RequestError:
        print("[log] Bruh")


with open("notes.txt", "r") as file:
    text_for_print = file.read()

note_time = note()

time_now = "{}:{}".format(datetime.datetime.now().hour, datetime.datetime.now().minute)

dollar_eur = "https://www.cbr.ru/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.66 Safari/537.36"
}

course_page = requests.get(dollar_eur, headers=headers)
soup = BeautifulSoup(course_page.content, "html.parser")
convert = soup.find_all("div", {"class": "col-md-2 col-xs-9 _right mono-num"})


def execute_cmd(cmd, voice, countries, cities, days):
    now = datetime.datetime.now()

    if cmd == "cdate":
        speak(str("Сейчас" + str(now.day) + "," + list_months[now.month]))
    if cmd == "ctime":
        speak("Сейчас" + str(now.hour) + ":" + str(now.minute))
    if cmd == "course_usd":
        print("{} рублей".format(convert[0].text))
        speak("{} рублей".format(convert[0].text))
    if cmd == "course_eur":
        print("{} рублей".format(convert[2].text))
        speak("{} рублей".format(convert[2].text))
    if cmd == "apps":
        try:
            voice_for_apps = ' '.join(voice.split()[2:])
            USER_NAME = getpass.getuser()
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\{}\\{}".format(
                voice_for_apps, voice_for_apps))

        except FileNotFoundError:
            try:
                os.startfile(
                    "C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\{}".format(
                        USER_NAME, voice_for_apps
                    )

                )
            except FileNotFoundError:
                try:
                    os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\{}".format(
                        voice_for_apps))
                except FileNotFoundError:
                    try:
                        os.startfile(
                            "C:\\Users\\{}\\Desktop\\{}".format(USER_NAME, voice_for_apps)
                        )
                    except FileNotFoundError:
                        print("incorrect app")

    if cmd == "send":
        try:
            voice_for_vk = voice.split()
            voice_for_id = voice_for_vk[2]
            voice_for_id = vk_names[voice_for_id]
            voice_for_message = voice_for_vk[3:]
            voice_for_message = " ".join(voice_for_message)
            sent(voice_for_id, voice_for_message)
        except Exception:
            pass
    if cmd == "note":
        voice = voice.split()
        voice_for_note = voice[3:]
        voice_for_note = " ".join(voice_for_note)
        with open("notes.txt", "w") as file:
            file.writelines(voice_for_note)
    if cmd == "note1":
        note()
    if cmd == "off":
        check = str(input("Вы уверены что хотите завершить работу компьютера? "))
        if check == "да":
            os.system("shutdown /p")
        else:
            pass
    if cmd == "temp":
        try:
            print(get_weather(cities[voice.split()[-1]]).temperature("celsius")["temp"])
            speak(get_weather(cities[voice.split()[-1]]).temperature("celsius")["temp"])
        except KeyError:
            print("incorrect city")
    if cmd == "sky":
        try:
            print(get_weather(cities[voice.split()[-1]]).detailed_status)
            speak(get_weather(cities[voice.split()[-1]]).detailed_status)
        except KeyError:
            print("incorrect city")
    if cmd == "wind":
        try:
            print(get_weather(cities[voice.split()[-1]]).wind())
            speak(get_weather(cities[voice.split()[-1]]).wind())
        except KeyError:
            print("incorrect city")
    if cmd == "if_rain":
        try:
            print(get_weather(cities[voice.split()[-1]]).rain)
            speak(get_weather(cities[voice.split()[-1]]).rain)
        except KeyError:
            print("incorrect city")
    if cmd == "humidity":
        try:
            print(get_weather(cities[voice.split()[-1]]).humidity)
            speak(get_weather(cities[voice.split()[-1]]).humidity)
        except KeyError:
            print("incorrect city")
    if cmd == "corona":
        try:
            covid = Covid(source="worldometers")
            action = covid.get_status_by_country_name(countries[voice.split()[-1]])
            print(
                "В {} {} новых случаев за сегодня".format(
                    voice.split()[-1], action["new_cases"]
                )
            )
            speak(
                "В {} {} новых случаев за сегодня".format(
                    voice.split()[-1], action["new_cases"]
                )
            )
        except KeyError:
            pass
    if cmd == "student":
        for i in range(5):
            speak("for real")
            speak("ealealealealealealealealealealealealealbruh")

    if cmd == "web_search":
        print(
            "https://www.google.com/search?q={}".format(voice.split()[2:])
        )


stop_listening = r.listen_in_background(m, callback)

while True:
    time.sleep(0.1)
    time_now = (
            f"{datetime.datetime.now().hour}:"
            + list(f"0{datetime.datetime.now().minute}")[-2]
            + list(f"0{datetime.datetime.now().minute}")[-1]
    )
    try:
        day_note = day_note()
        if datetime.datetime.now().isoweekday() == day_note:
            time.sleep(60)
            open("notes.txt", "w").close()

    except TypeError:
        pass
    if datetime.datetime.now().isoweekday() != day_note:
        time.sleep(60)
    else:
        if time_now == note_time:
            print("Вам пора {}".format(" ".join(text_for_print.split()[0:-2])))
            speak("Вам пора {}".format(" ".join(text_for_print.split()[0:-2])))
            open("notes.txt", "w").close()
            time.sleep(60)
