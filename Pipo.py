#!/usr/bin/python
import Motor
import Ultrasonic
import time


class Pipo:
    M_CONF = None
    Motors = [Motor] * 4

    S_CONF = None
    Sensors = None

    SPEED_RATE = 0

    SPEED_STEPS = 10
    SPEED_SLEEP = 0.25

    CURRENT_SPEED = 0
    TARGET_SPEED = 0

    POS_STOP = "stop"
    POS_FORWARD = "forward"
    POS_BACKWARD = "backward"

    CURRENT_POS = POS_STOP

    def __init__(self, M_CONF, S_CONF):
        self.M_CONF = M_CONF

        if self.M_CONF is not None:
            self.__init_motors()
        else:
            raise RuntimeError("Motors are not configured !")

        self.S_CONF = S_CONF
        if self.S_CONF is not None:
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
        self.CURRENT_POS = self.POS_BACKWARD
        for i,M in enumerate(self.Motors):
            (self.Motors[i]).forward()
        #self.__accelerate()
        self.__adapt_speed()

    def backward(self):
        self.CURRENT_POS = self.POS_FORWARD
        for i,M in enumerate(self.Motors):
            (self.Motors[i]).backward()
        #self.__accelerate()
        self.__adapt_speed()

    def stop(self):
        self.CURRENT_POS = self.POS_STOP
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

            if self.CURRENT_POS == self.POS_FORWARD:
                self.SPEED_RATE = self.Sensors.get_speed_rate(1)
            elif self.CURRENT_POS == self.POS_BACKWARD:
                self.SPEED_RATE = self.Sensors.get_speed_rate(0)

            for i, M in enumerate(self.Motors):
                (self.Motors[i]).set_speed(self.SPEED_RATE)

