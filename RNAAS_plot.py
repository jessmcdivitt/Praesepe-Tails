#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 12:40:05 2021

@author: jessica
"""

import astropy.io.ascii as at
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import join

#Join tables
t1=at.read("Praesepe_latest_AN.csv")
t1.rename_column("DR2_desig", "DR2Name")
t1.rename_column("D", "Distance")
t1["BP_RP_1"] = t1["BP"]-t1["RP"]
t1.rename_column("G", "Gmag_1")
t2=at.read("Cumulative_Praesepe_tails_table.csv")
t2.rename_column("BP_RP", "BP_RP_2")
t2.rename_column("Gmag", "Gmag_2")

t1["AbsGMag"] = t1["Gmag_1"] + 5 - 5*np.log10(t1["Distance"])

tab=join(t1, t2, keys="DR2Name")

gridspec_kw = {"width_ratios":[3.7,4.3]}
fig, axes = plt.subplots(1,2,sharex=True,figsize=(8,3.75),
                         gridspec_kw=gridspec_kw)

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
ax1.set_xlim(0.5, 3.25)
ax1.set_xlabel(r"$(G_{\rm BP} - G_{\rm RP})$",fontsize=11)
ax1.set_ylabel("Rotation Period (Days)",fontsize=11)
ax1.xaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)
ax1.yaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)

#Create adjusted outliers table
outlier_double=np.where((tab["BP_RP_2"]>1.2)&(tab["BP_RP_2"]<1.75)&(tab["Prot_Final"]<8)&(tab["Prot_Final"]>5)&(tab["Quality"] == 1))
print(tab[outlier_double])
tout=tab[outlier_double]
tout["Prot_Final_Adjusted"] = tout["Prot_Final"] + tout["Prot_Final"]

#Plot adjusted outliers
outliers=ax1.plot(tout["BP_RP_2"], tout["Prot_Final_Adjusted"], "*", 
                  markerfacecolor="#35b779", 
                  markeredgecolor="black", 
                  markersize=6, markeredgewidth=0.5, zorder=4, 
                  label=r'Doubled $P_{\rm rot}$')
ax1.legend(loc='upper left', fontsize=8)

#Create vertical lines to connect the original points to the adjusted ones
print(tout)
# ax1.vlines(x=[1.5656, 1.5072, 1.378], ymin=[6.408041748, 6.092199158, 6.046360285], 
#            ymax=[12.816083496, 12.184398316, 12.09272057], colors='k', 
#            linestyles='solid', zorder=2, linewidth=1.5)
ax1.vlines(x=tout["BP_RP_2"], ymin=tout["Prot_Final"], 
           ymax=tout["Prot_Final_Adjusted"], colors="#31688e",#'#440154', 
           linestyles='solid', zorder=2, linewidth=1)

#Create joined table for tails
# tab_again=join(t1, t2, keys="DR2Name")
t3=tab["DR2Name", "Quality", "Prot_Final", "BP_RP_2", "AbsGMag"]
at.write(t3,"Praesepe_tails_absolute_magnitude.csv", delimiter=",")
# print(t3.dtype)


#Pinpoint quality stars
good=np.where(t3["Quality"] == 1)

#Create a refined table
t4=t3[(t3["Quality"] == 1)]

# Plot central cluster
ax2 = axes[1]
cluster_cmd=ax2.plot(t1["BP_RP_1"], t1["AbsGMag"], ".", c="darkgray", 
                     markersize=2, zorder=1, label="Central Cluster")


#Plot tails
x=t4["BP_RP_2"]
y=t4["AbsGMag"]
colors=t4["Prot_Final"]


sc = ax2.scatter(x,y,s=36, c=colors, zorder=2, marker='*', edgecolors='black', 
                 linewidths=0.5, label="Tails")
plt.colorbar(sc,label='Rotation Period')

#Adjust plot
ax2.set_xlabel(r"$(G_{\rm BP} - G_{\rm RP})$",fontsize=11)
ax2.set_ylabel(r"$M_G$",fontsize=11)
ax2.set_ylim(16,-1)
# ax2.set_title("Praesepe")
ax2.xaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)
ax2.yaxis.grid(color='lightgray', linestyle='solid', alpha=0.25)
# ax2.legend(loc="upper right")

ax1.tick_params(labelsize=8)
ax2.tick_params(labelsize=8)

plt.savefig("rnaas_fig.png",dpi=600,bbox_inches="tight")


plt.show()
