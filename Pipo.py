#!/usr/bin/python
import Motor
import Ultrasonic
import time


class Pipo:
    M_CONF = None
    Motors = [Motor] * 4

    S_CONF = None
    Sensors = None

    SPEED_RATE = 1

    SPEED_STEPS = 10
    SPEED_SLEEP = 0.1

    CURRENT_SPEED = 0
    TARGET_SPEED = 0

    POS_STOP = "stop"
    POS_FORWARD = "forward"
    POS_BACKWARD = "backward"

    CURRENT_POS = POS_STOP

    DISABLED = -1

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
        self.CURRENT_POS = self.POS_FORWARD
        for i,M in enumerate(self.Motors):
            (self.Motors[i]).forward()
        self.__adapt_speed()

    def backward(self):
        self.CURRENT_POS = self.POS_BACKWARD
        for i,M in enumerate(self.Motors):
            (self.Motors[i]).backward()
        self.__adapt_speed()

    def stop(self):
        self.CURRENT_POS = self.POS_STOP
        for i,M in enumerate(self.Motors):
            (self.Motors[i]).stop()

    def left(self):
        self.DISABLED = 3

        if self.CURRENT_POS == self.POS_BACKWARD:
            self.DISABLED = 0

        (self.Motors[self.DISABLED]).set_speed(0)
        time.sleep(2)
        self.DISABLED = -1

    def right(self):
        self.DISABLED = 4

        if self.CURRENT_POS == self.POS_BACKWARD:
            self.DISABLED = 1

        (self.Motors[self.DISABLED]).set_speed(0)
        time.sleep(2)
        self.DISABLED = -1

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
                self.TARGET_SPEED = self.Sensors.get_speed_rate(True)
            elif self.CURRENT_POS == self.POS_BACKWARD:
                self.TARGET_SPEED = self.Sensors.get_speed_rate(False)
            else:
                break

            self.SPEED_RATE = self.SPEED_RATE + 1;

            if self.SPEED_RATE > self.TARGET_SPEED:
                self.SPEED_RATE = self.TARGET_SPEED

            print("Speed: " + str(self.SPEED_RATE))
            
            if self.TARGET_SPEED == 0:
                print("Stop pipo: " + str(self.SPEED_RATE))
                self.stop()
                break

            if self.TARGET_SPEED <= 2:
                print("turn left")
                self.left()
                """"
                self.TARGET_SPEED = 0;
                self.SPEED_RATE = 0;
                if self.CURRENT_POS == self.POS_FORWARD:
                    print("go backward")
                    self.backward()
                else:
                    print("go forward")
                    self.forward()
                """

            for i, M in enumerate(self.Motors):
                if(i != self.DISABLED):
                    (self.Motors[i]).set_speed(self.SPEED_RATE)

