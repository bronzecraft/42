# -*- coding: utf-8 -*-
"""
Created on Wed Feb  27 21:10:04 2021
@author: lid
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
        self.n =10
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
    def task_solver(self,data):
        with open ("run.bat","w") as f:
            if data["solver"] == "abaqus" :
                print ("echo ask_delete=OFF >abaqus_v6.env",file = f )
                print ("call call C:/SIMULIA/Commands/abaqus.bat job=" + str(data["job_name"])+" "+str(data["args"])+" " +"int",file = f )
                print ("del *.env",file = f)
                print ("",file=f)
            elif data["solver"] =="nastran" :
                print ('call "C:/Program Files/Siemens/NX1872/NXNASTRAN/bin/nastran.exe " ' + str(data["job_name"])+ " parallel=56 "+" "+"old=no",file = f)
        shutil.move("run.bat",data["trp"])
    def task_run(self):
        sta = 0
        while self.n > 0 :
            if len(self.task_list_waiting) > 0 :
                with self._value_lock:
                    self.task = self.task_list_waiting[0][0]
                    self.task_1 = self.task_list_waiting[0]
                # print(self.task)
                    del self.task_list_waiting[0]
                    data=self.task_1
                    self.task_solver(data)
                    trp = data["trp"]
                    # shutil.move('run.bat', trp)
                    Jobrun = os.path.join(trp,"run,bat")
                    p = subprocess.Popen(Jobrun,cwd=data["trp"])
                    pid = p.pid
                    runfile=os.path.join(data["trp"],data["job_name"])+".run"
                    with open (runfile,"w") as f:
                        print (pid,file=f)                    
                    task_cancell_list = self.singal_search(".cancell", "\\\\s4nas02.ap.cat.com\\ITDD_Groupdata02\\desk_hpc\\ServerA")
                    for i in task_cancell_list:
                        task_cancell = os.path.join(data["trp"]+data["master"]) + ".cancell"
                    while os.path.exists(runfile):
                        if not os.path.exists(task_cancell):
                            time.sleep(5)
                            self.task_statue = "running"
                            continue
                        else:
                            os.remove(runfile)
                            self.kill_proc_tree(pid)
                            self.task_statue = "killed"
                with open("\\\\s4nas02.ap.cat.com\\ITDD_Groupdata02\\desk_hpc\\ServerA\\Database.csv","w+") as ds:
                    for i in self.task_list_finished:
                        print (i,file=ds)
                    print ([self.task,"running"],file=ds)
                    for i in self.task_list_waiting:
                        print (i,file=ds)
                with open (self.task_1[2],"r") as h:
                    data = json.load(h)
            time.sleep(1)
    def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=True,timeout=None, on_terminate=None):
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
    def lastRnline(filename, N,resfile):
        with open (filename) as f:
            with open(resfile,'a') as r:
                for i in (f.readlines()[-N:]):
                    print(i,end="",file=r)
    def task_control(self):
        path = "\\\\s4nas02.ap.cat.com\\ITDD_Groupdata02\\desk_hpc\\ServerA"
        task_cancell = self.singal_search(".cancell",path)
        path = os.path.join("")
        while os.path.exists(""):
            os.remove(path_task)
    def task_move(self):
        job_id= 0
        while self.n > 0:
            print ("searching for job ....")
            rpath = "\\\\s4nas02.ap.cat.com\\ITDD_Groupdata02\\desk_hpc\\ServerA"
            tpath="E:\\WeiLi\\jobs"
            tasklist_singal = self.singal_search('.lck', rpath)
            n_list = len(tasklist_singal)
            t_line=[]
            
            for i in range(n_list):
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
                    if not os.path.exists(task['user_name']):
                        os.makedirs(task['user_name'])
                    if not os.path.exists(task['user_name']+"/"+task['job_name']):
                        os.makedirs(task['user_name']+"/"+task['job_name'])
                        tgp = os.path.join(tpath,task['user_name'])
                        tfgp = os.path.join(tgp,task['job_name'])
    # if os.path.exists(task['account'])
                        jobfile = os.path.join(tasklist_singal[i][0],task["master"])+".inp"
                        shutil.copy(jobfile,tfgp)
                        os.remove(file_lck)                    
                    with self._value_lock:
                        ts = os.path.join(tpath,file)
                        task_line=[job_id,task['job_name'],task['user_name'],task['charge_number'],task['solver'],task["cpus"],task["folder"],ts]
                        self.task_list_waiting.append(task_line)
                job_id= job_id + 1
                print("searching")
            time.sleep(2)
                # for i in t_line:
                #     print(i)
    def task_monitor(self):
        tpath = "\\\\s4nas02.ap.cat.com\\ITDD_Groupdata02\\desk_hpc\\ServerA"
        task_m_list = self.singal_search('.monitor', tpath)
        for i in task_m_list:
            job_sta_1 = task_m_list[i][1].replace(".monitor",".sta") + "1"
            job_sta = task_m_list[i][1].replace(".monitor",".sta")
            self.lastRnline(self,job_sta,10, job_sta_1)
            file_sta = os.path.join(task_m_list[i][1],"sta")
            if os.path.exists(file_sta):
                os.remove(file_sta)
            shutil.move(job_sta_1,task_m_list[i][0])
        time.sleep(5)

    # def aba_mon(self):
    # def nas_mon(self):
    
            

t =sharefunc()



t1 = threading.Thread(target=t.task_move,args=())
t2 = threading.Thread(target=t.task_run,args=())
t3 = threading.Thread(target=t.task_monitor,args=())
t1.start()
t2.start()
t3.start()