# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:57:20 2021

@author: lid
"""
# import os
import subprocess
h1 = 1200
alpha=90
for ij in range(10):
    alpha=alpha + 10
    with open ("D:\\data\\Abaqus\\test\\para.dat",'r') as f:
        x = f.readlines()
        y =[]
        for i in x:
            i =i.strip('\n')
            y.append(i)
        del x
    s1 = "h1="+str(h1)
    s2 = "alpha="+str(alpha)
    y[1] = s1
    y[2] = s2
    with open ("D:\\data\\Abaqus\\test\\para_1.dat",'w') as f:
        for i in y :
            print(i,file=f)
    del y
    p = subprocess.Popen("D:\\data\\Abaqus\\test\\abaqus.bat",cwd="D:\\data\\Abaqus\\test")
    p.wait()
    with open ('D:\\data\\Abaqus\\test\\t1.dat','r') as t1:
        n = 0
        ex = '                              E I G E N V A L U E    O U T P U T     \n'
        while t1.readline() != ex:
            pass
        t1.readline()
        t1.readline()
        t1.readline()
        t1.readline()
        t1.readline()
        eig =[]
        for i in range(10):
            data = t1.readline()
            d = data.split()
            eig.append(d[3]) 
    
    with open("D:\\data\\Abaqus\\test\\res.dat",'a') as f :
        print("h1=",h1,"alpha=",alpha,file=f)
        print(eig,file=f)
    print (ij,"finished")