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
# from covid import Covid
import getpass
# from translate import Translator
from googletrans import Translator
import random
# import pyautogui as pg
from sound import Sound

opts = {
    "names": ("шляпа", "шляпы", "шляпу"),
    "tbr": ("сколько", "какое", "блин", "выключи", "слово", "слова", "мне"),
    "cmds": {
        "cdate": ("число", "сегодня число"),
        "ctime": ("время", "сейчас времени"),
        "web_search": ("найди", "найти"),
        "off": ("dadads", "компьютер"),
        "course_usd": ("курс доллара", "доллар в рублях"),
        "course_eur": ("курс евро", "евро в рублях"),
        "apps": ("открой", "запусти"),
        "send": ("отправь", "сообщение"),
        "note": ("напомни", "dasdasd"),
        "note1": ("мои планы", "планы"),
        "temp": ("температура", "сейчас температура"),
        "sky": ("осадки", "сейчас осадки"),
        "wind_speed": ("ветер", "скорость ветра"),
        "if_rain": ("дождь", "сейчас есть дождь"),
        "humidity": ("влажность", "сейчас влажность"),
        "random": ("подкинь монетку", "подкинь монету"),
        "corona": ("коронавирус", "случаев короновируса"),
        "translate": ("переведи", "переведи слово", "перевод"),
        "print": ("напечатай", "печатай"),
        "close": ("закрой", "закрыть"),
        "sound": ("громкость на", "громкость"),
        "sound_switch": ("звук", "das"),
        "sound_max": ("максимальная", "dakjhd"),
        "wiki": ("что такое", "значение", "что значит"),
    },
}

vk_names = {
    #"ИМЯ": ID
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


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)
        for i in opts["names"]:
            if i in voice:
                name_index = voice.split().index(i)
                voice_split = voice.split()
                trash_list = voice_split[:name_index]
                for j in trash_list:
                    if j in voice_split:
                        voice_split.remove(j)
                voice_split.remove(voice_split[0])
                voice = " ".join(voice_split)
                cmd = voice
                cmd = recognize_cmd(cmd)
                if not cmd:
                    return
                execute_cmd(cmd["cmd"], voice, counties, cities, days)

    except sr.UnknownValueError:
        print("[log] Голос не распознан")
    except sr.RequestError:
        print("[log] Bruh")


def recognize_cmd(cmd):
    words = cmd.split()
    if len(words) < 1:
        return
    for i in words:
        if i in opts["tbr"]:
            words.remove(i)
            cmd = " ".join(words)
        else:
            cmd = " ".join(words)
    RC = {"cmd": "", "percent": 65}
    for c, v in opts["cmds"].items():
        for i in v:
            if i in words:
                cmd = i
        for i in v:
            vrt = fuzz.ratio(cmd, i)
            if vrt > RC["percent"] > 60:
                RC["cmd"] = c
                RC["percent"] = vrt
    return RC


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
    elif cmd == "ctime":
        speak("Сейчас" + str(now.hour) + ":" + str(now.minute))
    elif cmd == "course_usd":
        print("{} рублей".format(" ".join(convert[0].text.split())))
        speak("{} рублей".format(" ".join(convert[0].text.split())))
    elif cmd == "course_eur":
        print("{} рублей".format(" ".join(convert[2].text.split())))
        speak("{} рублей".format(" ".join(convert[2].text.split())))
    elif cmd == "apps":
        try:
            voice_for_apps = voice.split()
            voice_for_apps = voice_for_apps[1:]
            voice_for_apps = " ".join(voice_for_apps)
            USER_NAME = getpass.getuser()
            os.startfile(
                "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\{}\\{}".format(
                    voice_for_apps, voice_for_apps
                )
            )
            speak(f"Открываю {voice_for_apps}")

        except FileNotFoundError:
            try:
                os.startfile(
                    "C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\{}".format(
                        USER_NAME, voice_for_apps
                    )
                )
                speak(f"Открываю {voice_for_apps}")
            except FileNotFoundError:
                try:
                    os.startfile(
                        "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\{}".format(
                            voice_for_apps
                        )
                    )
                    speak(f"Открываю {voice_for_apps}")
                except FileNotFoundError:
                    try:
                        os.startfile(
                            "C:\\Users\\{}\\Desktop\\{}".format(
                                USER_NAME, voice_for_apps
                            )
                        )
                        speak(f"Открываю {voice_for_apps}")
                    except FileNotFoundError:
                        print("incorrect app")

    elif cmd == "send":
        try:
            voice_for_vk = voice.split()
            voice_for_id = voice_for_vk[2]
            voice_for_id = vk_names[voice_for_id]
            voice_for_message = voice_for_vk[3:]
            voice_for_message = " ".join(voice_for_message)
            sent(voice_for_id, voice_for_message)
        except Exception:
            pass
    elif cmd == "note":
        voice = voice.split()
        for i in voice:
            if i in opts["tbr"]:
                voice.remove(i)
            for j in opts["cmds"].values():
                if i in j:
                    cmd_index = voice.index(i)
        voice_for_note = voice[cmd_index + 1 :]
        voice_for_note = " ".join(voice_for_note)
        with open("notes.txt", "w") as file:
            file.writelines(voice_for_note)
    elif cmd == "note1":
        note()
    elif cmd == "off":
        check = str(input("Вы уверены что хотите завершить работу компьютера? "))
        if check == "да":
            os.system("shutdown /p")
        else:
            pass
    elif cmd == "temp":
        try:
            print(get_weather(cities[voice.split()[-1]]).temperature("celsius")["temp"])
            speak(get_weather(cities[voice.split()[-1]]).temperature("celsius")["temp"])
        except KeyError:
            print("incorrect city")
    elif cmd == "sky":
        try:
            print(get_weather(cities[voice.split()[-1]]).detailed_status)
            speak(get_weather(cities[voice.split()[-1]]).detailed_status)
        except KeyError:
            print("incorrect city")
    elif cmd == "wind":
        try:
            print(get_weather(cities[voice.split()[-1]]).wind())
            speak(get_weather(cities[voice.split()[-1]]).wind())
        except KeyError:
            print("incorrect city")
    elif cmd == "if_rain":
        try:
            print(get_weather(cities[voice.split()[-1]]).rain)
            speak(get_weather(cities[voice.split()[-1]]).rain)
        except KeyError:
            print("incorrect city")
    elif cmd == "humidity":
        try:
            print(get_weather(cities[voice.split()[-1]]).humidity)
            speak(get_weather(cities[voice.split()[-1]]).humidity)
        except KeyError:
            print("incorrect city")
    # elif cmd == "corona":
    #     try:
    #         covid = Covid(source="worldometers")
    #         action = covid.get_status_by_country_name(countries[voice.split()[-1]])
    #         print(
    #             "В {} {} новых случаев за сегодня".format(
    #                 voice.split()[-1], action["new_cases"]
    #             )
    #         )
    #         speak(
    #             "В {} {} новых случаев за сегодня".format(
    #                 voice.split()[-1], action["new_cases"]
    #             )
    #         )
    #     except KeyError:
    #         pass

    elif cmd == "web_search":
        webbrowser.open_new_tab(
            "https://www.google.com/search?q={}".format("+".join(voice.split()[2:]))
        )

    elif cmd == "translate":
        if Translator(dest="ru").translate(" ".join(voice.split()[1:])) == " ".join(
            voice.split()[1:]
        ):
            translator = Translator(src="ru", dest="en")
        else:
            translator = Translator(src="en", dest="ru")
        print(translator.translate(" ".join(voice.split()[1:])))
        speak(translator.translate(" ".join(voice.split()[1:])))

    elif cmd == "random":
        a = random.randint(1, 2)
        if a == 1:
            speak("Орёл")
            print("Орёл")
        else:
            speak("Решка")
            print("Решка")

    # elif cmd == "print":
    #     pg.write(" ".join(voice.split()[2:]), interval="0.01")
    # elif cmd == "close":
    #     pg.hotkey("alt", "f4")

    elif cmd == "sound":
        try:
            Sound.volume_set(int(voice.split()[-1]))
            speak(
                "Уровень громкости установлен на {} процентов".format(
                    int(voice.split()[-1])
                )
            )
        except ValueError:
            print("Уровень громкости указан неверно")

    elif cmd == "sound_switch":
        if Sound.current_volume() == 0:
            Sound.volume_set(50)
        else:
            Sound.volume_min()

    elif cmd == "sound_max":
        Sound.volume_max()
        speak("Уровень громкости установлен на 100 процентов")
    elif cmd == "wiki":
        try:
            wiki = "https://ru.wikipedia.org/wiki/{}".format(
                "_".join(voice.split()[2:])
            )
            HEADERS = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                "/;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.459",
            }

            def get_html(url, params=""):
                r = requests.get(url, headers=HEADERS, params=params)
                return r

            def get_content(html):
                try:
                    soup = BeautifulSoup(html, "html.parser")
                    items = soup.find("div", class_="mw-parser-output").find("p")
                    return items
                except AttributeError:
                    print("can`t get page content, try again")

            try:
                html = get_html(wiki)
                a = get_content(html.text)
                texts = "".join(a.find_all(text=True))
                stop_point = [".", ":"]
            except AttributeError:
                pass
            for i in list(texts):
                if i in stop_point:
                    a = len(texts.split()[: list(texts).index(i)])
                    if len(texts.split()[: list(texts).index(i)]) < 25:
                        try:
                            dot_index = [
                                i for i, n in enumerate(list(texts)) if n in [".", ":"]
                            ][2]
                        except IndexError:
                            try:
                                dot_index = [
                                    i
                                    for i, n in enumerate(list(texts))
                                    if n in [".", ":"]
                                ][1]
                            except IndexError:
                                dot_index = [
                                    i
                                    for i, n in enumerate(list(texts))
                                    if n in [".", ":"]
                                ][0]
                    else:
                        dot_index = [
                            i for i, n in enumerate(list(texts)) if n in [".", ":"]
                        ][0]
            if len(texts.split()) == 1:
                print("Bruh")
            else:
                print(texts)
                speak("".join(list(texts)[:dot_index]))
        except UnboundLocalError:
            pass
    # else:
    #     webbrowser.open_new_tab(
    #         "https://www.google.com/search?q={}".format("+".join(voice.split()[1:]))
    #     )


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
