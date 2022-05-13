# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:09:27 2020

@author: AKoul
"""

import nidaqmx
import time
from tcp_data.tcp_com import tcp_data

class ni_ao():
    def __init__(self,ao_dev="Dev2/ao0"):
        self.task = nidaqmx.Task()
        self.task.ao_channels.add_ao_voltage_chan(ao_dev)
#        task.ao_channels.add_ao_voltage_chan("Dev2/ao0")
    def send_data_trigger(self,data,code=[0,2,0]):
        self.tcp_con = tcp_data()        
        self.tcp_con.connect_tcp()
        self.tcp_con.send_data(data)
#        self.task.write(code, auto_start=True)
        # we might do away with waiting to receive
#        self.tcp_con.rec_data()
        
    def send_trigger(self,code=[0,2,0]):
        self.task.write(code, auto_start=True)
        
    def send_test_trigger(self,code=[0,2,0]):
        self.task.write(code, auto_start=True)

        
        

class ni_do():
    def __init__(self,do_dev="Dev2/port1/line0"):
        self.task = nidaqmx.Task()
        self.task.do_channels.add_do_chan(do_dev)
        
    def send_trigger(self,pulse_time_s=0.1):
        self.task.write(True, auto_start=True)
        time.sleep(pulse_time_s)
        self.task.write(False, auto_start=True)
        