# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:56:51 2020

@author: AKoul
"""


import zmq

import msgpack as serializer

from time import sleep, time
class dual_pupil():
    def __init__(self,ip0,port0,ip1,port1):
        self.ctx = zmq.Context()
        self.pupil_remote_0 = zmq.Socket(self.ctx, zmq.REQ)
        self.pupil_remote_0.connect('tcp://'+ ip0 +':'+ port0)
#        pupil_remote.connect('tcp://151.100.55.62:50020')

        self.pupil_remote_1 = zmq.Socket(self.ctx, zmq.REQ)
        self.pupil_remote_1.connect('tcp://'+ ip1 +':'+ port1)
#        pupil_remote_2.connect('tcp://151.100.55.62:56809')
    def start_rec(self,code0='R',code1='R'):
        self.pupil_remote_0.send_string(code0)
        print(self.pupil_remote_0.recv_string())

        self.pupil_remote_1.send_string(code1)
        print(self.pupil_remote_1.recv_string())
        
    def stop_rec(self,code0='r',code1='r'):
        self.pupil_remote_0.send_string(code0)
        print(self.pupil_remote_0.recv_string())

        self.pupil_remote_1.send_string(code1)
        print(self.pupil_remote_1.recv_string())
        
    def send_code(self,code0,code1):
        self.pupil_remote_0.send_string(code0)
        print(self.pupil_remote_0.recv_string())

        self.pupil_remote_1.send_string(code1)
        print(self.pupil_remote_1.recv_string())
    
    def check_acq_start(self):
        # have to complete this module - idea would be to check whether the start and stop are working
        # and if the duration of the files saved match
        self.start_rec('R test0','R test1')
        self.stop_rec()
    def send_annotation(self):
#        https://github.com/pupil-labs/pupil-helpers/blob/master/python/remote_annotations.py
#        topic = 'your_custom_topic'
#        payload = {'topic': topic}
#        
#        # create and connect PUB socket to IPC
##        pub_socket = zmq.Socket(zmq.Context(), zmq.PUB)
##        pub_socket.connect(ipc_pub_url)
#        
#        # send payload using custom topic
#        self.pupil_remote_0.send_string(topic, flags=zmq.SNDMORE)
#        self.pupil_remote_0.send(msgpack.dumps(payload, use_bin_type=True))
        
        # In order for the annotations to be correlated correctly with the rest of
        # the data it is required to change Pupil Capture's time base to this scripts
        # clock. We only set the time base once. Consider using Pupil Time Sync for
        # a more precise and long term time synchronization
        time_fn = time  # Use the appropriate time function here
    
        # Set Pupil Capture's time base to this scripts time. (Should be done before
        # starting the recording)
        self.pupil_remote_0.send_string("T {}".format(time_fn()))
        print(self.pupil_remote_0.recv_string())
        
        self.pupil_remote_1.send_string("T {}".format(time_fn()))
        print(self.pupil_remote_1.recv_string())
    
        # send notification:
        def notify(notification,pupil_remote):
            """Sends ``notification`` to Pupil Remote"""
            topic = "notify." + notification["subject"]
            payload = serializer.dumps(notification, use_bin_type=True)
            pupil_remote.send_string(topic, flags=zmq.SNDMORE)
            pupil_remote.send(payload)
            return pupil_remote.recv_string()
    
        def send_trigger(trigger,pub_socket):
            payload = serializer.dumps(trigger, use_bin_type=True)
            pub_socket.send_string(trigger["topic"], flags=zmq.SNDMORE)
            pub_socket.send(payload)
        
        
        self.pupil_remote_0.send_string("PUB_PORT")    
        pub_port_0 = self.pupil_remote_0.recv_string()

        self.pupil_remote_1.send_string("PUB_PORT")    
        pub_port_1 = self.pupil_remote_1.recv_string()
    
        pub_socket_0 = zmq.Socket(self.ctx, zmq.PUB)
    
        pub_socket_0.connect("tcp://127.0.0.1:{}".format(pub_port_0))
    
        pub_socket_1 = zmq.Socket(self.ctx, zmq.PUB)
    
        pub_socket_1.connect("tcp://127.0.0.1:{}".format(pub_port_1))
        # Start the annotations plugin
        notify({"subject": "start_plugin", "name": "Annotation_Capture", "args": {}},self.pupil_remote_0)
        notify({"subject": "start_plugin", "name": "Annotation_Capture", "args": {}},self.pupil_remote_1)
        
        self.pupil_remote_0.send_string("R")
        self.pupil_remote_0.recv_string()
    
        sleep(1.)  # sleep for a few seconds, can be less
    
        # Send a trigger with the current time
        # The annotation will be saved to annotation.pldata if a
        # recording is running. The Annotation_Player plugin will automatically
        # retrieve, display and export all recorded annotations.
    
        def new_trigger(label, duration):
            return {
                "topic": "annotation",
                "label": label,
                "timestamp": time_fn(),
                "duration": duration,
            }
    
        label = "custom_annotation_label"
        duration = 0.
        minimal_trigger = new_trigger(label, duration)
        send_trigger(minimal_trigger,pub_socket_0)
        send_trigger(minimal_trigger,pub_socket_1)
        sleep(1.)  # sleep for a few seconds, can be less
    
        minimal_trigger = new_trigger(label, duration)
        send_trigger(minimal_trigger,pub_socket_0)
        send_trigger(minimal_trigger,pub_socket_1)
    
        # add custom keys to your annotation
        minimal_trigger["custom_key"] = "custom value"
        send_trigger(minimal_trigger,pub_socket_0)
        send_trigger(minimal_trigger,pub_socket_1)
        sleep(1.)  # sleep for a few seconds, can be less
    
        # stop recording
        self.pupil_remote_0.send_string("r")
        self.pupil_remote_0.recv_string()
        
        
        
class mono_pupil():
    def __init__(self,ip0,port0):
        self.ctx = zmq.Context()
        self.pupil_remote_0 = zmq.Socket(self.ctx, zmq.REQ)
        self.pupil_remote_0.connect('tcp://'+ ip0 +':'+ port0)
#        pupil_remote.connect('tcp://151.100.55.62:50020')

    def start_rec(self,code0='R'):
        self.pupil_remote_0.send_string(code0)
        print(self.pupil_remote_0.recv_string())
        
    def stop_rec(self,code0='r'):
        self.pupil_remote_0.send_string(code0)
        print(self.pupil_remote_0.recv_string())

        
    def send_code(self,code0):
        self.pupil_remote_0.send_string(code0)
        print(self.pupil_remote_0.recv_string())
    
    def check_acq_start(self):
        # have to complete this module - idea would be to check whether the start and stop are working
        # and if the duration of the files saved match
        self.start_rec('R test0')
        self.stop_rec()
    def send_annotation(self):
        # not tested:::10-05-2022:
###############################################4        
#        https://github.com/pupil-labs/pupil-helpers/blob/master/python/remote_annotations.py
#        topic = 'your_custom_topic'
#        payload = {'topic': topic}
#        
#        # create and connect PUB socket to IPC
##        pub_socket = zmq.Socket(zmq.Context(), zmq.PUB)
##        pub_socket.connect(ipc_pub_url)
#        
#        # send payload using custom topic
#        self.pupil_remote_0.send_string(topic, flags=zmq.SNDMORE)
#        self.pupil_remote_0.send(msgpack.dumps(payload, use_bin_type=True))
        
        # In order for the annotations to be correlated correctly with the rest of
        # the data it is required to change Pupil Capture's time base to this scripts
        # clock. We only set the time base once. Consider using Pupil Time Sync for
        # a more precise and long term time synchronization
        time_fn = time  # Use the appropriate time function here
    
        # Set Pupil Capture's time base to this scripts time. (Should be done before
        # starting the recording)
        self.pupil_remote_0.send_string("T {}".format(time_fn()))
        print(self.pupil_remote_0.recv_string())
        
        self.pupil_remote_1.send_string("T {}".format(time_fn()))
        print(self.pupil_remote_1.recv_string())
    
        # send notification:
        def notify(notification,pupil_remote):
            """Sends ``notification`` to Pupil Remote"""
            topic = "notify." + notification["subject"]
            payload = serializer.dumps(notification, use_bin_type=True)
            pupil_remote.send_string(topic, flags=zmq.SNDMORE)
            pupil_remote.send(payload)
            return pupil_remote.recv_string()
    
        def send_trigger(trigger,pub_socket):
            payload = serializer.dumps(trigger, use_bin_type=True)
            pub_socket.send_string(trigger["topic"], flags=zmq.SNDMORE)
            pub_socket.send(payload)
        
        
        self.pupil_remote_0.send_string("PUB_PORT")    
        pub_port_0 = self.pupil_remote_0.recv_string()

        self.pupil_remote_1.send_string("PUB_PORT")    
        pub_port_1 = self.pupil_remote_1.recv_string()
    
        pub_socket_0 = zmq.Socket(self.ctx, zmq.PUB)
    
        pub_socket_0.connect("tcp://127.0.0.1:{}".format(pub_port_0))
    
        pub_socket_1 = zmq.Socket(self.ctx, zmq.PUB)
    
        pub_socket_1.connect("tcp://127.0.0.1:{}".format(pub_port_1))
        # Start the annotations plugin
        notify({"subject": "start_plugin", "name": "Annotation_Capture", "args": {}},self.pupil_remote_0)
        notify({"subject": "start_plugin", "name": "Annotation_Capture", "args": {}},self.pupil_remote_1)
        
        self.pupil_remote_0.send_string("R")
        self.pupil_remote_0.recv_string()
    
        sleep(1.)  # sleep for a few seconds, can be less
    
        # Send a trigger with the current time
        # The annotation will be saved to annotation.pldata if a
        # recording is running. The Annotation_Player plugin will automatically
        # retrieve, display and export all recorded annotations.
    
        def new_trigger(label, duration):
            return {
                "topic": "annotation",
                "label": label,
                "timestamp": time_fn(),
                "duration": duration,
            }
    
        label = "custom_annotation_label"
        duration = 0.
        minimal_trigger = new_trigger(label, duration)
        send_trigger(minimal_trigger,pub_socket_0)
        send_trigger(minimal_trigger,pub_socket_1)
        sleep(1.)  # sleep for a few seconds, can be less
    
        minimal_trigger = new_trigger(label, duration)
        send_trigger(minimal_trigger,pub_socket_0)
        send_trigger(minimal_trigger,pub_socket_1)
    
        # add custom keys to your annotation
        minimal_trigger["custom_key"] = "custom value"
        send_trigger(minimal_trigger,pub_socket_0)
        send_trigger(minimal_trigger,pub_socket_1)
        sleep(1.)  # sleep for a few seconds, can be less
    
        # stop recording
        self.pupil_remote_0.send_string("r")
        self.pupil_remote_0.recv_string()
        
    
    
        
        
 # pupil labs 
#'R'  # start recording with auto generated session name
#'R rec_name'  # start recording named "rec_name" 
#'r'  # stop recording
#'C'  # start currently selected calibration
#'c'  # stop currently selected calibration
#'T 1234.56'  # resets current Pupil time to given timestamp
#'t'  # get current Pupil time; returns a float as string.
#'v'  # get the Pupil Core software version string
#
## IPC Backbone communication
#'PUB_PORT'  # return the current pub port of the IPC Backbone
#'SUB_PORT'  # return the current sub port of the IPC Backbone       
        
        
        
        
        
        
        
        