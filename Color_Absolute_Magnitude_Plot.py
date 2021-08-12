#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 13:38:39 2021

@author: jessica
"""

import astropy.io.ascii as at
import numpy as np
import matplotlib.pyplot as plt

t1=at.read("Praesepe_latest_AN.csv")
t1.rename_column("DR2_desig", "DR2Name")
t1.rename_column("D", "Distance")
t1["BP_RP_1"] = t1["BP"]-t1["RP"]
t1.rename_column("G", "Gmag_1")
t2=at.read("Cumulative_Praesepe_tails_table.csv")
t2.rename_column("BP_RP", "BP_RP_2")
t2.rename_column("Gmag", "Gmag_2")
from astropy.table import Table,join
table=join(t1, t2, keys="DR2Name")

fig,ax = plt.subplots()

#Create plot for cluster
t1["Magnitude"] = t1["Gmag_1"] + 5 - 5*np.log10(t1["Distance"])
cluster=ax.plot(t1["BP_RP_1"], t1["Magnitude"], ".", c="darkgray", markersize="5", zorder=1, label="Central Cluster")

#Create joined table for tails
from astropy.table import Table,join
table=join(t1, t2, keys="DR2Name")
at.write(table["DR2Name", "Quality", "Prot_Final", "BP_RP_2", "Magnitude"], "Praesepe_tails_absolute_magnitude.csv", delimiter=",")
t3=at.read("Praesepe_tails_absolute_magnitude.csv")

#Pinpoint quality stars
good=np.where(t3["Quality"] == 1)

#Create a refined table
t4=t3[(t3["Quality"] == 1)]

#Plot tails
x=t4["BP_RP_2"]
y=t4["Magnitude"]
colors=t4["Prot_Final"]

plt.scatter(x,y,s=75, c=colors, zorder=2, marker='*', edgecolors='black', linewidths=0.5, label="Tails")
plt.colorbar(label='Rotation Period')

#Adjust plot
ax.set_xlabel("BP-RP")
ax.set_ylabel("Absolute Magnitude")
ax.set_ylim(16,-1)
ax.set_title("Praesepe")
ax.xaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)
ax.yaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)
plt.legend(loc="upper right")

plt.savefig("Praesepe_Color_vs_Absolute_Magnitude.jpg", dpi=1200)

plt.show()