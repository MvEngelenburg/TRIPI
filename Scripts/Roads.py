# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 14:38:05 2022

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
f = open("log-roads"+timestamp+".txt", "a")


#OPEN DATAFRAMES OF INTEREST
Roads = pd.DataFrame(columns=('highway','length','country')) 
Paving_by_type =pd.DataFrame(columns=('highway','surface','length','country'))
Tunnels =pd.DataFrame(columns=('highway','tunnel','length','country'))
Bridges =pd.DataFrame(columns=('highway','bridge','length','country'))
Width = pd.DataFrame(columns=('highway','width','length','country'))
Lanes = pd.DataFrame(columns=('highway','lanes','length', 'country'))
Lit = pd.DataFrame(columns=('highway','lit','length', 'country'))
Most_detailed_sample = pd.DataFrame(columns=('highway','width', 'lanes','length','country'))
PedBic = pd.DataFrame(columns=('highway', 'bicycle','cycleway', 'foot','length','country'))
Service = pd.DataFrame(columns=( 'service','length', 'country'))
Road_Quality =pd.DataFrame(columns=('highway', 'smoothness','surface', 'length','country'))

Bridge_type2 = pd.DataFrame(columns=('highway', 'bridge:structure','length', 'country'))

#MAIN LOOP FOR RUNNING THROUGH THE DIFFERENT .osm.pbf FILES
for i in glob.glob('C:\your-directory\Scripts\example-other\\**\\*.PBF',recursive=True):
    try:
        file = i
        head, tail = os.path.split(file)
        size = len(tail)
        #Proper file name format D:\directory\placename-latest.osm.pbf for -15 or D:\directory\placename.osm.pbf for -8
        country = tail [:size - 15]
        fp = get_data(country,directory="C:\your-directory\Scripts\example-other")
        osm = OSM(fp)

        #load in roads in dataframe
        highway= osm.get_network(network_type='driving',extra_attributes=['bridge:structure'])

        #filter to only take line elements. Removing points and polygons
        highway["geometry_types"]=highway.geom_type
        highway = highway.loc[highway["geometry_types"].isin(["LineString","MultiLineString"])]
    
        #convert road length from meters into kilometers
        highway["length"] = highway["length"]/1000
    
        #Calculate road types, paving and paving by road type
        
        #paved_total =  highway.groupby('surface')['length'].sum().reset_index()
        road_type =  highway.groupby('highway')['length'].sum().reset_index()
        services = highway.groupby(['service'])['length'].sum().reset_index()

        #Apply country name to column      
        road_type['country'] = country
        services ['country'] = country
   
        #Define a function for all different variables to be run individually. In order to extract as much information as possible without running into errors when a country has missing information
        def overpass():
            global bridges_road_type
            bridges_road_type = highway.groupby(['highway','bridge'])['length'].sum().reset_index()            
            bridges_road_type ['country'] = country            
        
        def walkbike():
            global ped_bik
            ped_bik = highway.groupby(['highway','bicycle','cycleway','foot'])['length'].sum().reset_index()
            ped_bik ['country'] = country                        
            
        def light():
            global lit_by_road_type
            lit_by_road_type = highway.groupby(['highway', 'lit'])['length'].sum().reset_index()
            lit_by_road_type ['country'] = country            
        
        def wide():
            global width_by_road_type
            width_by_road_type = highway.groupby(['highway','width'])['length'].sum().reset_index()            
            width_by_road_type ['country'] = country            

        def paving():
            global paved_by_road_type
            paved_by_road_type =  highway.groupby(['highway','surface'])['length'].sum().reset_index()
            paved_by_road_type['country'] = country            
            
        def lane():
            global lanes_by_road_type
            lanes_by_road_type = highway.groupby(['highway', 'lanes'])['length'].sum().reset_index()            
            lanes_by_road_type ['country'] = country            
        
        def tunnel_country():
            global tunnels_by_road_type
            tunnels_by_road_type = highway.groupby(['highway','tunnel'])['length'].sum().reset_index()            
            tunnels_by_road_type ['country'] = country                
        
        def path_bridges():
            global road_bridges_type1
            road_bridges = highway[highway.bridge.notnull()]
            road_bridges_type1 = road_bridges.groupby(['highway','bridge:structure'])['length'].sum().reset_index()
            road_bridges_type1 ['country'] = country

        def surface_area():
            global detailed_by_road_type
            detailed_by_road_type = highway.groupby(['highway','width','lanes'])['length'].sum().reset_index()
            detailed_by_road_type ['country'] = country            

        def quality():
            global roads_quality
            roads_quality =highway.groupby(['highway','smoothness','surface'])['length'].sum().reset_index()
            roads_quality ['country'] = country                         

        #Each function is run within a try function because not all countries have data on all elements. All missing elements are recorded in the log file
        try:
            overpass()
            Bridges = pd.concat([Bridges,bridges_road_type])         
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing bridges'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        try:
            walkbike()
            PedBic = pd.concat([PedBic,ped_bik])         
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing walking cycling'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        try:
            light()
            Lit = pd.concat([Lit,lit_by_road_type])    
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing Lighting'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        try:
            wide()
            Width = pd.concat([Width,width_by_road_type])           
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing width'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        try:
            paving()
            Paving_by_type = pd.concat([Paving_by_type,paved_by_road_type])        
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing surface'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass

        try:
            lane()
            Lanes = pd.concat([Lanes,lanes_by_road_type])           
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing lanes'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass

        try:
            surface_area()
            Most_detailed_sample = pd.concat([Most_detailed_sample,detailed_by_road_type])            
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing surface area'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        
        try:
            quality()
            Road_Quality = pd.concat([Road_Quality,roads_quality])            
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing road quality'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        
        try:
            tunnel_country()
            Tunnels = pd.concat([Tunnels,tunnels_by_road_type])           
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing tunnels'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        
        try: #ERROR - not including all bridges - 
            path_bridges()
            Bridge_type2 = pd.concat([Bridge_type2,road_bridges_type1])          
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing bridge types'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass

        #Append road lengths and types to global Roads dataframes
        Roads = pd.concat([Roads,road_type])
        Service = pd.concat([Service,services])
        
#For countries with no data - and exception is given, but the run is continued. The log file is to identify which countries can't be run
    except Exception as Argument:
        f.write(str(country))
        f.write(str('\n'))       
        f.write(str(Argument))
        f.write(str('\n\n'))
        pass

f.close()

#Export all the raw data extracts from OSM to Excel
with pd.ExcelWriter('RoadNetwork'+timestamp+'.xlsx') as writer:  
    Roads.to_excel(writer, sheet_name='Roads')
    Paving_by_type.to_excel(writer, sheet_name='Paving')
    Width.to_excel(writer, sheet_name='Width')    
    Tunnels.to_excel(writer, sheet_name='Tunnels')    
    Bridges.to_excel(writer, sheet_name='Bridges')
    Lanes.to_excel(writer,sheet_name='Lanes')
    Lit.to_excel(writer,sheet_name='Lit')
    PedBic.to_excel(writer,sheet_name='PedBic')
    Service.to_excel(writer, sheet_name='Service roads')
    Road_Quality.to_excel(writer,sheet_name='Road Quality')    
    Most_detailed_sample.to_excel(writer, sheet_name='Area')   
    Bridge_type2.to_excel(writer,sheet_name='Bridge type')
 

