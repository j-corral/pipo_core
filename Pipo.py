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
    TURN_SPEED = 5
    TURN_SLEEP = 0.25

    SPEED_STEPS = 10
    SPEED_SLEEP = 0.1

    CURRENT_SPEED = 0
    TARGET_SPEED = 0
    MAX_SPEED = 10

    POS_STOP = "stop"
    POS_FORWARD = "forward"
    POS_BACKWARD = "backward"

    CURRENT_POS = POS_STOP

    DISABLED = []

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
        print("Pipo: init motors...")
        for i, M in enumerate(self.M_CONF):
            self.Motors[i] = Motor.Motor(M["name"], M["pins"], M["pwm_pin"], M["forward"], M["backward"])

    def __init_sensors(self):
        self.Sensors = Ultrasonic.Ultrasonic(
            self.S_CONF["pin_sig"],
            self.S_CONF["pin_trig"],
            self.S_CONF["pin_echo"],
        )

    def forward(self, auto=False):

        auto = bool(int(auto))

        print("Going forward...")
        self.CURRENT_POS = self.POS_FORWARD
        for i, M in enumerate(self.Motors):
            (self.Motors[i]).forward()
        if bool(auto):
            print ("Auto drive: Enabled")
            self.__accelerate(True)
        else:
            print ("Auto drive: Disabled")
            self.__accelerate(False)

    def backward(self, auto=False):
        auto = bool(int(auto))
        print("Going backward...")
        self.CURRENT_POS = self.POS_BACKWARD
        for i, M in enumerate(self.Motors):
            (self.Motors[i]).backward()
        if bool(auto):
            print ("Auto drive: Enabled")
            self.__accelerate(True)
        else:
            print ("Auto drive: Disabled")
            self.__accelerate(False)

    def stop(self):
        print ("Stopping engines...")
        self.CURRENT_POS = self.POS_STOP
        for i, M in enumerate(self.Motors):
            (self.Motors[i]).stop()

    def __reverse(self, auto=False):
        print ("Reversing engines...")
        if self.CURRENT_POS == self.POS_FORWARD:
            self.backward(auto)
        elif self.CURRENT_POS == self.POS_BACKWARD:
            self.forward(auto)
        else:
            self.stop()

    def left(self, auto=False):
        print ("Turning left...")
        #self.DISABLED = [1, 3]
        self.__turnMode(auto, False)

        #if self.CURRENT_POS == self.POS_BACKWARD:
        #    self.DISABLED = [0, 2]

        for i, M in enumerate(self.Motors):
            if i in self.DISABLED:
                (self.Motors[i]).backward()
            else:
                (self.Motors[i]).forward()
            print ("Turn speed: " + str(self.TURN_SPEED))
            (self.Motors[i]).set_speed(self.TURN_SPEED)

        time.sleep(self.TURN_SLEEP)
        self.DISABLED = []

    def right(self, auto=False):
        print ("Turning right...")
        #self.DISABLED = [0, 2]
        self.__turnMode(auto, True)


        #if self.CURRENT_POS == self.POS_BACKWARD:
        #    self.DISABLED = [1, 4]

        for i, M in enumerate(self.Motors):
            if i in self.DISABLED:
                (self.Motors[i]).backward()
            else:
                (self.Motors[i]).forward()
            print ("Turn speed: " + str(self.TURN_SPEED))
            (self.Motors[i]).set_speed(self.TURN_SPEED)

        time.sleep(self.TURN_SLEEP)
        self.DISABLED = []

    def __turnMode(self, auto=False, direction=False):
        if auto:
            print ("Turn: auto mode")
            self.TURN_SPEED = 10
            self.TURN_SLEEP = 0.5

        else:
            print ("Turn: manual mode")
            self.TURN_SPEED = 7
            self.TURN_SLEEP = 0.1

        # if turn right
        if direction:
            # 0: ARD - 1: - ARG - 2: AVD - 3: AVG
            self.DISABLED = [0, 2]
        else:
            self.DISABLED = [1, 3]

    def __accelerate(self,auto=False):

        print ("accelerating...")
        step = 0

        if auto:
            while 1:
                adapt = self.__adapt_speed(auto)
                if not adapt:
                    break
        else:
            while step < self.SPEED_STEPS:
                adapt = self.__adapt_speed(auto)
                if not adapt:
                    break
            #self.SPEED_STEPS = 0

    def __adapt_speed(self, auto=False):
        time.sleep(self.SPEED_SLEEP)

        if self.CURRENT_POS == self.POS_FORWARD:
            self.TARGET_SPEED = self.Sensors.get_speed_rate(True)
        elif self.CURRENT_POS == self.POS_BACKWARD:
            self.TARGET_SPEED = self.Sensors.get_speed_rate(False)
        else:
            return False

        self.SPEED_RATE = self.SPEED_RATE + 1;

        if auto:
            print ("auto adapt")
            if self.SPEED_RATE > self.TARGET_SPEED:
                self.SPEED_RATE = self.TARGET_SPEED

            if self.TARGET_SPEED == 0:
                self.stop()
            if self.TARGET_SPEED <= 1:
                self.__reverse(auto)
            elif self.TARGET_SPEED <= 3:
                self.left(auto)
                self.forward(auto)

        else:
            print ("manual adapt")
            # print ("Speed: " + str(self.TARGET_SPEED))
            if self.TARGET_SPEED <= 3:
                # self.__reverse()
                self.stop()
                return False

        if self.SPEED_RATE > self.MAX_SPEED:
            self.SPEED_RATE = self.MAX_SPEED

        print("Speed: " + str(self.SPEED_RATE))

        for i, M in enumerate(self.Motors):
            if i not in self.DISABLED:
                (self.Motors[i]).set_speed(self.SPEED_RATE)

        return True