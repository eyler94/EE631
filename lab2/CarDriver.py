#!/usr/bin/env python3
import pyrealsense2 as rs
import numpy as np
import serial
import time
import cv2

class Car_driver():
    def __init__(self):
        # initialize communication with the arduino
        self.ser = serial.Serial("/dev/ttyUSB0", 115200)
        self.ser.flushInput()
        time.sleep(2)

        # Some of these numbers will be different for every car
        self.ser.write("!start1650\n".encode())
        self.ser.write("!inits0.8\n".encode())
        self.ser.write("!straight1575\n".encode())
        self.ser.write("!kp0.01\n".encode())
        self.ser.write("!kd0.01\n".encode())
        self.ser.write("!pid1\n".encode())
        # Required
        self.drive(1.0)
        time.sleep(0.2)
        self.drive(0)

    def drive(self, speed):
        forward_command = "!speed" + str(speed) + "\n"
        self.ser.write(forward_command.encode())

    def steer(self, degree):
        steer_command = "!steering" + str(degree) + "\n"
        self.ser.write(steer_command.encode())


if __name__ == "__main__":
    car = Car_driver()
    while True:
        car.drive(.8)
        car.steer(16)
        time.sleep(4)
        car.drive(.4)
        car.steer(-20)
        time.sleep(4)
        car.drive(0)
        car.steer(0)
        time.sleep(4)

