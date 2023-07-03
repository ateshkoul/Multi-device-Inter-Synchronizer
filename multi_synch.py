# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:51:25 2020

@author: AKoul
"""
#import cv2
#import matplotlib.pyplot as plt
import pdb
import time
#import json
import os
from utils.utils import get_current_list,update_list,approx_frame_rate,switch
from utils.check_functions import check_subject_data,check_input
from eye_tracker.pupil_labs import dual_pupil
from ni_card.acquire_ni import ni_ao,ni_do
from serial_port.serial_con import serial_connect
import random

class multisynch():
#  def __init__(self,device_nos,portname='/dev/ttyUSB0'):
#  def __init__(self,device_nos,portname='COM4'):
  def __init__(self,eye_ip0,eye_port0,eye_ip1,eye_port1,ao_dev="Dev2/ao0",do_dev="Dev2/port1/line0",serial_portname='COM3'):
      
      print("\nChecking pupil-labs connection ...")
      try:
          self.dual_pupil_lab = dual_pupil(eye_ip0,eye_port0,eye_ip1,eye_port1)
          print("\nConnected to eye tracker")
      except:
          print("\nCan't connect to eye tracker")
      
      print("\nChecking video camera connection ...")
      try:
          self.ni_synch_cam = ni_ao(ao_dev)
          print("\nConnected to video cameras")
      except:
          print("\nCan't connect to video cameras")
          
      print("\nChecking video camera connection ...")
      try:
          self.ni_vicon = ni_do(do_dev)
          print("\nConnected to vicon")
      except:
          print("\nCan't connect to video cameras")
      
      # BIOSEMI
      print("\nChecking BIOSEMI connection...")
      try:
          self.serial_con = serial_connect(serial_portname)
          print("\nConnected to BIOSEMI computer")
      except:
          print("\nCan't connect to BIOSEMI computer")
#      pdb.set_trace()
    
      
      # have to add module for checking all the equipment
      
  def check_connections(self):
      try:
          self.serial_con.serial_write(1)
          print('sent trigger')
      except:
          print("\nCan't send trigger to BIOSEMI computer")
          
      try:
          self.dual_pupil_lab.check_acq_start()
          print('sent trigger')
      except:
          print("\nCan't send trigger to pupil labs")
          
      try:
          self.ni_vicon.send_trigger()
          print('sent trigger')
      except:
          print("\nCan't send trigger to vicon")
          
      try:
          self.ni_synch_cam.send_trigger()
          
          test_tcp = {'test': 'test'}
          self.ni_synch_cam.send_data_trigger(test_tcp)
          print('sent trigger')
      except:
          print("\nCan't send trigger to video cameras")
      
  def create_sub_dir(self,sub_entry):
      self.results = sub_entry

#      self.results['path'] = os.path.join("Data","Sub_" + str(self.results['subject_no']),"Ses_" + str(self.results['session_no']))
#      pdb.set_trace()
      self.results['path'] = os.path.join("Data","Dyd_%.3d" % self.results['dyad_no'],"Ses_%.3d" % self.results['session_no'])
#      pdb.set_trace()
      try:
          if not os.path.exists(self.results['path']):
              # create a path if it doesn't exist
              os.makedirs(self.results['path'])
      except OSError:
          print ("Creation of the directory %s failed" % self.results['path'])
      else:
          print ("Successfully created the directory %s " % self.results['path'])
          
  def calibrate(self):
      # calibrate the eye-tracker
      eye_sub_0_code =  "Dyd_%.3d" % self.results['dyad_no'] + '\\' + 'calibration' + '\\' + 'Sub_0'
      eye_sub_1_code =  "Dyd_%.3d" % self.results['dyad_no'] + '\\' + 'calibration' + '\\' + 'Sub_1'
      self.dual_pupil_lab.start_rec('R ' + eye_sub_0_code,'R ' +eye_sub_1_code)
      # start calibratioj
      self.dual_pupil_lab.send_code('C','C')

      
      
      proceed = input('finished calib?\n')
      
      # stop calibratioj
#      self.dual_pupil_lab.send_code('c','c')
      self.dual_pupil_lab.start_rec('r ' + eye_sub_0_code,'r ' +eye_sub_1_code)
      
  def start_acq_buffer(self,codes,task_name,capture_duration):
      data = {'codes': codes,'task_name' : task_name}
#     video cameras are working: this should be the last one?
#            the way it is right now, this sends data and a trigger.
#            These could be segredated as sending only data and then trigger
#             would have to be updated also in the script
      self.ni_synch_cam.send_data_trigger(data)
      
      # eye tracking is working
      eye_sub_0_code =  "Dyd_%.3d" % self.results['dyad_no'] + '\\' + str(task_name) + '\\' + 'Sub_0'
      eye_sub_1_code =  "Dyd_%.3d" % self.results['dyad_no'] + '\\' + str(task_name) + '\\' + 'Sub_1'
      self.dual_pupil_lab.start_rec('R ' + eye_sub_0_code,'R ' +eye_sub_1_code)
      

      self.ni_vicon.send_trigger()
      self.serial_con.serial_write(data['codes'][0])
 

#      pdb.set_trace()
      self.ni_synch_cam.send_trigger()
      time.sleep(capture_duration)
      # send another trigger at the end for vicon
      self.serial_con.serial_write(data['codes'][1])
      self.ni_vicon.send_trigger()
      
#      self.ni_synch_cam.rec_data()
      
      self.dual_pupil_lab.stop_rec('r ' + eye_sub_0_code,'r ' +eye_sub_1_code)
      # this is critical so that the system waits for the video cameras to finish
      self.ni_synch_cam.tcp_con.rec_data()
      
      
      print('done')
          
  def run_task_buffer(self,task_name,capture_duration = 120):
    #pdb.set_trace()
    for case in switch(task_name):
        if case('Baseline_start'):
            self.start_acq_buffer(codes = (10,11),task_name=task_name,capture_duration=capture_duration)
            break
            # in theory the two commands could be combined but 
#            # I want to keep the check_input function as general as possible
#            # I would loose the specific condition names
#            acquisition = input("Start the baseline1? y/n ")
#            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
#            
#
##            pdb.set_trace()
#            if acquisition in ['y', 'yes']:
#                self.start_acq_buffer(codes = (10,11),task_name=task_name,capture_duration=capture_duration)              
#            break
        if case('FaOcc'):
            self.start_acq_buffer(codes = (20,21),task_name=task_name,capture_duration=capture_duration)
            break
#            acquisition = input("Start the Far with Occluder?  y/n ")
#            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
#
#            if acquisition in ['y', 'yes']:
#                self.start_acq_buffer(codes = (20,21),task_name=task_name,capture_duration=capture_duration)
#            break
        if case('FaNoOcc'):
            self.start_acq_buffer(codes = (30,31),task_name=task_name,capture_duration=capture_duration)
            break
#            acquisition = input("Start the Far with No Occluder?  y/n ")
#            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
#
#            if acquisition in ['y', 'yes']:           
#                self.start_acq_buffer(codes = (30,31),task_name=task_name,capture_duration=capture_duration)
#            break
        if case('NeOcc'):
            self.start_acq_buffer(codes = (40,41),task_name=task_name,capture_duration=capture_duration)
            break
#            acquisition = input("Start the Near with Occluder?  y/n ")
#            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
#            if acquisition in ['y', 'yes']:            
#                self.start_acq_buffer(codes = (40,41),task_name=task_name,capture_duration=capture_duration)
#            break
        if case('NeNoOcc'):
            self.start_acq_buffer(codes = (50,51),task_name=task_name,capture_duration=capture_duration)
            break
#            acquisition = input("Start the Near with No Occluder?  y/n ")
#            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
#            if acquisition in ['y', 'yes']:            
#                self.start_acq_buffer(codes = (50,51),task_name=task_name,capture_duration=capture_duration)
#            break
        if case('Baseline_end'):
            self.start_acq_buffer(codes = (70,71),task_name=task_name,capture_duration=capture_duration)
            break
#            acquisition = input("Start the baseline2 acquisition?  y/n ")
#            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
#            if acquisition in ['y', 'yes']:            
#                self.start_acq_buffer(codes = (60,61),task_name=task_name,capture_duration=capture_duration)
#            break
        if case('Task'):
            self.start_acq_buffer(codes = (60,61),task_name=task_name,capture_duration=capture_duration)
            break
#            acquisition = input("Start the test acquisition?  y/n ")
#            acquisition = check_input(input_value=acquisition,allowed_values=['y','yes','n','no'])
#            if acquisition in ['y', 'yes']:
##                self.start_acq(codes = (70,71),task_name=task_name)
#                self.start_acq_buffer(codes = (70,71),task_name=task_name,capture_duration=capture_duration)
#            break
        if case(): # default, could also just omit condition or 'if True'
            print("something else!")
            break
            # No need to break here, it'll stop anyway 
  def get_cond_list(self):
      n_blocks = 3
      task_list = ['FaOcc','FaNoOcc','NeOcc','NeNoOcc']
#      pdb.set_trace()
      # not randomized for now
#      randomized_task_list = task_list
      


#     to generate a pseudo random order
      # monkey
#      randomized_order_key = get_current_list('condition_sequence.json')
##      print(randomized_order_key)
#      randomized_order = eval(randomized_order_key.split()[0])
#      randomized_task_list = [ task_list[i] for i in randomized_order]
#      update_list('condition_sequence.json',randomized_order_key)
      
      randomized_order_key_0 = get_current_list('condition_sequence_human_0.json')
      randomized_order_key_1 = get_current_list('condition_sequence_human_1.json')
#      print(randomized_order_key)
      randomized_order_0 = eval(randomized_order_key_0.split()[0])
      randomized_order_1 = eval(randomized_order_key_1.split()[0])
      
      
      randomized_task_list_0 = [ task_list[i] for i in randomized_order_0]
      randomized_task_list_1 = [ task_list[i] for i in randomized_order_1]
      
      update_list('condition_sequence_human_0.json',randomized_order_key_0)
      update_list('condition_sequence_human_1.json',randomized_order_key_1) 
      
      
#      pdb.set_trace()
      # for the monkey experiment only the 4 conditions
#      final_task_list = ['test','baseline1'] + randomized_task_list + ['baseline2']
      
      Blocks = n_blocks* (randomized_task_list_0 + ['Task'] + randomized_task_list_1)
#      final_task_list = ['Baseline_start'] + Blocks + ['Baseline_end']
      final_task_list =  Blocks 

#      pdb.set_trace()
      print("The experimental conditions are :" + " ".join(final_task_list))
      self.results['final_task_list'] = final_task_list
      return(final_task_list)


#  def start_experiment(self):
#      
#      
#      
#      task_list = ['FaOcc','FaNoOcc','NeOcc','NeNoOcc']
#      
#      # not randomized for now
##      randomized_task_list = task_list
#      
#
#      randomized_order_key = get_current_list('condition_sequence.json')
##      print(randomized_order_key)
#      randomized_order = eval(randomized_order_key.split()[0])
#      randomized_task_list = [ task_list[i] for i in randomized_order]
#      update_list('condition_sequence.json',randomized_order_key)
##      pdb.set_trace()
#      # for the monkey experiment only the 4 conditions
##      final_task_list = ['test','baseline1'] + randomized_task_list + ['baseline2']
#      final_task_list = ['test'] + randomized_task_list
#      print("The experimental conditions are :" + " ".join(randomized_task_list))
#      self.results['final_task_list'] = final_task_list
#      proceed = input("To proceed press enter ")
#      
#      if not proceed:
#          for task_name in final_task_list:
#              self.run_task_buffer(task_name)
##          self.results['final_task_list'] = final_task_list
#      else:
#          print("You pressed " + proceed)
#          confirm_proceed = input(" Do you want to stop experiment? y/n ")
#          if confirm_proceed == 'n':
#              for task_name in final_task_list:
#                  self.run_task_buffer(task_name)
##              self.results['final_task_list'] = final_task_list     
      
  
  def releaseCams(self):
      for device in self.devices:
          print("releasing cameras")
          self.cam[str(device)].release()
