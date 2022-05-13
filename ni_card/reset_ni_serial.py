# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:18:08 2020

@author: AKoul
"""


import numpy as np

import nidaqmx
# working
with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev2/ao0")
    task.write([0,2,0], auto_start=True)
    
#with nidaqmx.Task() as task:
#    task.ao_channels.add_ao_voltage_chan("Dev2/ao0")
#    task.write([0], auto_start=True)
    
#with nidaqmx.Task() as task:
#    task.ao_channels.add_ao_voltage_chan("Dev2/ao0")
#    task.out_stream.OutStream([0], auto_start=True)
    
#with nidaqmx.Task() as task:
#    task.ao_channels.add_ao_voltage_chan("Dev2/ao0")
#    task.write(list(b'hello'), auto_start=True)