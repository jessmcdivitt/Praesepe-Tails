#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 14:04:38 2021

@author: jessica
"""

import astropy.io.ascii as at
import numpy as np
import matplotlib.pyplot as plt

from astropy.table import Table,join

t1=at.read("Praesepe_tails_Jessica.csv")
t2=at.read("Praesepe_tails_Jessica2.csv")
tab=join(t1, t2, keys='DR2Name')

#Investigating negative periods
bad=np.where((tab["Prot_Final_1"]<-1)&(tab["Prot_Final_1"]>-20))[0] 
print(tab[bad])

#Finding where the two different rotation periods are different
diff=np.where(tab["Prot_Final_1"] != tab["Prot_Final_2"])[0]
print(tab[diff])

#Refining the table results to exclude flat and garbage stars
diff=np.where((tab["Prot_Final_1"] != tab["Prot_Final_2"])&(tab["Prot_Final_1"]>-99)&(tab["Prot_Final_1"]<99))[0]
print(tab[diff])

#Creating a text file with a list of these names
f=open("Check_ids.txt","w")
for gaia_id in tab["DR2Name"][diff]:
    f.write(f"{gaia_id},")
f.close()

#t3 has all of the corrected rotation periods. They were updated in the first google sheet to avoid having three separate tables.
t3=at.read("Praesepe_tails_Jessica_update2.csv")
t2=at.read("Praesepe_tails_Jessica2.csv")
table=join(t3, t2, keys='DR2Name')

table.rename_column("Prot_Final_1", "Prot_Final")
table["Double"] = table["Single_Double_1"]+table["Single_Double_2"]
table["Multi"] = table["Multi_1"]+table["Multi_2"]
table["Eclipsing_Binary"] = table["Eclipsing_Binary_1"]+table["Eclipsing_Binary_2"]
table["Contaminated"] = table["Contaminated_1"]+table["Contaminated_2"]
table["Spot_Evolution"] = table["Spot_Evolution_1"]+table["Spot_Evolution_2"]
table["Flares"] = table["Flares_1"]+table["Flares_2"]

#Find where the different class designations are unequal
np.where(table["Class_1"] != table["Class_2"])
#Output:  8,   16,   19,   34,   40,   49,   64,  113,  128,  129,  210 1582, 1616, 1631, 1696, 1705]),)
diff2=np.where(table["Class_1"] != table["Class_2"])
print(table[diff2])
for star in diff2:
    print(table["DR2Name", "Class_1", "Class_2"][diff2])
    
#Create a text file to find this list of names 
f=open("Check_diff2_quality", "w")
for gaia_id in tab["DR2Name"][diff2]:
    f.write(f"{gaia_id},")
f.close()

#Rename column with corrected classifications
table.rename_column("Class_1", "Class")

#Create a table that combines the Targets list with the joined tables
t4=at.read("Praesepe_tails_Targets.csv")
table2=join(table, t4, keys='DR2Name')

#Make the notes column from the first user sheet the primary notes column
del table2["Notes"]
table2.rename_column("Notes_1", "Notes")

#When I updated the class, I had forgoteen to update the quality columns; the update is below.
diff3=np.where(table2["Quality_1"] != table2["Quality_2"])
print(table2[diff3])
#All of the stars in this table had final rotation periods of -99; they were all garbage. 
#Quality differences either resulted from a garbage/flat disagreement, or had already been remedied in the classification step.
table2.rename_column('Quality_1', 'Quality')

#Create a new table with all of the correct columns
at.write(table2['DR2Name', 'Prot_Final', 'Class', 'Quality', 'Double', 'Multi', 'Eclipsing_Binary', 'Contaminated', 'Spot_Evolution', 'Flares', 'Notes', 'RA', 'Dec', 'Gmag', 'BP_RP', 'Prot', 'Prot_LS', 'Power_LS', 'TESS_Data'], "Cumulative_Praesepe_tails_table.csv", delimiter=",")


