# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:18:35 2020

@author: AKoul
"""
import serial

#python -m serial.tools.list_ports
class serial_connect():
    def __init__(self,portname='COM4'):
        self.serial = serial.Serial(port = portname,baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, rtscts=False)
        print("Serial port opened!")
        
        
    def serial_write(self,code):
        self.serial.write(chr(code).encode())