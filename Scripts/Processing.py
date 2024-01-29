# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:51:17 2023

@author: MvEng
"""

# Import necessary libraries
import pandas as pd
from os import chdir

#ADD FOLDER OF PREFERENCE FOR RESULTS HERE
chdir('C:\your-directory\Processed-example')

# Define lists for country regions
IN = ['central-zone', 'eastern-zone', 'north-eastern-zone', 'northern-zone', 'southern-zone', 'western-zone']
INDO = ['java','kalimantan','maluku','nusa-tenggara','papua','sulawesi','sumatra']
JP = ['chubu', 'chugoku','hokkaido','kansai','kanto','kyushu','shikoku','tohoku']
RUS = ['central-fed-district','crimean-fed-district','far-eastern-fed-district','north-caucasus-fed-district','northwestern-fed-district','siberian-fed-district','south-fed-district','ural-fed-district','volga-fed-district','kaliningrad']
FR = ['new-caledonia','azores','alsace','aquitaine','auvergne','basse-normandie','bourgogne','bretagne','centre','champagne-ardenne','corse','franche-comte','guadeloupe','guyane','haute-normandie','ile-de-france','languedoc-roussillon','limousin','lorraine','martinique','mayotte','midi-pyrenees','nord-pas-de-calais','pays-de-la-loire','picardie','poitou-charentes','provence-alpes-cote-d-azur','reunion','rhone-alpes']
GR = ['baden-wuerttemberg','bayern','berlin','brandenburg','bremen','hamburg','hessen','mecklenburg-vorpommern','niedersachsen','nordrhein-westfalen','rheinland-pfalz','saarland','sachsen','sachsen-anhalt','schleswig-holstein','thueringen']
GB = ['england','scotland','wales','bedfordshire','berkshire','bristol','buckinghamshire','cambridgeshire','cheshire','cornwall','cumbria','derbyshire','devon','dorset','durham','east-sussex','east-yorkshire-with-hull','essex','gloucestershire','greater-london','greater-manchester','hampshire','hertfordshire','herefordshire','isle-of-man','isle-of-wight','isle-of-wright','kent','lancashire','leicestershire','lincolnshire','merseyside','norfolk','north-yorkshire','northamptonshire','northumberland','nottinghamshire','oxfordshire','rutland','shropshire','somerset','south-yorkshire','staffordshire','suffolk','surrey','tyne-and-wear','warwickshire','west-midlands','west-sussex','west-yorkshire','wiltshire','worcestershire']
IT = ['centro','isole','nord-est','nord-ovest','sud']
NL = ['drenthe','flevoland','friesland','gelderland','groningen','limburg','noord-brabant','noord-holland','overijssel','utrecht','zeeland','zuid-holland']
PO = ['dolnoslaskie','kujawsko-pomorskie','lodzkie','lubelskie','lubuskie','malopolskie','mazowieckie','opolskie','podkarpackie','podlaskie','pomorskie','slaskie','swietokrzyskie','warminsko-mazurskie','wielkopolskie','zachodniopomorskie']
CN = ['alberta','british-columbia','manitoba','new-brunswick','newfoundland-and-labrador','northwest-territories','nova-scotia','nunavut','ontario','prince-edward-island','quebec','saskatchewan','yukon']
USA = ['alabama','alaska','arizona','arkansas','northern_california','southern_california','northern-california','southern-california','colorado','connecticut','delaware','district-of-columbia','florida','georgia-US','hawaii','idaho','illinois','indiana','iowa','kansas','kentucky','louisiana','maine','maryland','massachusetts','michigan','minnesota','mississippi','missouri','montana','nebraska','nevada','new-hampshire','new-jersey','new-mexico','new-york','north-carolina','north-dakota','ohio','oklahoma','oregon','pennsylvania','puerto-rico','rhode-island','south-carolina','south-dakota','tennessee','texas','us-virgin-islands','utah','vermont','virginia','washington','west-virginia','wisconsin','wyoming']
BR = ['centro-oeste','nordeste','norte','sudeste','sul']
ES = ['madrid','canary-islands']



#%% ROAD NETWORK

# Define the path to the Excel file containing road results
Road_Results = 'C:\your-directory\Output\Output-merged\Road.xlsx'

# Read the Excel file into a dictionary of DataFrames, each DataFrame corresponds to a sheet in the Excel file
Roads_dict  = pd.read_excel( Road_Results, sheet_name=None )

# Convert all regions to the country
for i in Roads_dict.values():     
    i.loc[i['country'].isin(IN),'country']='india'     
    i.loc[i['country'].isin(INDO),'country']='indonesia' 
    i.loc[i['country'].isin(JP),'country']='japan'    
    i.loc[i['country'].isin(RUS),'country']='russia' 
    i.loc[i['country'].isin(FR),'country']='france' 
    i.loc[i['country'].isin(GR),'country']='germany'    
    i.loc[i['country'].isin(GB),'country']='great-britain'     
    i.loc[i['country'].isin(IT),'country']='italy' 
    i.loc[i['country'].isin(NL),'country']='netherlands'    
    i.loc[i['country'].isin(PO),'country']='poland'     
    i.loc[i['country'].isin(CN),'country']='canada'     
    i.loc[i['country'].isin(USA),'country']='usa' 
    i.loc[i['country'].isin(BR),'country']='brazil' 
    i.loc[i['country'].isin(ES),'country']='spain' 


# Retrieve specific DataFrames from the dictionary
Roads = Roads_dict.get('Roads')
Paving = Roads_dict.get('Paving')
Paving_a = Roads_dict.get('Paving')
Width = Roads_dict.get('Width')
Tunnels = Roads_dict.get('Tunnels')
Bridges = Roads_dict.get('Bridges')
Lanes = Roads_dict.get('Lanes')
Lit = Roads_dict.get('Lit')
PedBic = Roads_dict.get('PedBic')
Service = Roads_dict.get('Service roads')
Road_Quality = Roads_dict.get('Road Quality')
SufaceWidth = Roads_dict.get('Area')
BridgeTypes = Roads_dict.get('Bridge type')

# Preprocess Width DataFrame
Width = Width[pd.to_numeric(Width['width'], errors='coerce').notnull()]
Width['width'] = Width['width'].astype(float)
#Remove roads wider than 200 meters, as there are none existing currently
Width = Width[Width['width'] < 200]  

#Proces lane data t only include numeric values
Lanes = Lanes[pd.to_numeric(Lanes['lanes'], errors='coerce').notnull()]
Lanes['lanes'] = Lanes['lanes'].astype(float)

#Same for rows that include both width and lanes
SufaceWidth = SufaceWidth[pd.to_numeric(SufaceWidth['width'], errors='coerce').notnull()]
SufaceWidth = SufaceWidth[pd.to_numeric(SufaceWidth['lanes'], errors='coerce').notnull()]
SufaceWidth['width'] = SufaceWidth['width'].astype(float)
SufaceWidth['lanes'] = SufaceWidth['lanes'].astype(float)
#Remove roads wider than 200 meters, as there are none existing currently
SufaceWidth = SufaceWidth[SufaceWidth['width'] < 200]  

Detail_width = SufaceWidth.drop('lanes', axis=1)
Detail_lane = SufaceWidth.drop('width', axis=1)

# Define functions for calculating weighted averages and apply them to relevant DataFrames
def weighted_average(Width, value, weight):
    val = Width[value]
    wt = Width[weight]
    return (val * wt).sum() / wt.sum()

def detail_wid (Detail_width, value, weight):
    val = Detail_width[value]
    wt = Detail_width[weight]
    return (val * wt).sum() / wt.sum()

def detail_lan (Detail_lane, value, weight):
    val = Detail_lane[value]
    wt = Detail_lane[weight]
    return (val * wt).sum() / wt.sum()

def weighted_lanes (Lanes, value, weight):
    val = Lanes[value]
    wt = Lanes[weight]
    return (val * wt).sum() / wt.sum()

# Calculate weighted average width and lanes for each highway-country combination
Width_weighted = Width.groupby(['highway','country']).apply(weighted_average,'width', 'length').reset_index()
Lane_weighted = Lanes.groupby(['highway','country']).apply(weighted_lanes,'lanes', 'length').reset_index()

# Calculate total length of road surface for each highway-country combination
Detail_length = SufaceWidth.groupby(['highway','country'])['length'].sum().reset_index()

# Calculate weighted average width and lanes separately, then merge the results
Detail_width_width = Detail_width.groupby(['highway','country']).apply(detail_wid,'width', 'length').reset_index()
Detail_lane_lane = Detail_lane.groupby(['highway','country']).apply(detail_lan,'lanes', 'length').reset_index()

# Merge calculated width and lanes into a single DataFrame
merged_wid = Detail_length.merge(Detail_width_width, on=['highway', 'country']).merge(Detail_lane_lane, on=['highway', 'country'])
merged_wid = merged_wid.rename(columns={"0_x": "width", "0_y": "lanes"})
merged_wid = merged_wid[merged_wid['highway'].isin(['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link'])]  

# Group and aggregate road lengths by highway and country
Roads =  Roads.groupby(['highway','country'])['length'].sum().reset_index()
Road_a = Roads.copy()

# Replacing road classifications with standardized categories
Road_a.replace({'motorway': 'highway', 'motorway_link': 'highway'}, inplace=True)
Road_a.replace({'trunk': 'primary', 'trunk_link': 'primary', 'primary': 'primary', 'primary_link': 'primary', 'secondary': 'secondary', 'secondary_link': 'secondary'}, inplace=True)
Road_a.replace({'tertiary': 'Tertiary', 'tertiary_link': 'Tertiary', 'unclassified': 'local', 'residential': 'local', 'living_street': 'local', 'busway': 'local', 'service': 'local'}, inplace=True)

Roads =  Roads.groupby(['highway','country'])['length'].sum().reset_index()
Road_a =  Road_a.groupby(['highway','country'])['length'].sum().reset_index()

# Group and aggregate service roads by type and country
Service = Service.groupby(['service','country'])['length'].sum().reset_index()

# Group and aggregate bridges by type, highway, and country, then filter out bridges with 'no' type
Bridges = Bridges.groupby(['highway','bridge','country'])['length'].sum().reset_index()
Bridges = Bridges.loc[Bridges['bridge'] != 'no']
Bridges_sum = Bridges.groupby(['highway','country'])['length'].sum().reset_index()        

# Group and aggregate pedestrian and bicycle paths by type, highway, and country
PedBic = PedBic.groupby(['highway','bicycle','cycleway','foot','country'])['length'].sum().reset_index()

# Group and aggregate lit roads by lit status, highway, and country
Lit = Lit.groupby(['highway', 'lit','country'])['length'].sum().reset_index()

# Group and aggregate road widths by highway and country
Width_attribute = Width.groupby(['highway','country'])['length'].sum().reset_index()

# Group and aggregate road lanes by highway and country
Lanes_attribute = Lanes.groupby(['highway','country'])['length'].sum().reset_index()          

# Group and aggregate paved areas by highway, surface type, and country
Paving =  Paving.groupby(['highway','surface','country'])['length'].sum().reset_index()

# Create a copy of the 'Paving' DataFrame
Paving_a = Paving.copy()

# Standardize road classifications in the DataFrame
Paving_a.replace({'motorway': 'highway', 'motorway_link': 'highway'}, inplace=True)
Paving_a.replace({'trunk': 'primary', 'trunk_link': 'primary', 'primary': 'primary', 'primary_link': 'primary', 'secondary': 'secondary', 'secondary_link': 'secondary'}, inplace=True)
Paving_a.replace({'tertiary': 'Tertiary', 'tertiary_link': 'Tertiary', 'unclassified': 'local', 'residential': 'local', 'living_street': 'local', 'busway': 'local', 'service': 'local'}, inplace=True)

# Standardize surface types in the DataFrame
Paving_a.replace({'asphalt': 'paved', 'paved': 'paved', 'concrete': 'paved', 'concrete:plates': 'paved', 'concrete:lanes': 'paved', 'asphalt;sand': 'paved', 'chipseal': 'paved'}, inplace=True)
Paving_a.replace({'gravel': 'unpaved - construction', 'compacted': 'unpaved - construction', 'fine_gravel': 'unpaved - construction', 'laterite': 'unpaved - construction', 'grass_paver': 'unpaved - construction'}, inplace=True)
Paving_a.replace({'paving_stones': 'paving_stone', 'cobblestone': 'stone', 'sett': 'stone', 'pebblestone': 'stone', 'unhewn_cobblestone': 'stone', 'cobblestone_flattened': 'stone'}, inplace=True)
Paving_a.replace({'brick': 'brick', 'bricks': 'brick'}, inplace=True)
Paving_a.replace({'ground': 'unpaved - unmanaged', 'dirt': 'unpaved - unmanaged', 'unpaved': 'unpaved - unmanaged', 'sand': 'unpaved - unmanaged', 'earth': 'unpaved - unmanaged', 'grass': 'unpaved - unmanaged', 'ice': 'unpaved - unmanaged', 'dirt/sand': 'unpaved - unmanaged', 'mud': 'unpaved - unmanaged', 'laterite': 'unpaved - unmanaged', 'soil': 'unpaved - unmanaged', 'salt': 'unpaved - unmanaged', 'clay': 'unpaved - unmanaged', 'karral': 'unpaved - unmanaged', 'ice_road': 'unpaved - unmanaged'}, inplace=True)

# Group and aggregate data by highway, surface type, and country in the 'Paving_a' DataFrame
Paving_a = Paving_a.groupby(['highway','surface','country'])['length'].sum().reset_index()

# Group and aggregate data
Paving_agg =  Paving.groupby(['surface','country'])['length'].sum().reset_index()
Lanes = Lanes.groupby(['highway', 'lanes','country'])['length'].sum().reset_index()            
Tunnels = Tunnels.groupby(['highway','tunnel','country'])['length'].sum().reset_index()            
BridgeTypes = BridgeTypes.groupby(['highway','bridge:structure','country'])['length'].sum().reset_index()
BridgeTypes3 = BridgeTypes.groupby(['highway','bridge:structure'])['length'].sum().reset_index()
Road_Smoothness =Road_Quality.groupby(['highway','smoothness','country'])['length'].sum().reset_index()
Road_Quality =Road_Quality.groupby(['highway','smoothness','surface','country'])['length'].sum().reset_index()

# Merge the 'Width_attribute' and 'Width_weighted' DataFrames and drop unnecessary columns
Widthh = pd.merge(Width_attribute, Width_weighted, left_index=True, right_index=True)
Widthh = Widthh.drop(Widthh.columns[[3, 4]],axis = 1)

# Rename columns and filter rows in the 'Widthh' DataFrame
Widthh = Widthh.rename(columns={"highway_x": "highway", "country_x": "country", 0 : "width"})
Widthh = Widthh[Widthh['highway'].isin(['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link'])]  

# Merge the 'Lanes_attribute' and 'Lane_weighted' DataFrames and drop unnecessary columns
Lane = pd.merge(Lanes_attribute, Lane_weighted, left_index=True, right_index=True)
Lane = Lane.drop(Lane.columns[[3, 4]],axis = 1)

# Rename columns and filter rows in the 'Lane' DataFrame
Lane = Lane.rename(columns={"highway_x": "highway", "country_x": "country", 0 : "lanes"})
Lane = Lane[Lane['highway'].isin(['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link'])]  


# Reshaping data frames using pivot
Roads = Roads.pivot(index='country', columns='highway', values='length')
Roads_b = Road_a.pivot(index='country', columns='highway', values='length')
Paving_b = Paving_a.pivot(index='country', columns=['highway','surface'], values='length')
Paving2 = Paving.pivot(index='country', columns=['highway','surface'], values='length')
Paving3 = Paving_agg.pivot(index='country', columns='surface', values='length')
Width = Widthh.pivot(index='country', columns=['highway','width'], values='length')
Lanes = Lane.pivot(index='country', columns=['highway','lanes'], values='length')
SufaceWidth = merged_wid.pivot(index='country', columns=['highway','width','lanes'], values='length')
Tunnels2 = Tunnels.pivot(index='country', columns=['highway','tunnel'], values='length')
Bridges2 = Bridges_sum.pivot(index='country', columns='highway', values='length')
Lit2 = Lit.pivot(index='country', columns=['highway','lit'], values='length')
PedBic2 = PedBic.pivot(index='country', columns=['highway','bicycle','cycleway','foot'], values='length')
Service2 = Service.pivot(index='country', columns=['service'], values='length')
Road_Quality2 = Road_Quality.pivot(index='country', columns=['highway','smoothness','surface'], values='length')
Road_Smoothness2 = Road_Smoothness.pivot(index='country', columns=['highway','smoothness'], values='length')
BridgeTypes2 = BridgeTypes.pivot(index='country', columns=['highway','bridge:structure'], values='length')
BridgeTypes4 = BridgeTypes3.pivot(index='highway', columns='bridge:structure', values='length')

Width_per_Type = Widthh.pivot(index='country', columns='highway', values='width')
Lanes_per_Type = Lane.pivot(index='country', columns='highway', values='lanes')

SufaceWidth_Type_Width = merged_wid.pivot(index='country', columns='highway', values='width')
SufaceWidth_Type_Lanes = merged_wid.pivot(index='country', columns='highway', values='lanes')


# Selecting specific columns for further processing
#Road types
Roads = Roads[['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link']]
Roads_c = Roads_b[['highway', 'primary','secondary','Tertiary','local']]

#Paving data
Paving_c = Paving_b.loc[:, (['highway', 'primary','secondary','Tertiary','local'],
              ['paved','unpaved - construction','paving_stone','stone','brick','wood','metal','unpaved - unmanaged'])]
Paving2 = Paving2.loc[:, (['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link'],
              ['unpaved','asphalt','paved','gravel','ground','dirt','compacted','concrete','sand','paving_stones','fine_gravel','cobblestone','sett','earth','concrete:plates','pebblestone','grass','ice','dirt/sand','concrete:lanes','mud','laterite','asphalt;sand','chipseal','unhewn_cobblestone','ice_road','soil','salt','cobblestone_flattened','grass_paver','wood','bricks','clay','karral','brick'])]
Paving3 = Paving3[['unpaved','asphalt','paved','gravel','ground','dirt','compacted','concrete','sand','paving_stones','fine_gravel','cobblestone','sett','earth','concrete:plates','pebblestone','grass','ice','dirt/sand','concrete:lanes','mud','laterite','asphalt;sand','chipseal','unhewn_cobblestone','ice_road','soil','salt','cobblestone_flattened','grass_paver','wood','bricks','clay','karral','brick']]
Paving4 = Paving2.copy() 

#Width data
Width = Width[['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link']]
Width_per_Type = Width_per_Type[['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link']]

#Lane data
Lanes = Lanes[['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link']]
Lanes.loc['Type_Total']= Lanes.sum(numeric_only=True, axis=0)
Lanes.loc[:,'Width_Total'] = Lanes.sum(numeric_only=True, axis=1)
Lanes_per_Type = Lanes_per_Type[['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link']]

#Tunnel daata
Tunnels2 = Tunnels2.loc [:, (['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link'], ['yes'])]
#Bridge data
Bridges2 = Bridges2[['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link']]
#Road lighting data
Lit2 = Lit2.loc [:, (['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link'], ['yes', 'no'])]
#pedestrian-cycle data
PedBic2 = PedBic2[['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link']]
#Service road information
Service2 = Service2[['driveway', 'parking_aisle','alley','drive-through','emergency_access','haul_road','agricultural','driveway2','resource extraction','hydrocarbons','bus','logging','busway','pipeline_access']]
#road quality indicators
Road_Quality2 = Road_Quality2.loc[:, (['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link'],
                        ['excellent','very_good','good','intermediate','poor','bad','very_bad','horrible','very_horrible','impassable']
             , ['unpaved','asphalt','paved','gravel','ground','dirt','compacted','concrete','sand','paving_stones','fine_gravel','cobblestone','sett','earth','concrete:plates','pebblestone','grass','ice','dirt/sand','concrete:lanes','mud','laterite','asphalt;sand','chipseal','unhewn_cobblestone','ice_road','soil','salt','cobblestone_flattened','grass_paver','wood','bricks','clay','karral','brick'])]
Road_Smoothness2 = Road_Smoothness2.loc[:, (['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link'],['excellent','very_good','good','intermediate','poor','bad','very_bad','horrible','very_horrible','impassable'])]
Smoothness_Total = Road_Smoothness.sum(numeric_only=True, axis=0)
Road_Smoothness_Stat = Road_Smoothness.describe()
#road area information
SufaceWidth = SufaceWidth[['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link']]
#bridge types available
BridgeTypes2 = BridgeTypes2.loc[:, (['trunk', 'unclassified','secondary_link','primary_link','primary','residential','trunk_link','living_street','busway','service','tertiary','motorway','tertiary_link','secondary','motorway_link']
             , ['beam','suspension','cable-stayed','truss','arch','floating','beam;truss','simple-suspension'])]
BridgeTypes5 = BridgeTypes4[['beam','suspension','cable-stayed','truss','arch','floating','beam;truss','simple-suspension']]

# Write the dataframes to an Excel file
with pd.ExcelWriter('RoadsInfo.xlsx') as writer:  
    Roads.to_excel(writer, sheet_name='Roads')
    Paving.to_excel(writer, sheet_name='Paving')
    Width.to_excel(writer, sheet_name='Width')    
    Tunnels.to_excel(writer, sheet_name='Tunnels')    
    Bridges.to_excel(writer, sheet_name='Bridges')
    Lanes.to_excel(writer,sheet_name='Lanes')
    Lit.to_excel(writer,sheet_name='Lit')
    PedBic.to_excel(writer,sheet_name='PedBic')
    Service.to_excel(writer, sheet_name='Service roads')
    Road_Quality.to_excel(writer,sheet_name='Road Quality')
    Road_Smoothness.to_excel(writer,sheet_name='Road Smoothness') 
    BridgeTypes.to_excel(writer,sheet_name='Bridge type')  

# Write the dataframes to an Excel file for pivoted data
with pd.ExcelWriter('RoadsInfo-pivot.xlsx') as writer:  
    Roads.to_excel(writer, sheet_name='Roads')
    Paving2.to_excel(writer, sheet_name='Paving')
    Paving3.to_excel(writer, sheet_name='Paving aggregated')
    Width.to_excel(writer, sheet_name='Width')    
    Tunnels2.to_excel(writer, sheet_name='Tunnels')    
    Bridges2.to_excel(writer, sheet_name='Bridges')
    BridgeTypes2.to_excel(writer,sheet_name='Typer per county-road')
    BridgeTypes5.to_excel(writer,sheet_name='Types per road')
    Lanes.to_excel(writer,sheet_name='Lanes')
    Lit2.to_excel(writer,sheet_name='Lit')
    PedBic2.to_excel(writer,sheet_name='PedBic')
    Service2.to_excel(writer, sheet_name='Service roads')
    Road_Quality2.to_excel(writer,sheet_name='Road Quality')
    Road_Smoothness2.to_excel(writer,sheet_name='Road Smoothness')    



#%% INFORMAL ROADS OUTPUT

# Define the path to the Excel file containing informal road data
Informal_Road_Results = 'C:\your-directory\Output\Output-merged\Informal-Roads.xlsx'

# Read the Excel file into a dictionary of dataframes where each sheet is a dataframe
Informal_Roads_dict  = pd.read_excel( Informal_Road_Results, sheet_name=None )

# Values to drop from 'country' column
values_to_drop = ['bedfordshire', 'berkshire', 'bristol', 'buckinghamshire', 'cambridgeshire', 'cheshire', 'cornwall', 'cumbria', 'derbyshire', 'devon', 'dorset', 'durham', 'east-sussex', 'east-yorkshire-with-hull', 'essex', 'gloucestershire', 'greater-london', 'greater-manchester', 'hampshire', 'hertfordshire', 'herefordshire', 'isle-of-man', 'isle-of-wight', 'isle-of-wright', 'kent', 'lancashire', 'leicestershire', 'lincolnshire', 'merseyside', 'norfolk', 'north-yorkshire', 'northamptonshire', 'northumberland', 'nottinghamshire', 'oxfordshire', 'rutland', 'shropshire', 'somerset', 'south-yorkshire', 'staffordshire', 'suffolk', 'surrey', 'tyne-and-wear', 'warwickshire', 'west-midlands', 'west-sussex', 'west-yorkshire', 'wiltshire', 'worcestershire']

# Iterate over each dataframe in the dictionary and drop specified values from 'country' column
for key, dataframe in Informal_Roads_dict.items():
    Informal_Roads_dict[key] = dataframe[~dataframe['country'].isin(values_to_drop)]


#Merge country regions into country codes
for i in Informal_Roads_dict.values():     
    i.drop('Unnamed: 0', inplace=True, axis=1)
    i.loc[i['country'].isin(IN),'country']='india'     
    i.loc[i['country'].isin(INDO),'country']='indonesia' 
    i.loc[i['country'].isin(JP),'country']='japan'    
    i.loc[i['country'].isin(RUS),'country']='russia' 
    i.loc[i['country'].isin(FR),'country']='france' 
    i.loc[i['country'].isin(GR),'country']='germany'    
    i.loc[i['country'].isin(GB),'country']='great-britain'     
    i.loc[i['country'].isin(IT),'country']='italy' 
    i.loc[i['country'].isin(NL),'country']='netherlands'    
    i.loc[i['country'].isin(PO),'country']='poland'     
    i.loc[i['country'].isin(CN),'country']='canada'     
    i.loc[i['country'].isin(USA),'country']='usa' 
    i.loc[i['country'].isin(BR),'country']='brazil' 
    i.loc[i['country'].isin(ES),'country']='spain' 


# Extract specific dataframes from the dictionary
IR_Roads = Informal_Roads_dict.get('Roads')
IR_Roads_a = Informal_Roads_dict.get('Roads')
IR_Paving = Informal_Roads_dict.get('Paving')
IR_Paving_agg = Informal_Roads_dict.get('Paving')
IR_Width = Informal_Roads_dict.get('Width')
IR_Tunnels = Informal_Roads_dict.get('Tunnels')
IR_Bridges = Informal_Roads_dict.get('Bridges')
IR_Lanes = Informal_Roads_dict.get('Lanes')
IR_Lit = Informal_Roads_dict.get('Lit')
IR_PedBic = Informal_Roads_dict.get('PedBic')
IR_Service = Informal_Roads_dict.get('Service roads')
IR_Road_Quality = Informal_Roads_dict.get('Road Quality')
IR_Road_Quality_agg = Informal_Roads_dict.get('Road Quality')
IR_SufaceWidth = Informal_Roads_dict.get('Area')
IR_BridgeTypes = Informal_Roads_dict.get('Bridge type')


# Aggregate paving materials into categories
IR_Paving_agg.replace({'asphalt': 'paved', 'paved': 'paved', 'concrete': 'paved', 'concrete:plates': 'paved', 'concrete:lanes': 'paved', 'asphalt;sand': 'paved', 'chipseal': 'paved'}, inplace=True)
IR_Paving_agg.replace({'gravel': 'unpaved - construction', 'compacted': 'unpaved - construction', 'fine_gravel': 'unpaved - construction', 'laterite': 'unpaved - construction', 'grass_paver': 'unpaved - construction'}, inplace=True)
IR_Paving_agg.replace({'paving_stones': 'paving_stone', 'cobblestone': 'stone', 'sett': 'stone', 'pebblestone': 'stone', 'unhewn_cobblestone': 'stone', 'cobblestone_flattened': 'stone'}, inplace=True)
IR_Paving_agg.replace({'brick': 'brick', 'bricks': 'brick'}, inplace=True)
IR_Paving_agg.replace({'ground': 'unpaved - unmanaged', 'dirt': 'unpaved - unmanaged', 'unpaved': 'unpaved - unmanaged', 'sand': 'unpaved - unmanaged', 'earth': 'unpaved - unmanaged', 'grass': 'unpaved - unmanaged', 'ice': 'unpaved - unmanaged', 'dirt/sand': 'unpaved - unmanaged', 'mud': 'unpaved - unmanaged', 'laterite': 'unpaved - unmanaged', 'soil': 'unpaved - unmanaged', 'salt': 'unpaved - unmanaged', 'clay': 'unpaved - unmanaged', 'karral': 'unpaved - unmanaged', 'ice_road': 'unpaved - unmanaged', 'trail': 'unpaved - unmanaged' }, inplace=True)
IR_Paving_agg.replace({'wood': 'wood', 'metal': 'metal'}, inplace=True)
IR_Paving_agg.replace({'rock': 'unpaved - unmanaged', 'snow': 'unpaved - unmanaged'}, inplace=True)
IR_Paving_agg.replace({'woodchips': 'wood', 'shingle': 'unpaved - construction'}, inplace=True)
IR_Paving_agg.replace({ 'shells': 'unpaved - construction', 'rocks': 'unpaved - unmanaged', 'moss': 'unpaved - unmanaged', 'peat': 'unpaved - unmanaged', 'glacier': 'unpaved - unmanaged',  'stones': 'unpaved - unmanaged', 'bare_rock': 'unpaved - unmanaged', 'terre': 'unpaved - unmanaged',  'artificial_turf': 'plastic', 'ground:lanes': 'unpaved - unmanaged', 'gravel path': 'unpaved - construction', 'ground;woodchips': 'wood', 'metal_grid': 'metal', 'dirt;gravel': 'unpaved - construction', 'ground,gravel': 'unpaved - unmanaged', 'unpaved;gravel': 'unpaved - construction', 'dirt;grass': 'unpaved - unmanaged'}, inplace=True)


#For road quality aggregate into the correct materials
IR_Road_Quality_agg.replace({'asphalt': 'paved', 'paved': 'paved', 'concrete': 'paved', 'concrete:plates': 'paved', 'concrete:lanes': 'paved', 'asphalt;sand': 'paved', 'chipseal': 'paved'}, inplace=True)
IR_Road_Quality_agg.replace({'gravel': 'unpaved - construction', 'compacted': 'unpaved - construction', 'fine_gravel': 'unpaved - construction', 'laterite': 'unpaved - construction', 'grass_paver': 'unpaved - construction'}, inplace=True)
IR_Road_Quality_agg.replace({'paving_stones': 'paving_stone', 'cobblestone': 'stone', 'sett': 'stone', 'pebblestone': 'stone', 'unhewn_cobblestone': 'stone', 'cobblestone_flattened': 'stone'}, inplace=True)
IR_Road_Quality_agg.replace({'brick': 'brick', 'bricks': 'brick'}, inplace=True)
IR_Road_Quality_agg.replace({'ground': 'unpaved - unmanaged', 'dirt': 'unpaved - unmanaged', 'unpaved': 'unpaved - unmanaged', 'sand': 'unpaved - unmanaged', 'earth': 'unpaved - unmanaged', 'grass': 'unpaved - unmanaged', 'ice': 'unpaved - unmanaged', 'dirt/sand': 'unpaved - unmanaged', 'mud': 'unpaved - unmanaged', 'laterite': 'unpaved - unmanaged', 'soil': 'unpaved - unmanaged', 'salt': 'unpaved - unmanaged', 'clay': 'unpaved - unmanaged', 'karral': 'unpaved - unmanaged', 'ice_road': 'unpaved - unmanaged', 'trail': 'unpaved - unmanaged' }, inplace=True)
IR_Road_Quality_agg.replace({'wood': 'wood', 'metal': 'metal'}, inplace=True)
IR_Road_Quality_agg.replace({'rock': 'unpaved - unmanaged', 'snow': 'unpaved - unmanaged'}, inplace=True)
IR_Road_Quality_agg.replace({'woodchips': 'wood', 'shingle': 'unpaved - construction'}, inplace=True)
IR_Road_Quality_agg.replace({ 'shells': 'unpaved - construction', 'rocks': 'unpaved - unmanaged', 'moss': 'unpaved - unmanaged', 'peat': 'unpaved - unmanaged', 'glacier': 'unpaved - unmanaged',  'stones': 'unpaved - unmanaged', 'bare_rock': 'unpaved - unmanaged', 'terre': 'unpaved - unmanaged',  'artificial_turf': 'plastic', 'ground:lanes': 'unpaved - unmanaged', 'gravel path': 'unpaved - construction', 'ground;woodchips': 'wood', 'metal_grid': 'metal', 'dirt;gravel': 'unpaved - construction', 'ground,gravel': 'unpaved - unmanaged', 'unpaved;gravel': 'unpaved - construction', 'dirt;grass': 'unpaved - unmanaged'}, inplace=True)


#CALCULATE WIDTH OF AVERAGE ROAD TYPE PER COUNTRY
IR_Width = IR_Width[pd.to_numeric(IR_Width['width'], errors='coerce').notnull()]
IR_Width['width'] = IR_Width['width'].astype(float)
#Remove roads wider than 200 meters, as there are none existing currently
IR_Width = IR_Width[IR_Width['width'] < 200]  

def weighted_average(IR_Width, value, weight):
    val = IR_Width[value]
    wt = IR_Width[weight]
    return (val * wt).sum() / wt.sum()

IR_Width_weighted = IR_Width.groupby(['highway','country']).apply(weighted_average,'width', 'length').reset_index()

# Perform groupby operations to aggregate data
IR_Roads =  IR_Roads.groupby(['highway','country'])['length'].sum().reset_index()
IR_Bridges = IR_Bridges.groupby(['highway','bridge','country'])['length'].sum().reset_index()
IR_Bridges = IR_Bridges.loc[IR_Bridges['bridge'] != 'no']
IR_Bridges_sum = IR_Bridges.groupby(['highway','country'])['length'].sum().reset_index()        
IR_BridgeTypes = IR_BridgeTypes.groupby(['highway','bridge:structure','country'])['length'].sum().reset_index()
IR_BridgeTypes3 = IR_BridgeTypes.groupby(['highway','bridge:structure'])['length'].sum().reset_index()
IR_Tunnels = IR_Tunnels.groupby(['highway','tunnel','country'])['length'].sum().reset_index()     
IR_Lit = IR_Lit.groupby(['highway', 'lit','country'])['length'].sum().reset_index()
IR_Width_attribute = IR_Width.groupby(['highway','country'])['length'].sum().reset_index()     
IR_Paving =  IR_Paving.groupby(['highway','surface','country'])['length'].sum().reset_index()
IR_Paving_agg = IR_Paving_agg.groupby(['highway','surface','country'])['length'].sum().reset_index()
IR_Paving_agg2 =  IR_Paving.groupby(['surface','country'])['length'].sum().reset_index()

#CHECK WHICH MATERIALS ARE MOST COMMON
IR_Paving_agg_global =  IR_Paving_agg.groupby(['surface'])['length'].sum().reset_index()
IR_Road_Quality =IR_Road_Quality.groupby(['highway','smoothness','surface','country'])['length'].sum().reset_index()

#renaming columsn for further processing and selecting the right road types
IR_Widthh = pd.merge(IR_Width_attribute, IR_Width_weighted, left_index=True, right_index=True)
IR_Widthh = IR_Widthh.drop(IR_Widthh.columns[[3, 4]],axis = 1)
IR_Widthh = IR_Widthh.rename(columns={"highway_x": "highway", "country_x": "country", 0 : "width"})
IR_Widthh = IR_Widthh[IR_Widthh['highway'].isin(['bridleway', 'cycleway','footway','path','pedestrian','steps','track'])]  

#remove length of shorter than 2km. Lowest 20%, as the sample is too small for accurate representativeniss 
IR_Widthh = IR_Widthh[IR_Widthh['length'] > 2]
IR_Widthh_stat = IR_Widthh.describe()

# Pivot dataframes for easier analysis
IR_Roads = IR_Roads.pivot(index='country', columns='highway', values='length')
IR_Paving_b = IR_Paving_agg.pivot(index='country', columns=['highway','surface'], values='length')
IR_Paving2 = IR_Paving_agg.pivot(index='country', columns=['highway','surface'], values='length')
IR_Paving3 = IR_Paving_agg2.pivot(index='country', columns='surface', values='length')
IR_Width_pivot = IR_Widthh.pivot(index='country', columns=['highway','width'], values='length')
IR_Width_pivot_forstat = IR_Widthh.pivot(index='country', columns=['highway'], values='length')
IR_Width_pivot_stat = IR_Width_pivot_forstat.describe()
IR_Tunnels2 = IR_Tunnels.pivot(index='country', columns=['highway','tunnel'], values='length')
IR_Bridges_sum2 = IR_Bridges_sum.pivot(index='country', columns='highway', values='length')
IR_Lit2 = IR_Lit.pivot(index='country', columns=['highway','lit'], values='length')
IR_Road_Quality2 = IR_Road_Quality.pivot(index='country', columns=['highway','smoothness','surface'], values='length')
IR_BridgeTypes2 = IR_BridgeTypes.pivot(index='country', columns=['highway','bridge:structure'], values='length')
IR_BridgeTypes4 = IR_BridgeTypes3.pivot(index='highway', columns='bridge:structure', values='length')
IR_Widthh_per_type = IR_Widthh.pivot(index='country', columns='highway', values='width')

# Reindex IR_Widthh_per_type with the index of IR_Roads
IR_Widthh_per_type = IR_Widthh_per_type.reindex(IR_Roads.index)

#Get the weighted average width for the globe
IR_Weighted_width = (IR_Width_pivot_forstat) * IR_Widthh_per_type
IR_Weighted_width.loc['Total'] = IR_Weighted_width.sum()
IR_Width_pivot_forstat.loc['Total'] = IR_Width_pivot_forstat.sum()

# Assuming IR_Width_pivot_forstat and IR_Weighted_width are dataframes containing the 'Total' row
last_row_IR_Width_pivot_forstat = IR_Width_pivot_forstat.loc['Total']
last_row_IR_Weighted_width = IR_Weighted_width.loc['Total']

# Calculate the average width
average_width =  last_row_IR_Weighted_width / last_row_IR_Width_pivot_forstat

# Create a new row with the average_width value
new_row = pd.DataFrame({'world_average': average_width}).transpose()

# Add the new row to the IR_Widthh_per_type dataframe
IR_Widthh_per_type = pd.concat([IR_Widthh_per_type, new_row])
# Use the 'world_average' value to populate NaN values
IR_Widthh_per_type_filled = IR_Widthh_per_type.fillna(average_width)
# Change values for countries that have 0 to the world average
IR_Widthh_per_type_filled = IR_Widthh_per_type_filled.replace(0, IR_Widthh_per_type_filled.iloc[-1])

#Select the types that are most common - most insightful for analysis and removing mislabelled items in the process
IR_Roads = IR_Roads[['bridleway', 'cycleway','footway','path','pedestrian','steps','track']]
IR_Paving_c = IR_Paving_b.loc[:, (['bridleway', 'cycleway','footway','path','pedestrian','steps','track'],
              ['paved', 'unpaved - construction','paving_stone','stone','brick','wood','metal','unpaved - unmanaged','plastic'])]
IR_Tunnels2 = IR_Tunnels2.loc [:, (['bridleway', 'cycleway','footway','path','pedestrian','steps','track'], ['yes'])]
IR_Bridges_sum2 = IR_Bridges_sum2[['bridleway', 'cycleway','footway','path','pedestrian','steps','track']]    
IR_Lit2 = IR_Lit2.loc [:, (['bridleway', 'cycleway','footway','path','pedestrian','steps','track'], ['yes', 'no'])]
IR_Road_Quality2 = IR_Road_Quality2.loc[:, (['bridleway', 'cycleway','footway','path','pedestrian','steps','track'],
                        ['excellent','very_good','good','intermediate','poor','bad','very_bad','horrible','very_horrible','impassable']
             , ['paved', 'unpaved - construction','paving_stone','stone','brick','wood','metal','unpaved - unmanaged','plastic'])]
IR_BridgeTypes2 = IR_BridgeTypes2.loc[:, (['bridleway', 'cycleway','footway','path','pedestrian','steps','track']
             , ['beam','suspension','cable-stayed','truss','arch','floating','simple-suspension','humpback','log','boardwalk','simple_wooden','suspended','arch'])]
IR_BridgeTypes4 = IR_BridgeTypes4[['beam','suspension','cable-stayed','truss','arch','floating','simple-suspension','humpback','log','boardwalk','simple_wooden','suspended','arch']]


# Write processed data to a new Excel file
with pd.ExcelWriter('Informal_Roads.xlsx') as writer:  
    IR_Roads.to_excel(writer, sheet_name='Informal_roads')
    IR_Paving_c.to_excel(writer, sheet_name='Paving')
    IR_Widthh_per_type_filled.to_excel(writer, sheet_name='Width')    
    IR_Tunnels2.to_excel(writer, sheet_name='Tunnels')    
    IR_Bridges_sum2.to_excel(writer, sheet_name='Bridges')
    IR_Lit2.to_excel(writer,sheet_name='Lit')
    IR_Road_Quality2.to_excel(writer,sheet_name='Road Quality')
    IR_BridgeTypes2.to_excel(writer,sheet_name='Bridge type per country')  
    IR_BridgeTypes4.to_excel(writer,sheet_name='Bridge type global')



#%%

#Rail output

# Define the path to the Excel file containing rail data
Rail_Results = 'C:\your-directory\Output\Output-merged\Rail.xlsx'

# Read the Excel file into a dictionary of dataframes where each sheet is a dataframe
rails  = pd.read_excel( Rail_Results, sheet_name=None )

# Merge regions to country name
for i in rails.values():     
    i.loc[i['country'].isin(IN),'country']='india'     
    i.loc[i['country'].isin(INDO),'country']='indonesia' 
    i.loc[i['country'].isin(JP),'country']='japan'    
    i.loc[i['country'].isin(RUS),'country']='russia' 
    i.loc[i['country'].isin(FR),'country']='france' 
    i.loc[i['country'].isin(GR),'country']='germany'    
    i.loc[i['country'].isin(GB),'country']='great-britain'     
    i.loc[i['country'].isin(IT),'country']='italy' 
    i.loc[i['country'].isin(NL),'country']='netherlands'    
    i.loc[i['country'].isin(PO),'country']='poland'     
    i.loc[i['country'].isin(CN),'country']='canada'     
    i.loc[i['country'].isin(USA),'country']='usa' 
    i.loc[i['country'].isin(BR),'country']='brazil'     
    i.loc[i['country'].isin(ES),'country']='spain' 

# Extract specific dataframes from the dictionary
rail = rails.get('Rails')
electrified = rails.get('Electrified')
rail_tunnel = rails.get('Rail_Tunnel')
rail_bridges = rails.get('Rail_Bridges')
rail_stationary = rails.get('Rail_Stationary')
Abandoned_to_road = rails.get('Abandoned_to_road')
Gauge = rails.get('Gauge')
Highspeed = rails.get('Highspeed')

# Filter dataframes based on certain criteria
Highspeed = Highspeed[Highspeed['highspeed'] == 'yes']
rail_tunnel = rail_tunnel[rail_tunnel['tunnel'] == 'yes']
rail_bridges = rail_bridges[rail_bridges['bridge'].isin(['yes', 'viaduct','aquaduct'])]

# Perform groupby operations to aggregate data
global_summary_bridge = rail_bridges.groupby(['railway','bridge'])['length'].sum().reset_index()
global_summary_rail =  rail.groupby('railway')['length'].sum().reset_index()
rail =  rail.groupby(['railway','country'])['length'].sum().reset_index()
electrified = electrified.groupby(['railway','electrified','country'])['length'].sum().reset_index()
rail_tunnel = rail_tunnel.groupby(['railway','tunnel','country'])['length'].sum().reset_index()            
rail_bridges = rail_bridges.groupby(['railway','bridge','country'])['length'].sum().reset_index()
rail_stationary = rail_stationary.groupby('railway','country').sum().reset_index()
Abandoned_to_road = Abandoned_to_road.groupby(['highway','country'])['length'].sum().reset_index()            
Gauge =  Gauge.groupby(['railway','gauge','country'])['length'].sum().reset_index()
Highspeed =  Highspeed.groupby(['railway','highspeed','country'])['length'].sum().reset_index()


# Pivot dataframes for easier analysis
rail = rail.pivot(index='country', columns='railway', values='length')
electrified = electrified.pivot(index='country', columns=['railway','electrified'], values='length')
rail_tunnel = rail_tunnel.pivot(index='country', columns=['railway','tunnel'], values='length')
rail_bridges = rail_bridges.pivot(index='country', columns=['railway','bridge'], values='length')
rail_stationary = rail_stationary.pivot(index='country', columns='railway')
Abandoned_to_road = Abandoned_to_road.pivot(index='country', columns='highway', values='length')
Gauge = Gauge.pivot(index='country', columns=['railway','gauge'], values='length')
Highspeed = Highspeed.pivot(index='country', columns=['railway','highspeed'], values='length')

# Select and filter desired columns for analysis
rail = rail[['rail', 'abandoned','construction','proposed','disused','subway','razed','tram','platform','narrow_gauge','light_rail','planned','preserved','platform_edge','monorail','station','dismantled','miniature']]
electrified = electrified.loc[:, (['rail', 'abandoned','construction','proposed','disused','subway','razed','tram','platform','narrow_gauge','light_rail','planned','preserved','platform_edge','monorail','station','dismantled','miniature'],['contact_line', 'yes'])]
rail_tunnel = rail_tunnel.loc[:, (['rail', 'abandoned','construction','proposed','disused','subway','razed','tram','platform','narrow_gauge','light_rail','planned','preserved','platform_edge','monorail','station','dismantled','miniature'])]
rail_bridges = rail_bridges.loc[:, (['rail', 'abandoned','construction','proposed','disused','subway','razed','tram','platform','narrow_gauge','light_rail','planned','preserved','platform_edge','monorail','station','dismantled','miniature'],['yes', 'viaduct','aquaduct'])]
Highspeed = Highspeed.loc[:, (['rail', 'abandoned','construction','proposed','disused','subway','razed','tram','platform','narrow_gauge','light_rail','planned','preserved','platform_edge','monorail','station','dismantled','miniature'],)]

# Write processed data to a new Excel file
with pd.ExcelWriter('Railprocessed.xlsx') as writer:  
    rail.to_excel(writer, sheet_name='Rails')
    electrified.to_excel(writer, sheet_name='Electrified')
    rail_tunnel.to_excel(writer, sheet_name='Rail_Tunnel')    
    rail_bridges.to_excel(writer, sheet_name='Rail_Bridges')    
    Highspeed.to_excel(writer, sheet_name='Highspeed')


#%%
#Parking output

# Define the path to the Excel file containing parking data
Parking_results = 'C:\your-directory\Output\Output-merged\Parking.xlsx'

# Read the Excel file into a dictionary of dataframes where each sheet is a dataframe
parking_dict  = pd.read_excel( Parking_results, sheet_name=None )

# Merge regions to country name
for i in parking_dict.values():     
    #i.drop('Unnamed: 0', inplace=True, axis=1)
    i.loc[i['country'].isin(IN),'country']='india'     
    i.loc[i['country'].isin(INDO),'country']='indonesia' 
    i.loc[i['country'].isin(JP),'country']='japan'    
    i.loc[i['country'].isin(RUS),'country']='russia' 
    i.loc[i['country'].isin(FR),'country']='france' 
    i.loc[i['country'].isin(GR),'country']='germany'    
    i.loc[i['country'].isin(GB),'country']='great-britain'     
    i.loc[i['country'].isin(IT),'country']='italy' 
    i.loc[i['country'].isin(NL),'country']='netherlands'    
    i.loc[i['country'].isin(PO),'country']='poland'     
    i.loc[i['country'].isin(CN),'country']='canada'     
    i.loc[i['country'].isin(USA),'country']='usa' 
    i.loc[i['country'].isin(BR),'country']='brazil'       
    i.loc[i['country'].isin(ES),'country']='spain' 

# Extract specific dataframes from the dictionary
Parking_Area = parking_dict.get('Area')
Parking_Area_by_surface = parking_dict.get('Area by surface type')


# Aggregate parking area data
global_park_area = Parking_Area.groupby('parking')['area'].sum().reset_index()
global_park_area["area"] = global_park_area["area"]/1000000

# Group parking area by country and type
Parking_ar_grouped = Parking_Area.groupby(['country','parking'])['area'].sum().reset_index()

# Pivot the data for easier analysis
Parking_Area_piv = Parking_ar_grouped.pivot(index='country', columns='parking', values='area')

# Filter and normalize parking area data
Parking_Area_piv_filtered = Parking_Area_piv[['surface','multi-storey','street_side','underground','lane','rooftop','garage_boxes','carports','garage','depot','sheds','layby','park_and_ride','garages','Carpool','carpool','park_ride']]
Parking_Area_piv_filtered = Parking_Area_piv_filtered/1000000

# Group parking area by country and surface type
Parking_surf_ar_grouped = Parking_Area_by_surface.groupby(['country','surface'])['area'].sum().reset_index()

# Pivot the data for easier analysis
Parking_Surf_Area_piv = Parking_surf_ar_grouped.pivot(index='country', columns='surface', values='area')

# Replace surface types to standardize them
Parking_surf_ar_grouped.replace({'asphalt': 'paved', 'paved': 'paved', 'concrete': 'paved', 'concrete:plates': 'paved', 'concrete:lanes': 'paved', 'asphalt;sand': 'paved', 'chipseal': 'paved'}, inplace=True)
Parking_surf_ar_grouped.replace({'gravel': 'unpaved - construction', 'compacted': 'unpaved - construction', 'fine_gravel': 'unpaved - construction', 'laterite': 'unpaved - construction', 'grass_paver': 'unpaved - construction'}, inplace=True)
Parking_surf_ar_grouped.replace({'paving_stones': 'paving_stone', 'cobblestone': 'stone', 'sett': 'stone', 'pebblestone': 'stone', 'unhewn_cobblestone': 'stone', 'cobblestone_flattened': 'stone'}, inplace=True)
Parking_surf_ar_grouped.replace({'brick': 'brick', 'bricks': 'brick'}, inplace=True)
Parking_surf_ar_grouped.replace({'ground': 'unpaved - unmanaged', 'dirt': 'unpaved - unmanaged', 'unpaved': 'unpaved - unmanaged', 'sand': 'unpaved - unmanaged', 'earth': 'unpaved - unmanaged', 'grass': 'unpaved - unmanaged', 'ice': 'unpaved - unmanaged', 'dirt/sand': 'unpaved - unmanaged', 'mud': 'unpaved - unmanaged', 'laterite': 'unpaved - unmanaged', 'soil': 'unpaved - unmanaged', 'salt': 'unpaved - unmanaged', 'clay': 'unpaved - unmanaged', 'karral': 'unpaved - unmanaged', 'ice_road': 'unpaved - unmanaged', 'trail': 'unpaved - unmanaged' }, inplace=True)
Parking_surf_ar_grouped.replace({'wood': 'wood', 'metal': 'metal'}, inplace=True)
Parking_surf_ar_grouped.replace({'rock': 'unpaved - unmanaged', 'snow': 'unpaved - unmanaged'}, inplace=True)
Parking_surf_ar_grouped.replace({'woodchips': 'wood', 'shingle': 'unpaved - construction'}, inplace=True)
Parking_surf_ar_grouped.replace({ 'shells': 'unpaved - construction', 'rocks': 'unpaved - unmanaged', 'moss': 'unpaved - unmanaged', 'peat': 'unpaved - unmanaged', 'glacier': 'unpaved - unmanaged',  'stones': 'unpaved - unmanaged', 'bare_rock': 'unpaved - unmanaged', 'terre': 'unpaved - unmanaged',  'artificial_turf': 'plastic', 'ground:lanes': 'unpaved - unmanaged', 'gravel path': 'unpaved - construction', 'ground;woodchips': 'wood', 'metal_grid': 'metal', 'dirt;gravel': 'unpaved - construction', 'ground,gravel': 'unpaved - unmanaged', 'unpaved;gravel': 'unpaved - construction', 'dirt;grass': 'unpaved - unmanaged'}, inplace=True)

# Re-group parking area by country and surface type
Parking_surf_ar_grouped = Parking_surf_ar_grouped.groupby(['country', 'surface'])['area'].sum().reset_index()

# Pivot the data for easier analysis
Parking_Surf_Area_piv = Parking_surf_ar_grouped.pivot(index='country', columns='surface', values='area')

# Select desired columns for further analysis
desired_columns = ['paved', 'unpaved - construction', 'paving_stone', 'stone', 'brick', 'wood', 'metal', 'unpaved - unmanaged', 'plastic']

# Filter and normalize parking area data by material type
Parking_Surf_Area_piv_materials = Parking_Surf_Area_piv[desired_columns]
Parking_Surf_Area_piv_materials = Parking_Surf_Area_piv_materials / 1000000

# Write processed data to a new Excel file
with pd.ExcelWriter('ParkingProcessed.xlsx') as writer:  
    global_park_area.to_excel(writer, sheet_name='Global park type')
    Parking_Area_piv_filtered.to_excel(writer, sheet_name='Park type per country')
    Parking_Surf_Area_piv_materials.to_excel(writer, sheet_name='Paving shares per country')

