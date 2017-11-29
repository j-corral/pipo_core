#!/usr/bin/python
import RPi.GPIO as GPIO
import time


class Ultrasonic:

    SLEEP_INIT = 0.25
    SLEEP_TRIG = 0.00001
    GPIO_SIG = None

    GPIO_TRIGGER = None
    GPIO_ECHO = None

    MIN_DIST = 5
    QUART_DIST = 20
    MID_DIST = 50
    FAR_DIST = 75
    MAX_DIST = 100

    def __init__(self, GPIO_SIG, GPIO_TRIGGER, GPIO_ECHO):
        GPIO.setmode(GPIO.BOARD)
        self.GPIO_SIG = GPIO_SIG
        self.GPIO_TRIGGER = GPIO_TRIGGER
        self.GPIO_ECHO = GPIO_ECHO

    def __front_distance(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.GPIO_SIG, GPIO.OUT)
        GPIO.output(self.GPIO_SIG, 0)
        time.sleep(self.SLEEP_INIT)

        GPIO.output(self.GPIO_SIG, 1)
        time.sleep(self.SLEEP_TRIG)
        GPIO.output(self.GPIO_SIG, 0)
        start = time.time()

        GPIO.setup(self.GPIO_SIG, GPIO.IN)

        while GPIO.input(self.GPIO_SIG) == 0:
            start = time.time()

        while GPIO.input(self.GPIO_SIG) == 1:
            stop = time.time()

        elapsed = stop - start
        distance = elapsed * 34000
        distance = distance / 2

        return round(distance)

    def __back_distance(self):

        # use pin numbers
        GPIO.setmode(GPIO.BOARD)

        GPIO.setwarnings(False)

        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # Trigger
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)  # Echo

        GPIO.output(self.GPIO_TRIGGER, 0)

        time.sleep(self.SLEEP_INIT)

        GPIO.output(self.GPIO_TRIGGER, 1)
        time.sleep(self.SLEEP_TRIG)
        GPIO.output(self.GPIO_TRIGGER, 0)
        start = time.time()

        while GPIO.input(self.GPIO_ECHO) == 0:
            start = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:
            stop = time.time()

        elapsed = stop - start
        distance = elapsed * 34000
        distance = distance / 2

        return round(distance)

    def get_speed_rate(self, mode):

        if mode:
            distance = self.__front_distance()
        else:
            distance = self.__back_distance()

        print ("distance: " + str(distance))

        if distance <= self.MIN_DIST:
            return 0
        elif distance <= self.QUART_DIST:
            return 2.5
        elif distance <= self.MID_DIST:
            return 5
        elif distance <= self.FAR_DIST:
            return 7.5
        elif distance >= self.MAX_DIST:
            return 10
        else:
            return 0