#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 14:55:21 2021

@author: jessica
"""

import astropy.io.ascii as at
import numpy as np
import matplotlib.pyplot as plt

#Join tables
t1=at.read("Praesepe_latest_AN.csv")
t1.rename_column("DR2_desig", "DR2Name")
t1["BP_RP_1"]=t1["BP"]-t1["RP"]
t1.rename_column("G", "Gmag_1")
t2=at.read("Cumulative_Praesepe_tails_table.csv")
t2.rename_column("BP_RP", "BP_RP_2")
t2.rename_column("Gmag", "Gmag_2")

fig,ax = plt.subplots()

#Pinpoint the quality stars from the cumulative table
good=np.where(t2["Quality"] == 1)
print(t2[good])

#Create a refined table
t3=t2[(t2["Quality"] == 1)]

#Create plots
cluster=ax.plot(t1["BP_RP_1"], t1["Gmag_1"], ".", color="tab:gray", alpha=0.75, markersize="5", label="Central Cluster")
tails=ax.plot(t3["BP_RP_2"], t3["Gmag_2"], "*", color="c", markersize="5", markeredgecolor="black", label="Tails")

#Adjust plot
ax.set_xlabel("BP-RP")
ax.set_ylabel("Apparent Magnitude")
ax.set_ylim(21,5)
ax.set_title("Praesepe")
ax.xaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)
ax.yaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)
plt.legend(loc="upper right")

plt.savefig("Praesepe_Color_vs_Apparent_Magnitude.jpg", dpi=1200)

plt.show()
