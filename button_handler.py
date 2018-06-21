import RPi.GPIO as GPIO
import time
import threading


BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)


class ButtonHandler:

    def __init__(self):
        self._callbacks = []
        self._callback_lock = threading.RLock()

    def register_callback(self, callback):
        self._callback_lock.acquire()
        self._callbacks.append(callback)
        self._callback_lock.release()

    def watchdog(self):
        while True:
            pressed = not GPIO.input(BUTTON)
            if pressed:
                self._callback_lock.acquire()
            for cb in self._callbacks:
                cb()

            time.sleep(2)



