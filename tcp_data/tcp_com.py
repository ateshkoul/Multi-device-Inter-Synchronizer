# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:46:04 2020

@author: AKoul
"""

import socket
from tcp_data.byte_string import dict_to_bytes
import pdb
#https://www.geeksforgeeks.org/python-interconversion-between-dictionary-and-bytes/
class tcp_data():
    def __init__(self,host="151.100.55.49",port=30):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect_tcp(self):
        self.s.connect((self.host, self.port))
        
    def send_data(self,data):
#        pdb.set_trace()
        self.s.sendall(dict_to_bytes(data))
#        pdb.set_trace()
#        rec_data = self.s.recv(1024)
##        self.s.close()
#        print('Received', repr(rec_data))
    def rec_data(self):
        rec_data = self.s.recv(1024)
#        self.s.close()
        print('Received', repr(rec_data))
    def send_str_data(self,data):
#        pdb.set_trace()
        self.s.sendall( bytes(data, 'utf-8'))

        