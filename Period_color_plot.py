#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 12:40:05 2021

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
cluster=ax.plot(table["BP_RP_1"], table["Prot_1"], ".", markerfacecolor="cyan", markeredgecolor="black", markersize=5, label='Central Cluster')
tails=ax.plot(table["BP_RP_2"], table["Prot_Final"], "*", markerfacecolor="orange", markeredgecolor="black", markersize=7, label='Tails')

#Adjust plot
ax.set_ylim(0.01, 30)
ax.set_xlim(0.5, 3.7)
ax.set_xlabel("BP-RP")
ax.set_ylabel("Rotation Period (Days)")
ax.set_title("Praesepe Rotation vs Color Plot")
plt.legend(loc='upper left')
ax.yaxis.grid(color='gray', linestyle='dashed')

plt.savefig("Praesepe_Rotation_vs_Color.jpg", dpi=1200)

plt.show()

#Identify stars that may be binary candidates
gap1=np.where((table["BP_RP_2"]>1.2)&(table["BP_RP_2"]<1.75)&(table["Prot_Final"]<8)&(table["Quality"] == 1))
print(table[gap1])
gap2=np.where((table["BP_RP_2"]>2.1)&(table["BP_RP_2"]<2.4)&(table["Prot_Final"]>6.5)&(table["Prot_Final"]<9))
print(table[gap2])

#Create a list of the possible binary candidates
f=open("Possible_binary_candidates_1.txt", "w")
for star in table["DR2Name"][gap1]:
    f.write(f"{star},")
f.close()
f=open("Possible_binary_candidates_2.txt", "w")
for star in table["DR2Name"][gap2]:
    f.write(f"{star},")
f.close()

#Combine previous text files
filenames=['Possible_binary_candidates_1.txt', 'Possible_binary_candidates_2.txt']
with open('Possible_binary_candidates', 'w') as outfile:
    for names in filenames:
        with open(names) as infile:
            outfile.write(infile.read())
        outfile.write("\n")
        
#Determine whether highlighted stars were labeled as possible eclipsing binaries
for star in table[gap1]:
    binary1=np.where(table["Eclipsing_Binary"] >0)
print(table[binary1])
for star in table[gap2]:
    binary2=np.where(table["Eclipsing_Binary"] >0)
print(table[binary2])

