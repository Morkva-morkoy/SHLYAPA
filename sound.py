"""
отредактировали модуль sound
https://github.com/Paradoxis/Windows-Sound-Manager
"""
"""
The MIT License (MIT)

Copyright (c) 2016 Paradoxis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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
