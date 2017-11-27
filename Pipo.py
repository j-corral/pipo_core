#!/usr/bin/python
import Motor
import Ultrasonic
import time


class Pipo:
    M_CONF = None
    Motors = [Motor] * 4

    S_CONF = None
    Sensors = None

    FRONT_SPEED_RATE = 0
    BACK_SPEED_RATE = 0

    SPEED_STEPS = 10
    SPEED_SLEEP = 0.25

    CURRENT_SPEED = 0
    TARGET_SPEED = 0

    def __init__(self, M_CONF, S_CONF):
        self.M_CONF = M_CONF

        if self.M_CONF is not None:
            self.__init_motors()
        else:
            raise RuntimeError("Motors are not configured !")

        if self.S_CONF is not None:
            self.S_CONF = S_CONF
            self.__init_sensors()
        else:
            raise RuntimeError("Sensors are not configured !")

    def __init_motors(self):
        print("Pipo: init motors..." )
        for i,M in enumerate(self.M_CONF):
            self.Motors[i] = Motor.Motor(M["name"], M["pins"], M["pwm_pin"], M["forward"], M["backward"])

    def __init_sensors(self):
        self.Sensors = Ultrasonic.Ultrasonic(
            self.S_CONF["pin_sig"],
            self.S_CONF["pin_trig"],
            self.S_CONF["pin_echo"],
        )

    def forward(self):
        for i,M in enumerate(self.Motors):
            (self.Motors[i]).forward()
        self.__accelerate()

    def backward(self):
        for i,M in enumerate(self.Motors):
            (self.Motors[i]).backward()
        self.__accelerate()

    def stop(self):
        for i,M in enumerate(self.Motors):
            (self.Motors[i]).stop()

    def left(self):
        self.stop()
        # todo: conf left

    def right(self):
        self.stop()
        # todo: conf right

    def __accelerate(self):

        speed = 0
        while speed < self.SPEED_STEPS:
            speed += 1

            for i, M in enumerate(self.Motors):
                (self.Motors[i]).set_speed(speed)

            time.sleep(self.SPEED_SLEEP)

    def __adapt_speed(self):

        while 1:
            time.sleep(self.SPEED_SLEEP)
            self.FRONT_SPEED_RATE = self.Sensors.get_speed_rate(1)
            self.BACK_SPEED_RATE = self.Sensors.get_speed_rate(0)
