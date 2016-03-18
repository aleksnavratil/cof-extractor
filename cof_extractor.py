print "Welcome to the Columbia ET+L Lab CETR CoF Saver\nNow Loading Plotting Libraries"

import numpy
import os
import traceback
import Tkinter, tkFileDialog
import csv

def User_Chooses_Skiprows():
    User_Skiprow_Choice=18
    print "This program is presently configured to skip",User_Skiprow_Choice,"rows"
    print "This works well if you only textified step 2 of data on the CETR computer."
    tempvar=raw_input("If you want to skip some other number of rows, type it now. Otherwise, press enter.""")
    if tempvar=="":
            print "OK. Skipping 18 rows."
            return User_Skiprow_Choice
    try:
            User_Skiprow_Choice=int(tempvar)
            return User_Skiprow_Choice
    except Exception:
            print "\nThat wasn't a number. Try again.\n"
            return User_Chooses_Skiprows()


def Get_User_Target_Directory_Wish():
    print "Choose the folder that you want the average CoF's from."
    root = Tkinter.Tk()
    root.withdraw()
    user_target_directory_wish = tkFileDialog.askdirectory(parent=root,initialdir="/home/aleks/Documents/ETL Lab/Graphene/CETR/Wear Evolution Tests",title='Pick a folder.')
    return user_target_directory_wish

def Iterate_Over_Files(user_target_directory_wish):
    for directory, list_of_subdirectories, list_of_files in os.walk(user_target_directory_wish):
        for files in list_of_files:
            if files.endswith("6000s.csv"):                                    
                try:
                    Do_Calculations(directory, files)
                except Exception:
                     print "Dude something went wrong."
                     print traceback.format_exc()
                     pass

def Do_Calculations(directory_containing_data, datafile_name):
    data = Load_Values(directory_containing_data, datafile_name)
    time_data = data[0]
    cof_data = data[1]
    print len(cof_data)
    absolute_filename = directory_containing_data+os.path.sep+datafile_name##[0:-4]
    human_readable_test_id = os.path.split(os.path.dirname(directory_containing_data+os.path.sep+datafile_name))[1] ##this is a sneaky way of making "Lambda X%" appear in the .csv
    print "\nNow averaging",human_readable_test_id,"\n",absolute_filename
    average_cof = round(float(numpy.mean(cof_data)),3)
    std_error = numpy.std(cof_data)#/numpy.sqrt(len(cof_data))
    cofs_by_filename.append( (human_readable_test_id, average_cof,std_error) )

def Load_Values(directory_containing_data, datafile_name):
    data = numpy.loadtxt(directory_containing_data+os.path.sep+datafile_name, delimiter = ",", skiprows = skiprows, usecols = (0,1,10,12))
    time_values = data[:,2]
    manually_calculated_cof = abs(data[:,0]/data[:,1])
    return time_values, manually_calculated_cof

def Write_to_File(cofs_by_filename):
    file_to_write = "/home/aleks/Documents/ETL Lab/ETL Python/Average CoFs.csv"
    file = open(file_to_write, "wb")
    c = csv.writer(file, delimiter = ',')
    c.writerow(('Test ID', 'Average CoF','Standard Error'))                                            
    for row in cofs_by_filename:
        c.writerow(row)
    file.close()
    print "\nSuccessfully wrote to",file_to_write

if __name__ == "__main__":
    cofs_by_filename = list()
    skiprows = User_Chooses_Skiprows()
    user_target_directory_wish = Get_User_Target_Directory_Wish()                                   
    Iterate_Over_Files(user_target_directory_wish)
    Write_to_File(cofs_by_filename)
    
    
