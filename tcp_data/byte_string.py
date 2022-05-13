# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:43:23 2020

@author: AKoul
"""

import json
#https://www.geeksforgeeks.org/python-interconversion-between-dictionary-and-bytes/
#def dict_to_binary(the_dict):
#    string = json.dumps(the_dict)
#    binary = ' '.join(format(ord(letter), 'b') for letter in string)
#    return(binary)

#def binary_to_dict(the_binary):
#    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
#    d = json.loads(jsn)  
#    return(d)
    
    
def dict_to_bytes(the_dict):
    string = json.dumps(the_dict).encode('utf-8')
    return(string)

def bytes_to_dict(string):
    the_dict = json.loads(string.decode('utf-8'))
    return(the_dict)
    
    


#binary = dict_to_binary(my_dict)
#
#
#dct = binary_to_dict(binary)
