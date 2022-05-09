#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 12:40:05 2021

@author: jessica
"""

import astropy.io.ascii as at
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table,join

#Join tables
t1=at.read("Praesepe_latest_AN.csv")
t1.rename_column("DR2_desig", "DR2Name")
t1.rename_column("D", "Distance")
t1["BP_RP_1"] = t1["BP"]-t1["RP"]
t1.rename_column("G", "Gmag_1")
t2=at.read("Cumulative_Praesepe_tails_table.csv")
t2.rename_column("BP_RP", "BP_RP_2")
t2.rename_column("Gmag", "Gmag_2")

t1["Magnitude"] = t1["Gmag_1"] + 5 - 5*np.log10(t1["Distance"])

tab=join(t1, t2, keys="DR2Name")

fig, axes = plt.subplots(1,2,sharex=True,figsize=(8,3.75))

ax1 = axes[0]
#Create Scatterplots
cluster=ax1.plot(tab["BP_RP_1"], tab["Prot_1"], ".", 
                 markerfacecolor="darkgray", markeredgecolor='darkgray', 
                 markersize=2, zorder=1, label='Central Cluster')
tails=ax1.plot(tab["BP_RP_2"], tab["Prot_Final"], "*", 
               markerfacecolor="k", markeredgecolor="black", 
               markersize=6, markeredgewidth=0.5, zorder=3, 
               label=r'Candidates with $P_{\rm rot}$')

#Adjust plot
ax1.set_ylim(0.01, 30)
ax1.set_xlim(0.5, 3.7)
ax1.set_xlabel(r"$(G_{\rm BP} - G_{\rm RP})$")
ax1.set_ylabel("Rotation Period (Days)")
# ax1.set_title("Praesepe Rotation vs Color Plot")
# ax1.legend(loc='upper left')
# ax.yaxis.grid(color='gray', linestyle='dashed')

#Create adjusted outliers table
outlier_double=np.where((tab["BP_RP_2"]>1.2)&(tab["BP_RP_2"]<1.75)&(tab["Prot_Final"]<8)&(tab["Prot_Final"]>5)&(tab["Quality"] == 1))
print(tab[outlier_double])
table2=tab[outlier_double]
table2["Prot_Final_Adjusted"] = table2["Prot_Final"] + table2["Prot_Final"]
at.write(table2["DR2Name", "BP_RP_2", "Prot_Final", "Prot_Final_Adjusted"], 
         "Praesepe_Outliers_Adjusted.csv", delimiter=",")

#Create plot from table
tout=at.read("Praesepe_Outliers_Adjusted.csv")
outliers=ax1.plot(tout["BP_RP_2"], tout["Prot_Final_Adjusted"], "*", 
                  markerfacecolor="#35b779", markeredgecolor="black", 
                  markersize=6, markeredgewidth=0.5, zorder=4, 
                  label=r'Doubled $P_{\rm rot}$')
ax1.legend(loc='upper left', fontsize=8)

#Create vertical lines to connect the original points to the adjusted ones
print(tout)
ax1.vlines(x=[1.5656, 1.5072, 1.378], ymin=[6.408041748, 6.092199158, 6.046360285], 
           ymax=[12.816083496, 12.184398316, 12.09272057], colors='k', 
           linestyles='solid', zorder=2, linewidth=1.5)


# plt.savefig("Praesepe_Rotation_vs_Color.jpg", dpi=1200)

# plt.show()

#Identify stars that may be binary candidates
gap1=np.where((tab["BP_RP_2"]>1.2)&(tab["BP_RP_2"]<1.75)&(tab["Prot_Final"]<8)&(tab["Quality"] == 1))
print(tab[gap1])
gap2=np.where((tab["BP_RP_2"]>2.1)&(tab["BP_RP_2"]<2.4)&(tab["Prot_Final"]>6.5)&(tab["Prot_Final"]<9))
print(tab[gap2])

#Create a list of the possible binary candidates
f=open("Possible_binary_candidates_1.txt", "w")
for star in tab["DR2Name"][gap1]:
    f.write(f"{star},")
f.close()
f=open("Possible_binary_candidates_2.txt", "w")
for star in tab["DR2Name"][gap2]:
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
for star in tab[gap1]:
    binary1=np.where(tab["Eclipsing_Binary"] >0)
print(tab[binary1])
for star in tab[gap2]:
    binary2=np.where(tab["Eclipsing_Binary"] >0)
print(tab[binary2])

#Create joined table for tails
# tab_again=join(t1, t2, keys="DR2Name")
at.write(tab["DR2Name", "Quality", "Prot_Final", "BP_RP_2", "Magnitude"], 
         "Praesepe_tails_absolute_magnitude.csv", delimiter=",")
t3=at.read("Praesepe_tails_absolute_magnitude.csv")
print(t3.dtype)

#Pinpoint quality stars
good=np.where(t3["Quality"] == 1)

#Create a refined table
t4=t3[(t3["Quality"] == 1)]

# Plot central cluster
ax2 = axes[1]
cluster_cmd=ax2.plot(t1["BP_RP_1"], t1["Magnitude"], ".", c="darkgray", 
                     markersize=2, zorder=1, label="Central Cluster")


#Plot tails
x=t4["BP_RP_2"]
y=t4["Magnitude"]
colors=t4["Prot_Final"]


sc = ax2.scatter(x,y,s=36, c=colors, zorder=2, marker='*', edgecolors='black', 
                 linewidths=0.5, label="Tails")
plt.colorbar(sc,label='Rotation Period')

#Adjust plot
ax2.set_xlabel(r"$(G_{\rm BP} - G_{\rm RP})$")
ax2.set_ylabel("Absolute Magnitude")
ax2.set_ylim(16,-1)
# ax2.set_title("Praesepe")
ax2.xaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)
ax2.yaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)
# ax2.legend(loc="upper right")

plt.savefig("rnaas_fig.png",dpi=600,bbox_inches="tight")


plt.show()
