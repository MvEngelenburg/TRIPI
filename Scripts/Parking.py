# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 11:18:32 2023

@author: MvEng
"""

#LOAD NECESSARY MODULES 
import pandas as pd
import glob
import os
from pyrosm import get_data
from pyrosm import OSM


#ADD FOLDER OF PREFERENCE FOR RESULTS HERE
os.chdir("C:\your-directory\Scripts\example-results")

#OPEN LOG FOR TRACKING THE DIFFERENT RUNS. AND EASY ERROR PROCESSING
import time

t = time.localtime()
timestamp = time.strftime('%b-%d-%Y_%H%M', t)
f = open("log-parking"+timestamp+".txt", "a")

#OPEN DATAFRAMES OF INTEREST
Parking_spots = pd.DataFrame(columns=('parking','count','country'))
Parking_surface = pd.DataFrame(columns=('parking','surface','count','country'))
Parking_capacity = pd.DataFrame(columns=('parking','count','capacity','country'))

Parking_Area = pd.DataFrame(columns=('parking','area','country'))
Parking_Surface_Area = pd.DataFrame(columns=('parking','surface','area','country'))

#MAIN LOOP FOR RUNNING THROUGH THE DIFFERENT .osm.pbf FILES
for i in glob.glob('C:\your-directory\Scripts\example-other\\**\\*.PBF',recursive=True):
    try:
        file = i
        head, tail = os.path.split(file)
        size = len(tail)
        country = tail [:size - 15]
        fp = get_data(country,directory="C:\your-directory\Scripts\example-informal")
        osm = OSM(fp)
                
        #Parking elements
        parking = osm.get_data_by_custom_criteria(custom_filter={'amenity':True},filter_type="keep",keep_nodes=True,keep_ways=True, keep_relations=True,extra_attributes=["capacity","surface"])
        parking = parking[parking.parking.notnull()]
        
        #With the parking elements the crs needs to be included to accurately calculate the area.
        # Some examples for larger runs - areas to be looping through minimizing inaccuracies 
        # Europe projection - 3035
        # South and central america
        # EPSG:31974
        # SIRGAS 2000 / UTM zone 20N
        # North America
        # EPSG:26920
        # NAD83 / UTM zone 20N
        # Oceania (Australia biased)
        # EPSG:7859
        # GDA2020 / MGA zone 59
        # Africa (Nigeria basis)
        # EPSG:26393
        # Minna / Nigeria East Belt
        # EPSG:7755
        # WGS 84 / India NSF LCC
        # India, afghanistan, pakistan, bangladesh, nepal, bhutan, myanmar, sri lanka
        # EPSG:5636
        # TUREF / LAEA Europe
        # armenia, azerbaijan, syria 
        # EPSG:6984
        # Israeli Grid 05
        # Israel, palestine, jordan, lebanon
        # EPSG:24047
        # Indian 1975 / UTM zone 47N
        # Thailand, laos, cambodia, vietnam, malaysia
        # EPSG:5330
        # Batavia (Jakarta) / NEIEZ
        # EPSG:2318
        # Ain el Abd / Aramco Lambert
        # GCC-states, yemen, oman, iraq, iran, 
        # EPSG:2545
        # Pulkovo 1942 / 3-degree Gauss-Kruger zone 29
        # EPSG:3094
        # Tokyo / UTM zone 53N
        # Japan, North Korea, South Korea, Philipines
        # EPSG:4496
        # CGCS2000 / Gauss-Kruger zone 18
        # China, Mongolia, Taiwan

        parking = parking.to_crs(3035)        
        parking_area = parking.to_crs(3035)
        
        #We are interested in the parking Polygons to calculate the actual area for parking within a country
        parking_area = parking_area[parking_area.geometry.type != 'Point']
        parking_area ['area'] = parking_area['geometry'].area    

        parking = pd.DataFrame.from_dict(parking)
        parking_area = pd.DataFrame.from_dict(parking_area)

        #Functions for the actual extraction of data from the parking OSM information 
        def park():
            global parking_points
            parking_points = parking.groupby('parking').size().to_frame('count').reset_index()
            parking_points['country'] = country
    
        def parking_paving():
            global parking_surface
            parking_surface = parking.groupby(['parking','surface']).size().to_frame('count').reset_index()
            parking_surface['country'] = country                        

        def parking_cap():
            global parking_capacity
            parking_capacity = parking.groupby(['parking','capacity']).size().to_frame('count').reset_index()
            parking_capacity['country'] = country                 

        def parking_space():
            global parking_by_area, parking_by_surfacearea
            parking_by_area = parking_area.groupby('parking')['area'].sum().reset_index()
            parking_by_surfacearea = parking_area.groupby(['parking','surface'])['area'].sum().reset_index()

            parking_by_area['country'] = country   
            parking_by_surfacearea['country'] = country   

        #Try through all data and countries to extract as much data as possible while keeping the loop going and logging all missing data.
        try:
            park()
            Parking_spots = pd.concat([Parking_spots,parking_points])  
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing parking'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        
        try:
            parking_paving()
            Parking_surface = pd.concat([Parking_surface,parking_surface])  
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing parking pavement'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        
        try:
            parking_cap()
            Parking_capacity = pd.concat([Parking_capacity,parking_capacity]) 
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing parking capacity'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        try:
            parking_space()
            Parking_Area = pd.concat([Parking_Area,parking_by_area])
            Parking_Surface_Area = pd.concat([Parking_Surface_Area,parking_by_surfacearea])
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing parking space'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass

    #Log for when a country has absolutely no data on parking    
    except Exception as Argument:
        f.write(str(country))
        f.write(str('\n'))       
        f.write(str(Argument))
        f.write(str('\n\n'))
        pass

f.close()
    
#Export the raw data from OSM to Excel
with pd.ExcelWriter('Parking'+timestamp+'.xlsx') as writer:
    Parking_spots.to_excel(writer, sheet_name='Parking')
    Parking_surface.to_excel(writer, sheet_name='Surface')
    Parking_capacity.to_excel(writer, sheet_name='Capacity')
    Parking_Area.to_excel(writer, sheet_name='Area')
    Parking_Surface_Area.to_excel(writer, sheet_name='Area by surface type')    