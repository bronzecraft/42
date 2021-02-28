# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 21:10:04 2021

@author: lid
"""

import threading
import time
import queue
import os
import shutil

class sharefunc:
    '''
    shared function
    '''
    def __init__(self,initial_value=0):

        self.data=initial_value
        self._value_lock = threading.Lock()
        self.tasklist = []
        self.task_list_finished=[]
        self.task_list_waiting=[]
        self.task=[]
    def singal_search(self,file_type,path):
        file_list =[]
        for root, dirs, files in os.walk(path):
            for i in files :
                if os.path.splitext(i)[-1] == file_type:
                    # j = os.path.join(root,i)
                    k = root.replace('\\','/')
                    # print (k)
                    file_list.append([k,i])
        return file_list
        
    def task_move(self):
        tasklist_singal = self.singal_search('.singal', path)
        # tasklist_txt = list(map(lambda y : y.replace(".singal",".txt"), tasklist_singal))
        trp = "D:/data/python/Target"
        n_list = len(tasklist_singal)
        for i in range(n_list):
            
            file = tasklist_singal[i][1].replace(".singal",".txt")
            
            file_path = os.path.join(tasklist_singal[i][0],file)
            # print (file_path)
            file_path_singal =  os.path.join(tasklist_singal[i][0],tasklist_singal[i][1])
            file_dir = tasklist_singal[i][0].split("/")[-1]
            tgd = os.path.join(trp,file_dir)
            # print (tgd)
            if not os.path.exists(tgd):
                os.makedirs(tgd)
            shutil.move(file_path,tgd)
            shutil.move(file_path_singal,tgd)
            with self._value_lock:
                ts = os.path.join(tgd,file)
                self.task_list_waiting.append([file,"waiting",ts])
    

    def task_run(self):
        while len(self.task_list_waiting) > 0:
            with self._value_lock:
            # print (len(self.task_list_waiting))
                if len(self.task_list_waiting) > 0 :
                    self.task = self.task_list_waiting[0][0]
                    self.task_1 = self.task_list_waiting[0]
                # print(self.task)
                    del self.task_list_waiting[0]        
            with self._value_lock:
                for i in self.task_list_finished:
                    print (i)
                print ([self.task,"running"])
                for i in self.task_list_waiting:
                    print (i)
            # with open ('task_status.txt',"wt") as f:
            #     for i in self.task_list_finished:
            #         print(i,file = f)
            #     print([self.task,"running"],file =f)
            #     for i in self.task_list_waiting:
            #         print(i,file = f)
                # print(self.task_list_waiting,file =f)
       
            with open (self.task_1[2],"r") as h:
                data = h.read()
                path = str(os.path.splitext(self.task_1[2])[0])+".bat"
            # print (path)
            path_2 = os.path.splitext(path)[0]
            with open (path,"wt") as b:
                print ("ping -n " + str(data) +" www.bing.com > "+str(path_2)+".res", file = b)
            os.system(path)
            self.task_list_finished.append((self.task,'finished'))
        for i in self.task_list_finished:
            print (i)        

t =sharefunc()
path = 'D:/data/python/Source'


l = t.task_move()  
t.task_run()
    

