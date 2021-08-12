#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 17:41:51 2021

@author: jessica
"""

import astropy.io.ascii as at
import matplotlib.pyplot as plt
import numpy as np

#Join tables
t1=at.read("Praesepe_latest_AN.csv")
t1.rename_column("DR2_desig", "DR2Name")
t1["BP_RP_1"]=t1["BP"]-t1["RP"]
t2=at.read("Cumulative_Praesepe_tails_table.csv")
t2.rename_column("BP_RP", "BP_RP_2")
from astropy.table import Table,join
table=join(t1, t2, keys='DR2Name')

fig, ax = plt.subplots()

#Create Scatterplots
cluster=ax.plot(table["BP_RP_1"], table["Prot_1"], ".", markerfacecolor="darkgray", markeredgecolor='darkgray', markersize=5, zorder=1, label='Central Cluster')
tails=ax.plot(table["BP_RP_2"], table["Prot_Final"], "*", markerfacecolor="#287D8EFF", markeredgecolor="black", markersize=10, markeredgewidth=0.5, zorder=3, label='Tails')

#Adjust plot
ax.set_ylim(0.01, 30)
ax.set_xlim(0.5, 3.7)
ax.set_xlabel("BP-RP")
ax.set_ylabel("Rotation Period (Days)")
ax.set_title("Praesepe")
ax.xaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)
ax.yaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)

#Create adjusted outliers table
outlier_double=np.where((table["BP_RP_2"]>1.2)&(table["BP_RP_2"]<1.75)&(table["Prot_Final"]<8)&(table["Prot_Final"]>5)&(table["Quality"] == 1))
print(table[outlier_double])
table2=table[outlier_double]
table2["Prot_Final_Adjusted"] = table2["Prot_Final"] + table2["Prot_Final"]
at.write(table2["DR2Name", "BP_RP_2", "Prot_Final", "Prot_Final_Adjusted"], "Praesepe_Outliers_Adjusted.csv", delimiter=",")

#Create plot from table
t3=at.read("Praesepe_Outliers_Adjusted.csv")
outliers=ax.plot(t3["BP_RP_2"], t3["Prot_Final_Adjusted"], "*", markerfacecolor="#440154FF", markeredgecolor="black", markersize=10, markeredgewidth=0.5, zorder=4, label='Adjusted Outliers')
plt.legend(loc='upper left', fontsize=8)

#Create vertical lines to connect the original points to the adjusted ones
print(t3)
plt.vlines(x=[1.5656, 1.5072, 1.378], ymin=[6.408041748, 6.092199158, 6.046360285], ymax=[12.816083496, 12.184398316, 12.09272057], colors='k', linestyles='solid', zorder=2, linewidth=3)

plt.savefig("Praesepe_Rotation_vs_Color_Outlier_Adjustment.jpg", dpi=1200)

plt.show()

