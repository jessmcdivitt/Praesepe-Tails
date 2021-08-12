#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 12:10:45 2021

@author: jessica
"""

import astropy.io.ascii as at
import matplotlib.pyplot as plt
import numpy as np

t3=at.read("Praesepe_tails_absolute_magnitude.csv")
good=np.where(t3["Quality"] == 1)
t4=t3[(t3["Quality"] == 1)]

x=t4["BP_RP_2"]
y=t4["Magnitude"]
colors=t4["Prot_Final"]

plt.scatter(x,y,s=10, c=colors)
plt.colorbar()


plt.show()