# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 11:47:03 2021

@author: liw56
"""


import threading
import time
import psutil
import os
import shutil
import json
import subprocess
import signal

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
        self.n =1
        self.status=[]
# search singal file 
    def singal_search(self,file_type,path):
        file_list =[]
        for root, dirs, files in os.walk(path):
            for i in files :
                if os.path.splitext(i)[-1] == file_type:
                    j = os.path.join(root,i)
                    k = root.replace('\\','/')
                    # print (k)
                    t = os.path.getmtime(j)
                    file_list.append([k,i,t])
                    file_list = sorted(file_list,key=lambda x:x[2])
 # [file path, file,file time]     
        return file_list
    def task_move(self):
        # job_id= 0
        while self.n > 0:
            print ("searching for job ....")
            # rpath : resource path, which used to search for job json file 
            rpath = "E:/WeiLi/Personal/Python/Test/ServerA/ServerA/Submit"
            #tpath : target path, which used to move or copy job file to it
            tpath="E:\\WeiLi\\Personal\\Python\\Test\\ServerA\\jobs"
            #jobrpath: job input indeck file located file
            jobrpath = "E:/WeiLi/Personal/Python/Test/ServerA/ServerA/"
            #root path
            ropath = "E:\\WeiLi\\Personal\\Python\\Test\\ServerA\\ServerA"
            tasklist_singal = self.singal_search('.lck', rpath)
            n_list = len(tasklist_singal)
            # t_line=[]    
            for i in range(n_list):
                job_id = tasklist_singal[i][1].split(".")[0]
                file = tasklist_singal[i][1].replace(".lck",".json")
                file_path = os.path.join(tasklist_singal[i][0],file)
                file_lck = os.path.join(tasklist_singal[i][0],tasklist_singal[i][1])
                print (file_path)
                try:
                    with open(file_path) as f:
                        task = json.load(f) 
                except (FileNotFoundError):
                        print ("error, json file not found")
                except Exception :
                        print ("json file has a problem")
                if not os.path.exists(tpath+"/"+task['user_name']):
                    os.makedirs(tpath+"/"+task['user_name'])
                # if not os.path.exists(tpath+"/"+task['user_name']+"/"+task['job_name']):
                #     os.makedirs(tpath+"/"+task['user_name']+"/"+task['job_name'])
                    
                tfgp = ropath + "/"+task['user_name']+"/"+task['job_name']
    # if os.path.exists(task['account'])
                    # jobfile = os.path.join(tasklist_singal[i][0],task["master"])+".inp"
                t = str(time.perf_counter())
                tf = t.replace(".","p")
                tgp = tpath+"/"+task['user_name']+"/"+tf

                shutil.copytree(tfgp,tgp)
                os.remove(file_lck)                    
                with self._value_lock:
                    task_line=[job_id,task['job_name'],task['user_name'],task['charge_number'],task['solver'],task["wall_time"],task["submit_time"],task["folder"],tfgp,tgp]
                    self.task_list_waiting.append(task_line)
                # job_id= job_id + 1
                print(task_line)
                time.sleep(2)
                self.n = self.n - 1
    def task_solver(self,data):
        with open ("run.bat","w") as f:
            if data["solver"] == "abaqus" :
                print ("echo ask_delete=OFF >abaqus_v6.env",file = f )
                print ("call C:/SIMULIA/Commands/abaqus.bat job=" + str(data["job_name"])+" "+str(data["args"])+" " +"int",file = f )
                print ("del *.env",file = f)
                print ("",file=f)
            elif data["solver"] =="nastran" :
                print ('call "C:/Program Files/Siemens/NX1872/NXNASTRAN/bin/nastran.exe " ' + str(data["job_name"])+ " parallel=56 "+" "+"old=no",file = f)
        if os.path.exists(self.task[-1]+"/"+"run.bat"):
            os.remove(self.task[-1]+"/"+"run.bat")
        shutil.move("run.bat",data["trp"])
    def kill_proc_tree(self,pid, sig=signal.SIGTERM, include_parent=True,timeout=None, on_terminate=None):
        assert pid != os.getpid(), "won't kill myself"
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        if include_parent:
            children.append(parent)
            for p in children:
                try:
                    p.send_signal(sig)
                except psutil.NoSuchProcess:
                    pass
        gone, alive = psutil.wait_procs(children, timeout=timeout, callback=on_terminate)
        return (gone, alive)
    def task_run(self):
        cpath = "E:\\WeiLi\\Personal\\Python\\Test\\ServerA\\ServerA\\Command"
        # task_cancell = self.singal_search(".cancell", cpath)
        while self.n>0:
            if len(self.task_list_waiting) > 0 :
                with self._value_lock:
                    self.task = self.task_list_waiting[0]
                    self.task_1 = self.task_list_waiting[0]
                    del self.task_list_waiting[0]
                    data = self.task
                    self.task_solver(data)
                    #define current work directory
                    trp = data[-1]
                    Jobrun = os.path.join(trp,"run,bat")
                    p = subprocess.Popen(Jobrun,cwd=trp)
                    pid = p.pid
                    runfile=os.path.join(data["trp"],data["job_name"])+".run"
                    with open (runfile,"w") as f:
                        print (pid,file=f)
                    while not os.path.exists(runfile):
                        time.sleep(10)
                        try:
                            self.kill_proc_tree(pid)
                            self.task_list_finished.append([data,"killed"])
                        except Exception:
                            continue
                    self.task_list_finished.append([data,"finished"])
            time.sleep(10)
    def lastRnline(filename, N,resfile):
        with open (filename) as f:
            with open(resfile,'a') as r:
                for i in (f.readlines()[-N:]):
                    print(i,end="",file=r)
    def task_monitor(self):
        cpath = "E:\\WeiLi\\Personal\\Python\\Test\\ServerA\\ServerA\\Command"
        task_monitor = self.singal_search(".lck", cpath)
        n_list = task_monitor
        for i in range(n_list):
            file = task_monitor[i][1].replace(".lck",".txt")
            file_path = os.path.join(task_monitor[i][0],file)
            file_lck = os.path.join(task_monitor[i][0],task_monitor[i][1])
            with open (file_path) as f:
                tlist = f.readline()
                tc = tlist.split()
                if tc[0] == "cancell" :
                    job_id = int(tc[1])
                    if job_id == self.task[0] :
                        runfile=os.path.join(self.task[0]["trp"],self.task[0]["job_name"])+".run"
                        os.remove(runfile)
                if tc[0] == "monitor" :
                    if tc[2].split(".")[1]=="odb":
                        if 
        return task_monitor
        
        
        
         
                  
                        
                        
                        
                    