import datetime
import token
import vk_api
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps


def note():
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
            note_time = ':'.join(time_for_note)
            if time_diff >= 0:
                print(f'У вас осталось {time_diff // 60} часов {time_diff % 60} минут до того, чтобы {text_for_print}')
            else:
                print('Вы прошляпили свой план')
            return note_time
        except IndexError:
            pass
        except ValueError:
            pass
        except UnboundLocalError:
            print('У вас нет планов')


with open('vk_token.txt') as file:
    token = file.read()


def sent(user_id, messagee):
    vk = vk_api.VkApi(token=token).get_api()
    vk.messages.send(
        user_id=user_id,
        message=messagee,
        random_id=0)


with open('owm_token', 'r') as file:
    tok = file.read()


def get_weather(city):
    owm = OWM(tok)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather
    return w
