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
f = open("log-rail"+timestamp+".txt", "a")



#OPEN DATAFRAMES OF INTEREST
Rails = pd.DataFrame(columns=('railway','length','country'))
Electrified = pd.DataFrame(columns=('railway','electrified','length','country'))
Rail_Tunnel = pd.DataFrame(columns=('railway','tunnel','country'))
Rail_Bridges = pd.DataFrame(columns=('railway','bridge','country'))
Rail_Stationary = pd.DataFrame(columns=('railway','count','country'))
Aban = pd.DataFrame(columns=('highway','length','country'))
Gauge =  pd.DataFrame(columns=('railway','gauge','length','country'))
Highspeed =  pd.DataFrame(columns=('railway','highspeed','length','country'))

#MAIN LOOP FOR RUNNING THROUGH THE DIFFERENT .osm.pbf FILES
for i in glob.glob('C:\your-directory\Scripts\example-other\\**\\*.PBF',recursive=True):
    try:
        file = i
        head, tail = os.path.split(file)
        size = len(tail)
        country = tail [:size - 15]
        fp = get_data(country,directory="C:\your-directory\Scripts\example-informal")
        osm = OSM(fp)

    #Open dic for rail lines and rail stationary objects
        rail_dic = osm.get_data_by_custom_criteria(custom_filter={'railway': True, 'public_transport ': True},filter_type="keep",keep_nodes=False,keep_ways=True, keep_relations=False,extra_attributes=['highspeed','electrified','bridge','tunnel','gauge','service','covered','embankment','highway','material'])
        rail_stat =  osm.get_data_by_custom_criteria(custom_filter={'railway': True},filter_type="keep",keep_nodes=True,keep_ways=False, keep_relations=False,extra_attributes=['building','crossing:barrier','crossing:bell','crossing:light','electrified'])   
        
        rail = osm.get_data_by_custom_criteria(custom_filter={'railway': True, 'public_transport ': True},filter_type="keep",keep_nodes=False,keep_ways=True, keep_relations=False,extra_attributes=['electrified','bridge','tunnel'])                            
    #remove polygons for rail lines 
        rail_dic = rail_dic[rail_dic.geometry.type != 'Polygon']

        #With the rail elements the crs needs to be included to accurately calculate the area.
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


    #calculate rail length
        rail_dic = rail_dic.to_crs(3035)
        rail_dic['length'] = rail_dic['geometry'].length

    #Filter station layer for points and polygons
        rail_stat = rail_stat[rail_stat.geometry.type != 'Linestring']
        rail_stat = rail_stat[rail_stat.geometry.type != 'Multilinestring']

    #transform into panda dataframe
        rail_dic = pd.DataFrame.from_dict(rail_dic)
        railstat_df = pd.DataFrame.from_dict(rail_stat)
    #convert to kilometers
        rail_dic["length"] = rail_dic["length"]/1000

    #type total
        rail_type = rail_dic.groupby('railway', dropna=False)['length'].sum().reset_index()
        railstat_point = railstat_df.groupby('railway').size().reset_index()
        railstat_point.columns = ['railway', 'count']

     

    #Create functions for running through the different elements in rail infrastructure that not every country have data on
    #Bridges, electrified, tunnels, abandoned, gauge
        def bridg():
            global brid
            brid =rail_dic.groupby(['railway','bridge'])['length'].sum().reset_index()            
            brid['country'] = country

        def elec():
            global electrified
            electrified = rail_dic.groupby(['railway','electrified'])['length'].sum().reset_index()  
            electrified['country'] = country  
            
        def underground():
            global tunn
            tunn = rail_dic.groupby(['railway','tunnel'])['length'].sum().reset_index()
            tunn['country'] = country                        

        def abandoned():
            global aban_trans
            aban_use = rail_dic.loc[rail_dic['railway'] =='abandoned']
            aban_trans = aban_use.groupby(['highway'])['length'].sum().reset_index()
            aban_trans['country'] = country

        def gauges():
            global gauge
            gauge = rail_dic.groupby(['railway','gauge'])['length'].sum().reset_index()
            gauge['country'] = country            

        def hs():
            global highspeed
            highspeed = rail_dic.groupby(['railway','highspeed'])['length'].sum().reset_index()
            highspeed ['country'] = country

        try:
            bridg()
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing bridges'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass

        try:
            elec()
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing electrified'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        
        try:
            underground()
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing tunnels'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass

        try:
            abandoned()
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing abandoned'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        try:
            gauges()
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing gauge'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass

        try:
            hs()
        except Exception as Argument:
            f.write(str(country))
            f.write(str('\n missing highspeed'))       
            f.write(str(Argument))
            f.write(str('\n\n'))
            pass
        
        
    #Add country to dataframe
        rail_type['country'] = country
        railstat_point['country'] = country
    
    #Append rail length and electrified to global Rail dataframes
        Rails = pd.concat([Rails,rail_type])
        Electrified = pd.concat([Electrified,electrified])
        Rail_Tunnel = pd.concat([Rail_Tunnel,tunn])
        Rail_Bridges = pd.concat([Rail_Bridges,brid])
        Rail_Stationary = pd.concat([Rail_Stationary,railstat_point])
        Aban = pd.concat([Aban,aban_trans])
        Gauge = pd.concat([Gauge,gauge])
        Highspeed = pd.concat([Highspeed,highspeed])

    
    #Log for when a country has absolutely no data on rail
    except Exception as Argument:
        f.write(str(country))
        f.write(str('\n'))       
        f.write(str(Argument))
        f.write(str('\n\n'))
        pass

f.close()

#Export the raw data from OSM to Excel
with pd.ExcelWriter('Railnetwork'+timestamp+'.xlsx') as writer:  
    Rails.to_excel(writer, sheet_name='Rails')
    Electrified.to_excel(writer, sheet_name='Electrified')
    Rail_Tunnel.to_excel(writer, sheet_name='Rail_Tunnel')    
    Rail_Bridges.to_excel(writer, sheet_name='Rail_Bridges')    
    Rail_Stationary.to_excel(writer, sheet_name='Rail_Stationary')
    Aban.to_excel(writer, sheet_name='Abandoned_to_road')
    Gauge.to_excel(writer, sheet_name='Gauge')
    Highspeed.to_excel(writer, sheet_name='Highspeed')
