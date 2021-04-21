# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 20:39:58 2021

@author: lid
"""

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
import queue
from concurrent.futures import ThreadPoolExecutor

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
        self.n = 1
        self.m = 1
        self.t = "task_run is running"
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
            # rpath = "E:/WeiLi/Personal/Python/Test/ServerA/ServerA/Submit"
            rpath ="D:\\data\\python\\submit"
            #tpath : target path, which used to move or copy job file to it
            # tpath="E:\\WeiLi\\Personal\\Python\\Test\\ServerA\\jobs"
            tpath="D:\\data\\python\\liw56\\jobs"
            #jobrpath: job input indeck file located file
            # jobrpath = "E:/WeiLi/Personal/Python/Test/ServerA/ServerA/"
            jobrpath = "D:\\data\\python\\liw56\\jobs "
            #root path
            # ropath = "E:\\WeiLi\\Personal\\Python\\Test\\ServerA\\ServerA"
            ropath = 'D:\\data\\python'
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
                    task_line=[job_id,task['job_name'],task['user_name'],task['charge_number'],task['solver'],task["wall_time"],task["submit_time"],task["folder"],tfgp,tgp,"waiting"]
                    self.task_list_waiting.append(task_line)
                    
                # job_id= job_id + 1
                # print(task_line)
                # print(len(self.task_list_waiting))
            time.sleep(2)
            # self.n = self.n - 1
    def task_solver(self):
        data = self.task
        with open ("run.bat","w") as f:
            if data[4] == "abaqus" :
                print ("echo ask_delete=OFF >abaqus_v6.env",file = f )
                print("ping -n 100 www.bing.com ",file=f)
                # print ("call C:/SIMULIA/Commands/abaqus.bat job=" + str(data["job_name"])+" "+str(data["args"])+" " +"int",file = f )
                print ("del *.env",file = f)
                print ("",file=f)
            elif data[4] =="nastran" :
                 print("ping -n 100 www.baidu.com",file=f)
                # print ('call "C:/Program Files/Siemens/NX1872/NXNASTRAN/bin/nastran.exe " ' + str(data["job_name"])+ " parallel=56 "+" "+"old=no",file = f)
        with open ("run.bat","r") as f:
            print (f.readline)
        if os.path.exists(data[-2]+"/"+"run.bat"):
            os.remove(self.task[-2]+"/"+"run.bat")
        try:
            shutil.move("run.bat",data[-2])
            return True
        except Exception:
            return False
        
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
        # cpath = "E:\\WeiLi\\Personal\\Python\\Test\\ServerA\\ServerA\\Command"
        # task_cancell = self.singal_search(".cancell", cpath)
        # print (self.m)
        print (self.t)
        while self.m>0:
            
            print(len(self.task_list_waiting))
            if len(self.task_list_waiting) > 0 :
                # self.m = self.m - 1
                with self._value_lock:
                    self.task = self.task_list_waiting[0]
                    data = self.task

                    self.task_1 = self.task_list_waiting[0]
                    del self.task_list_waiting[0]
                    print(len(self.task_list_waiting))
                    if self.task[-1]=="cancell":
                        self.task_list_finished.append([data])
                    else:                                        
                        # print(data)
                        print("#############")
                        F = self.task_solver()
                        print(F)
                        #define current work directory
                        trp = data[-2]
                        print(trp)
                        Jobrun = os.path.join(trp,"run.bat")
                        print(Jobrun)
                        while not os.path.exists(Jobrun):
                            time.sleep(1)
                            print("no run bat file")
                        p = subprocess.Popen(Jobrun,cwd=trp)
                        self.task[-1]="running"
                        # p = subprocess.Popen("ping -n 100 www.bing.com >> 1.txt",cwd=trp)
                        pid = p.pid
                        print ("pid"+str(pid)+" is "+str(psutil.pid_exists(pid)))
                        runfile=os.path.join(data[-2],data[1])+".run"
                        print (runfile)
                        with open (runfile,"w") as f:
                            print (pid,file=f)
                        stat = 1
                        while  stat == 1:
                             
                            # self.task_csv()
                            time.sleep(5)
                            print ("pid"+str(pid)+" is "+str(psutil.pid_exists(pid)))
                            if psutil.pid_exists(pid) and os.path.exists(runfile):
                                print ("task is running")
                                # time.sleep(5)
                            elif psutil.pid_exists(pid):                            
                                try:
                                    self.kill_proc_tree(pid)
                                    data[-1] = "killed"
                                    self.task_list_finished.append([data])
                                    stat = 0
                                except Exception:
                                        continue
                            else:
                                os.remove(runfile)
                                data[-1] = "finished"
                                self.task_list_finished.append([data])
                                stat = 0
                    # if psutil.pid_exists(pid):
                    #     self.task_list_finished.append([data,"finished"])
            time.sleep(10)
            
    def lastRnline(filename, N,resfile):
        with open (filename) as f:
            with open(resfile,'a') as r:
                for i in (f.readlines()[-N:]):
                    print(i,end="",file=r)
    def taskfile_tf(self,file):
        tasklist = []
        tasklist.extend(self.task_list_finished)
        tasklist.extend(self.task)
        tasklist.extend(self.task_waiting)
        file_txt = file[1].replace(".lck",".txt")
        file_path = os.path.join(file[0],file_txt)
        file_lck = os.path.join(file[0],file[1])                
        with open (file_path) as f:
            tlist = f.readline()
            tc = tlist.split()
            if tc[0] == "cancell" :
                job_id = int(tc[1])                    
                if job_id == self.task[0] :
                    runfile=os.path.join(self.task[0]["trp"],self.task[0]["job_name"])+".run"
                    os.remove(runfile)
                    os.remove(file_path)
                    os.remove(file_lck)
                    return True
                elif job_id< self.task[0] :
                    os.remove(file_path)
                    os.remove(file_lck)
                    return True
                else:
                    n = job_id - len(self.task_list_finished) - 1
                    self.task_waiting[n][-1] = "cancell"
                    os.remove(file_path)
                    os.remove(file_lck)
                    return True
            elif tc[0] == "monitor" :
                job_id = int(tc[1])
                file = tc[2]
                jobfile = tasklist[job_id][-2]+"/"+file
                job_file = tasklist[job_id][-3]+"/"+file
                if os.path.exists(jobfile):                                        
                    self.lastRnline(jobfile, 50,job_file)
                    return True
                else:
                    return False
    def task_monitor(self):
        #command path
        cpath = "E:\\WeiLi\\Personal\\Python\\Test\\ServerA\\ServerA\\Command"
        while True:
            task_monitor = self.singal_search(".lck", cpath)
            n_list = task_monitor
            time.sleep(1)
            with ThreadPoolExecutor(20) as TPE:               
                for i in range(n_list):                                                            
                    TPE.submit(self.taskfile_tf,task_monitor[i])
                    time.sleep(0.5)
        return task_monitor
    def task_csv(self):
        csv_root = "D:/data/python/liw56/jobs/data.csv"
        with open (csv_root,"w") as f :
            print (self.task_list_finished,file=f)
            print (self.task,file=f)
            print (self.task_list_waiting,file=f)
        
t = sharefunc()
t1 = threading.Thread(target=t.task_move,args=())
t2 = threading.Thread(target=t.task_run,args=())
t1.start()
t2.start()      