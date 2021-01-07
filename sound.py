"""
отредактировали модуль sound
https://github.com/Paradoxis/Windows-Sound-Manager
"""
from keyboard import Keyboard


class Sound:
    __current_volume = None

    @staticmethod
    def current_volume():
        if Sound.__current_volume is None:
            return 0
        else:
            return Sound.__current_volume

    @staticmethod
    def __set_current_volume(volume):
        if volume > 100:
            Sound.__current_volume = 100
        elif volume < 0:
            Sound.__current_volume = 0
        else:
            Sound.__current_volume = volume

    __is_muted = False

    @staticmethod
    def is_muted():
        return Sound.__is_muted

    @staticmethod
    def __track():
        if Sound.__current_volume == None:
            Sound.__current_volume = 0
            for i in range(0, 50):
                Sound.volume_up()

    @staticmethod
    def volume_up():
        Sound.__track()
        Sound.__set_current_volume(Sound.current_volume() + 2)
        Keyboard.key(Keyboard.VK_VOLUME_UP)

    @staticmethod
    def volume_down():
        Sound.__track()
        Sound.__set_current_volume(Sound.current_volume() - 2)
        Keyboard.key(Keyboard.VK_VOLUME_DOWN)

    @staticmethod
    def volume_set(amount):
        Sound.__track()

        if Sound.current_volume() > amount:
            for i in range(0, int((Sound.current_volume() - amount) / 2)):
                Sound.volume_down()
        else:
            for i in range(0, int((amount - Sound.current_volume()) / 2)):
                Sound.volume_up()

    @staticmethod
    def volume_min():
        Sound.volume_set(0)

    @staticmethod
    def volume_max():
        Sound.volume_set(100)
