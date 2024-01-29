# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:20:05 2023

@author: MvEng
"""
import subprocess
import os
import glob
os.system('cmd /k "cd C:\your-directory\Scripts\pre-processing files"')
import shutil


os.chdir("C:\\your-directory\\Scripts\\pre-processing files\\")

#Add loop to run through all files
for i in glob.glob('C:\your-directory\\Scripts\\pre-processing files\\*.PBF',recursive=True):
    file = i
    head, tail = os.path.split(file)
    size = len(tail)
    tail = tail [:size - 8]

#setting up variables for converting the files
    convert_o5m= 'osmconvert ' +tail+ '.osm.pbf -o=o5m_subprocess.o5m'

    filter_roads_big = 'osmfilter o5m_subprocess.o5m --keep="highway=primary =trunk =motorway =secondary =tertiary =unclassified =residential =motorway_link =trunk_link =primary_link =secondary_link =tertiary_link =living_street =service =busway =escape" -o=highways.o5m'
    filter_roads_detail = 'osmfilter o5m_subprocess.o5m --keep="highway=track =path =footway =pedestrian =steps =cycleway =bridleway" -o=detailroads.o5m '
    filter_other = 'osmfilter o5m_subprocess.o5m --keep=railway=* --keep=public_transport=* --keep=barrier=* --keep=military=* --keep=aerialway=* --keep=aeroway=* --keep=telecom=* --keep=power=* --keep=man_made=* --keep=utility=* --keep=amenity=* -o=other.o5m '    
    filter_water = 'osmfilter o5m_subprocess.o5m --keep=water=* --keep=waterway=* --keep=man_made=* -o=water.o5m '    

    convert_to_roads = 'osmconvert highways.o5m -o='+tail+'-roads.osm.pbf'
    convert_to_detail = 'osmconvert detailroads.o5m -o='+tail+'-detailroads.osm.pbf'
    convert_to_other = 'osmconvert other.o5m -o='+tail+'-other.osm.pbf'
    convert_to_water = 'osmconvert water.o5m -o='+tail+'-water.osm.pbf'    

#converting and filtering files for roads
    subprocess.check_call(convert_o5m, shell=True)
    subprocess.check_call(filter_roads_big, shell=True)
    subprocess.check_call(filter_roads_detail, shell=True)
    subprocess.check_call(filter_other, shell=True)    
    subprocess.check_call(filter_water, shell=True)
   
    subprocess.check_call(convert_to_roads, shell=True)
    subprocess.check_call(convert_to_detail, shell=True)    
    subprocess.check_call(convert_to_other, shell=True)    
    subprocess.check_call(convert_to_water, shell=True)
     
 #Removing unused files   
    os.remove('C:\your-directory\\Scripts\\pre-processing files\\o5m_subprocess.o5m')
    os.remove('C:\your-directory\\Scripts\\pre-processing files\\highways.o5m')
    os.remove('C:\your-directory\\Scripts\\pre-processing files\\detailroads.o5m')    
    os.remove('C:\your-directory\\Scripts\\pre-processing files\\other.o5m')    
    os.remove('C:\your-directory\\Scripts\\pre-processing files\\water.o5m')

#Move files to correct folder    
    shutil.move('C:\your-directory\\Scripts\\pre-processing files\\'+tail+'-roads.osm.pbf', 'C:\Academic\\Scripts\\pre-processing files\\Filtered-Roads\\'+tail+'.osm.pbf')
    shutil.move('C:\your-directory\\Scripts\\pre-processing files\\'+tail+'-detailroads.osm.pbf', 'C:\Academic\\Scripts\\pre-processing files\\Detailed-Roads\\'+tail+'.osm.pbf')
    shutil.move('C:\your-directory\\Scripts\\pre-processing files\\'+tail+'-other.osm.pbf', 'C:\Academic\\Scripts\\pre-processing files\\Other\\'+tail+'.osm.pbf')
    shutil.move('C:\your-directory\\Scripts\\pre-processing files\\'+tail+'-water.osm.pbf', 'C:\Academic\\Scripts\\pre-processing files\\Water\\'+tail+'.osm.pbf')

#Remove original .osm.pbf file. Comment out if you want to keep the original file
    os.remove('C:\your-directory\\Scripts\\pre-processing files\\'+tail+'.osm.pbf')
