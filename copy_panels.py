import os, sys, glob, shutil

import astropy.io.ascii as at

users = "Jessica","Jessica2","Jessica3"

# Create a local file for the inspection panels
new_dir = "./Panels/"
if os.path.exists(new_dir)==False:
    os.mkdir(new_dir)

# Open the final list of tidal tail targets
dbf = at.read("rnaas_dbf.csv")

# Put the garbage back, since that's what's in the filenames
garbage = dbf["Class"]=="Systematics"
dbf["Class"][garbage] = "Garbage"

# Panel directory
panel_dir = os.path.expanduser("~/Google Drive/Shared drives/DouglasGroup/tess_check/Praesepe_tails/Panels/")
if os.path.exists(panel_dir)==False:
    print("directory not found")
    sys.exit(1)

for i in range(len(dbf)):
    dr2name = dbf["DR2Name"][i].replace("Gaia DR2 ","GaiaDR2_")
    # print(dr2name)

    all_files = glob.glob(f"{panel_dir}{dr2name}*png")
    # print(all_files)

    # If more than one file is found, check for the matching classification
    if len(all_files)>1:
        for rname in all_files:
            if dbf["Class"][i] in rname:
                fname = rname
                break

    elif len(all_files)==0:
        print("\nuh oh\n",dbf["DR2Name","Class","Quality"][i])

    else:
        fname = all_files[0]

    # print(dbf["DR2Name","Class","Quality"][i])
    # print(fname.split("/")[-1].replace("-User=Jessica",""),"\n")

    # Copy the desired file to the local directory
    new_fname = fname.split("/")[-1].replace("-User=Jessica","")
    shutil.copyfile(fname,os.path.join(new_dir,new_fname))

    # Finally, copy the panels for the three doubled stars
    # Gaia DR2 1093716552959714816
    fname = "GaiaDR2_1093716552959714816-User=Jessica3.png"
    shutil.copyfile(os.path.join(panel_dir,fname),
                    os.path.join(new_dir,fname.replace("User=Jessica3","Doubled")))


    # Gaia DR2 703692806193429248
    fname = "GaiaDR2_703692806193429248-User=Jessica3.png"
    shutil.copyfile(os.path.join(panel_dir,fname),
                    os.path.join(new_dir,fname.replace("User=Jessica3","Doubled")))


    # Gaia DR2 716094541439727104
    fname = "GaiaDR2_716094541439727104-User=Jessica3-Review=Possibility.png"
    shutil.copyfile(os.path.join(panel_dir,fname),
                    os.path.join(new_dir,"GaiaDR2_716094541439727104-Doubled.png"))
