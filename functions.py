import datetime
import token
import vk_api
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

week_days = {
    "понедельник": 1,
    "вторник": 2,
    "среду": 3,
    "четверг": 4,
    "пятницу": 5,
    "субботу": 6,
    "воскресение": 7,
}

def note():
    with open("notes.txt", "r") as file:
        try:
            text_for_print = file.read()
            text = text_for_print.split()
            lent = len(text)
            time_for_note = text[lent - 1].replace(":", " ").split()
            hour_note = int(time_for_note[0])
            minute_note = int(time_for_note[1])
            day_note = week_days[text[-2]]
            hour_now = datetime.datetime.now().hour
            minute_now = datetime.datetime.now().minute
            minute_now += hour_now * 60
            minute_note += hour_note * 60
            day_now = datetime.datetime.now().isoweekday()
            time_diff = minute_note - minute_now
            day_diff = day_note - day_now
            note_time = ":".join(time_for_note)
            if day_now == day_note:
                if time_diff >= 0:
                    print(
                        f"У вас осталось {time_diff // 60} часов {time_diff % 60} минут до того, чтобы {text_for_print}"
                    )
                else:
                    print("Вы прошляпили свой план")

            else:
                print(
                    f"У вас осталось {day_diff} дней {time_diff // 60} часов {time_diff % 60} минут до того, чтобы {text_for_print}"
                )


        except IndexError:
            pass
        except ValueError:
            pass


        try:
            return note_time
        except UnboundLocalError:
            print("У вас нет планов")


with open("vk_token.txt") as file:
    token = file.read()


def sent(user_id, messagee):
    vk = vk_api.VkApi(token=token).get_api()
    vk.messages.send(user_id=user_id, message=messagee, random_id=0)


with open("owm_token.txt", "r") as file:
    tok = file.read()


def get_weather(city):
    owm = OWM(tok)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather
    return w
