#!/usr/bin/python
import Motor
import time


class Pipo:
    M_CONF = None
    Motors = [Motor] * 4
    SPEED_STEPS = 10
    SPEED_SLEEP = 0.25

    def __init__(self, M_CONF):
        self.M_CONF = M_CONF
        if self.M_CONF is not None:
            self.__init_motors()
        else:
            raise RuntimeError("Motors are not configured !")

    def __init_motors(self):
        print("Pipo: init motors..." )
        for i,M in enumerate(self.M_CONF):
            self.Motors[i] = Motor.Motor(M["name"], M["pins"], M["pwm_pin"], M["forward"], M["backward"])

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
