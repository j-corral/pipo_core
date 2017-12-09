#!/usr/bin/python
import RPi.GPIO as GPIO


class Motor:
    name = ""
    pins = []
    pwm_pin = None
    pwm = None
    forward_conf = []
    backward_conf = []
    PWM_FREQ = 120
    PWM_COEFF = 1000
    MIN_PWM = 10
    MAX_PWM = 70

    def __init__(self, name, pins, pwm_pin, forward, backward):
        GPIO.setmode(GPIO.BOARD)
        self.name = name
        self.pins = pins
        self.pwm_pin = pwm_pin
        self.forward_conf = forward
        self.backward_conf = backward
        self.__init_pins()

    def __init_pins(self):
        for pin in self.pins:
                GPIO.setup(pin, GPIO.OUT)
                print (self.name + " - init pin: " + str(pin) + " [OUT]")

    def forward(self):
        for pin, value in zip(self.pins, self.forward_conf):
            print (self.name + " [FW] - enable pin : " + str(pin))
            if pin == self.pwm_pin:
                self.__init_pwm()
            else:
                GPIO.output(pin, value)

    def backward(self):
        for pin, value in zip(self.pins, self.backward_conf):
            print (self.name + " [BW] - enable pin : " + str(pin))
            GPIO.output(pin, value)

    def stop(self):
        for pin in self.pins:
            print (self.name + " [STOP] - disable pin : " + str(pin))
            GPIO.output(pin, 0)

    def __init_pwm(self):
        self.pwm = GPIO.PWM(self.pwm_pin, self.PWM_FREQ)
        self.pwm.start(self.MIN_PWM)

    def set_speed(self, i):

        if self.name != "M5":
            
             speed = (self.PWM_COEFF * i) / self.MAX_PWM

             if speed > self.MAX_PWM:
                speed = self.MAX_PWM
             elif speed < self.MIN_PWM:
                speed = self.MIN_PWM

                print (self.name + " - speed:" + str(speed))
             self.pwm.ChangeDutyCycle(speed)
