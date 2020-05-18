#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:21:53 2020

@author: kai
"""
import re
import numpy as np
import copy

motor1 = [0,0]
motor2 = [1,0]

Xnumbers = []
Ynumbers = []

with open('./Pictures/testfile.ngc','w') as h:
    for line in open('./Pictures/test_0001.ngc','r'):
        match = re.search('X',line)         #find lines containing the character X
        if match:
#            print(line, end = '\n')
            xpos = line.find('X')
            ypos = line.find('Y')
            Xnumbers.append(re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",line[xpos:ypos]))
            Zmatch = re.search('Z',line)
            if Zmatch:                      #if there IS a Z in the line, make this the last index
                zpos = line.find('Z')
                Ynumbers.append(re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",line[ypos:zpos]))
            else:                           #if there ISN'T a Z in the line, make the length of the line +1 the last index
                zpos = len(line)+1
                Ynumbers.append(re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",line[ypos:zpos]))
    Xnumbers = list(np.float_(Xnumbers))
    Ynumbers = list(np.float_(Ynumbers))
    maxX = max(Xnumbers)                    #retrieved maximum x value for normalization
    maxY = max(Ynumbers)                    #retrieved maximum y value for normalization
    

    for line in open('./Pictures/test_0001.ngc','r'):
        match = re.search('X',line)
        if match:
            xpos = line.find('X')
            ypos = line.find('Y')
            Zmatch = re.search('Z',line)
            if Zmatch:
                zpos = line.find('Z')
            else:
                zpos = len(line)+1
            X = list(map(float,re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",line[xpos:ypos]))) #X value
            Y = list(map(float,re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",line[ypos:zpos]))) #Y value
            U = np.sqrt((X/maxX)**2 + (Y/maxY)**2)
            V = np.sqrt((motor2[0]-X/maxX)**2 + (Y/maxY)**2)
            
            mod = copy.deepcopy(line)
            mod = mod.replace('X'+str(X[0]),'X'+str(U[0]))
            mod = mod.replace('Y'+str(Y[0]),'Y'+str(V[0]))
#            mod[xpos+1:ypos-1] = str(U)
#            mod[ypos+1:zpos-1] = str(V)
            h.write('{}\n'.format(mod))     #write modified line to file
        else:
            h.write('{}\n'.format(line))    #write unmodified line to file