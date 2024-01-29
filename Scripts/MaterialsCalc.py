# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:45:15 2023

@author: MvEng
"""
# Import necessary libraries
import pandas as pd
from os import chdir

#ADD FOLDER OF PREFERENCE FOR RESULTS HERE
chdir('C:\your-directory\Example-results')
        
#%%|IMPORTING Bridges & Tunnels Mat data

Bridge_input = 'C:\your-directory\Output\Processed\BT_Input_processed.xlsx'
BT_Material = 'C:\your-directory\Output\Material intensities\mat_per_bridgetunnel_type.xlsx' 

# Read all sheets into a dictionary of dataframes
brd = pd.read_excel(Bridge_input, sheet_name=None, index_col=(0))
BT_Mat  = pd.read_excel( BT_Material,header=[0],index_col=[0])

# Store each dataframe in a separate variable
bridges = brd['Bridges']
tunnels = brd['Tunnels']

#TUNNELS - select the correct values for calculation
road_tunnel_values = tunnels.iloc[:, 15].values
road_tunnel_mat_values = BT_Mat.iloc[:, 1].values

tunnel_road_mat = road_tunnel_values[:, None] * road_tunnel_mat_values

tunnel_road = pd.DataFrame(tunnel_road_mat, columns=BT_Mat.index, index=tunnels.index)

#BRIDGES - select the correct values for calculation
road_bridge_values = bridges.iloc[:, 15].values
road_bridge_mat_values = BT_Mat.iloc[:, 0].values

bridge_road_mat = road_bridge_values[:, None] * road_bridge_mat_values

bridge_road = pd.DataFrame(bridge_road_mat, columns=BT_Mat.index, index=bridges.index)

# List of final DataFrames
final_brd = [tunnel_road, bridge_road]

# Initialize the sum DataFrame with the index from one of the final DataFrames
sum_brd = pd.DataFrame(index=final_brd[0].index)

# Sum up the values from each DataFrame
for df in final_brd:
    sum_brd = sum_brd.add(df, fill_value=0)

# Create the DataFrame names for tunnels and bridges
brtun = ['tunnel_road','bridge_road']

# Add the DataFrame names as a new column to each DataFrame
for df, name in zip(final_brd, brtun):
    df['part_road_infra'] = name

# Concatenate the DataFrames along the desired axis (e.g., axis=0 for row-wise concatenation)
brtun_df = pd.concat(final_brd, axis=0)

#%%|IMPORTING RAIL 

Rail_input = 'C:\your-directory\Output\Processed\Rail_Input_processed.xlsx'
Rail_Material = 'C:\your-directory\Output\Material intensities\mat_per_rail_type.xlsx'

# Read all sheets into a dictionary of dataframes
dfs = pd.read_excel(Rail_input, sheet_name=None, index_col=(0))
Rail_Mat  = pd.read_excel( Rail_Material,header=[0],index_col=[0])

# Store each dataframe in a separate variable
Rail = dfs['Rails']
Tram = dfs['Tram']
Disused = dfs['Abandoned']
Rail_bridges = dfs['Rail_Bridges']
Rail_tunnels = dfs['Rail_Tunnel']
Highspeed = dfs['Highspeed']

# Subtract column 2 from column 1 and add a new column in column 3 for Rail DataFrame
Rail['Standard Rail'] = Rail.iloc[:, 0] - Rail.iloc[:, 1]

# Subtract column 2 from column 1 and add a new column in column 3 for Disused DataFrame
Disused['Standard_Disused_Rail'] = Disused.iloc[:, 0] - Disused.iloc[:, 1]

# Perform the multiplication using broadcasting
rail_values = Rail.iloc[:, 3].values
disused_values = Disused.iloc[:, 2].values
standard_rail_mat_values = Rail_Mat.iloc[:, 0].values

# Broadcasting the multiplication
Standard_rail_mat = rail_values[:, None] * standard_rail_mat_values
Disused_stand_rail_mat = disused_values[:, None] * standard_rail_mat_values

# Create a DataFrame from the result
standard_rail = pd.DataFrame(Standard_rail_mat, columns=Rail_Mat.index, index=Rail.index)
disused_rail = pd.DataFrame(Disused_stand_rail_mat, columns=Rail_Mat.index, index=Disused.index)

# Perform the multiplication using broadcasting for Rail DataFrame
electrified_values = Rail.iloc[:, 1].values
disused_electrified_values = Disused.iloc[:, 1].values
electrified_rail_mat_values = Rail_Mat.iloc[:, 1].values

# Broadcasting the multiplication
electrified_rail_mat = electrified_values[:, None] * electrified_rail_mat_values

disused_elec_rail_mat = disused_electrified_values[:, None] * electrified_rail_mat_values

# Create a DataFrame from the result
electrified_rail = pd.DataFrame(electrified_rail_mat, columns=Rail_Mat.index, index=Rail.index)
electrified_disused = pd.DataFrame(disused_elec_rail_mat, columns=Rail_Mat.index, index=Disused.index)

# Perform the multiplication using broadcasting for Highspeed DataFrame
highspeed_values = Highspeed.iloc[:, 0].values
highspeed_rail_mat_values = Rail_Mat.iloc[:, 2].values

# Broadcasting the multiplication
highspeed_rail_mat = highspeed_values[:, None] * highspeed_rail_mat_values

# Create a DataFrame from the result
highspeed_rail = pd.DataFrame(highspeed_rail_mat, columns=Rail_Mat.index, index=Highspeed.index)

#TRAMS
tram_values = Tram.iloc[:, 1].values
tram_mat_values = Rail_Mat.iloc[:, 3].values

tram_rail_mat = tram_values[:, None] * tram_mat_values

tram_rail = pd.DataFrame(tram_rail_mat, columns=Rail_Mat.index, index=Tram.index)

#TUNNELS
tunnel_values = Rail_tunnels.iloc[:, 12].values
tunnel_mat_values = Rail_Mat.iloc[:, 6].values

tunnel_rail_mat = tunnel_values[:, None] * tunnel_mat_values

tunnel_rail = pd.DataFrame(tunnel_rail_mat, columns=Rail_Mat.index, index=Rail_tunnels.index)

#BRIDGES
bridges_values = Rail_bridges.iloc[:, 12].values
bridges_mat_values = Rail_Mat.iloc[:, 5].values

bridges_rail_mat = bridges_values[:, None] * bridges_mat_values

bridges_rail = pd.DataFrame(bridges_rail_mat, columns=Rail_Mat.index, index=Rail_bridges.index)

# List of final DataFrames
final_dfs = [standard_rail,disused_rail, electrified_rail, electrified_disused, highspeed_rail, tram_rail, tunnel_rail, bridges_rail]

# Create a list of DataFrame names
df_names = ['standard_rail','disused_rail', 'electrified_rail', 'electrified_disused', 'highspeed_rail', 'tram_rail', 'tunnel_rail', 'bridges_rail']

# Add the DataFrame names as a new column to each DataFrame
for df, name in zip(final_dfs, df_names):
    df['part_rail_infra'] = name

# Concatenate the DataFrames along the desired axis (e.g., axis=0 for row-wise concatenation)
rail_res = pd.concat(final_dfs, axis=0)

rail_res_group = rail_res.groupby(['part_rail_infra']).sum()

Rail_region = 'C:\your-directory\Example-results\Rail_Mat_Results_plus_region.xlsx'

Rail_region_aggregation = pd.read_excel( Rail_region,header=[0],index_col=[0,1,2])

Mat_rail_country_IMAGE = Rail_region_aggregation.groupby(['country-level','IMAGE-region']).sum()
Mat_rail_country = Rail_region_aggregation.groupby(['country-level']).sum()
Mat_rail_IMAGE = Rail_region_aggregation.groupby(['IMAGE-region']).sum()


#%% PARKING INFRASTRUCTURE

from os import chdir
chdir('C:\your-directory\Example-results')

aac_country_stat = 'C:\your-directory\Output\Processed\country_stat.xlsx'
aac_country_stat = pd.read_excel( aac_country_stat,header=[0],index_col=[0])
# Divide population by area and create a new column 'population_density'
aac_country_stat['population_density'] = aac_country_stat['population'] / aac_country_stat['area']

# Divide GDP by population and create a new column 'GDP_per_capita'
aac_country_stat['GDP_per_capita'] = aac_country_stat['gdp'] / aac_country_stat['population']

# Define the file path of the Excel file
Mat_int = 'C:\your-directory\Output\Material intensities\mat_per_road_type.xlsx'

# Read the Excel file into a pandas DataFrame, specifying the first row as the header and the first column as the index
Mat_int = pd.read_excel( Mat_int,header=[0],index_col=[0])

# Group the data by 'GRIP region', 'GRIP road type', and 'Country Alpha-3 Code' and calculate the mean for each group
# Calculating the average based on climate class
average_per_country = Mat_int.groupby(['GRIP region','GRIP road type','Country Alpha-3 Code']).mean()

# Group the data by 'GRIP region' and 'GRIP road type', and calculate the mean for each group
# Calculating the average by region, taking the average of the countries
average_per_grip = average_per_country.groupby(['GRIP region','GRIP road type']).mean()
columns_to_drop = [0, 1, 3, 4, 6, 7, 9, 10]
#Uses the same code as material composition as road but takes the average of the two lowest classes of roads. This is done manually in Excel resulting in the Informal_road_avg_dropped_input.xlsx 
average_per_grip_dropped = average_per_grip.drop(average_per_grip.columns[columns_to_drop], axis=1)


Mat_parking = 'C:\your-directory\Output\Composition by area\Mat_by_Parking_area.xlsx'

Mat_parking_check = pd.read_excel( Mat_parking,header=[0,1],index_col=[0,1,2])
Parking_indexed = Mat_parking_check.stack(level=[0, 1])
Parking_indexed_renamed = Parking_indexed.rename_axis(index=['country', 'GRIP_region', 'IMAGE_region', 'Road_class', 'Surface_type'])
Parking_indexed_renamed_stat = Parking_indexed.rename_axis(index=['country', 'GRIP_region', 'IMAGE_region', 'Road_class', 'Surface_type'])

Parking_indexed_renamed = Parking_indexed_renamed.to_frame()
Parking_indexed_renamed_stat = Parking_indexed_renamed_stat.to_frame()

# Rename the '0' column to 'length'
Parking_indexed_renamed = Parking_indexed_renamed.rename(columns={0: 'area'})
aaa_parking_area_country_by_roadtype = Parking_indexed_renamed_stat.rename(columns={0: 'area'})

aab_parking_area_country_by_roadtype = aaa_parking_area_country_by_roadtype.groupby(['country','GRIP_region','IMAGE_region','Road_class']).sum()

# Reset the index of aaa_road_area_country_by_roadtype to convert 'Road_class' from the index to a regular column
aab_parking_area_country_by_roadtype = aab_parking_area_country_by_roadtype.reset_index()

# Merge the two dataframes based on the 'country' index column
aab_parking_area_stat = pd.merge(aac_country_stat, aab_parking_area_country_by_roadtype, on='country')

# Divide population by area and create a new column 'population_density'
aab_parking_area_stat['capita/km2 road'] = aab_parking_area_stat['population'] / aab_parking_area_stat['area_y']
aab_parking_area_stat['GDP/km2 road'] = aab_parking_area_stat['gdp'] / aab_parking_area_stat['area_y']
aab_parking_area_stat['road land use %'] = aab_parking_area_stat['area_y'] / aab_parking_area_stat['area_x']*100

aad_parking_area_country_by_roadtype = aaa_parking_area_country_by_roadtype.groupby(['country','GRIP_region','IMAGE_region']).sum()
# Merge the two dataframes based on the 'country' index column
aad_parking_area_stat = pd.merge(aac_country_stat, aad_parking_area_country_by_roadtype, on='country')
# Divide population by area and create a new column 'population_density'
aad_parking_area_stat['capita/km2 road'] = aad_parking_area_stat['population'] / aad_parking_area_stat['area_y']
aad_parking_area_stat['GDP/km2 road'] = aad_parking_area_stat['gdp'] / aad_parking_area_stat['area_y']
aad_parking_area_stat['road land use %'] = aad_parking_area_stat['area_y'] / aad_parking_area_stat['area_x']*100
aad_parking_area_stat['m2 road/capita'] = aad_parking_area_stat['area_y'] / aad_parking_area_stat['population']* 1000000

asphalt_results = []
aggregate_results = []
cement_results = []
concrete_results = []
pavingstone_results = []
bricks_results = []
stone_results = []

for index in Parking_indexed_renamed.index:
    grip_region = index[1]  # Get the GRIP_region value from the index
    road_class = index[3]  # Get the Road_class value from the index
    surface_class = index[4]
    
    # Get the matching value from average_per_grip_dropped
    matching_value = average_per_grip_dropped.loc[(grip_region, road_class)]
    
    # Perform calculations
    length = Parking_indexed_renamed.loc[index, 'area']  # Assuming 'area' is the column you want to multiply
    
    if surface_class == 1:
        matching_result = length * matching_value * 1000000

        asphalt_results.append(matching_result['asphalt_int_median'])
        aggregate_results.append(matching_result['granular_int_median'])
        cement_results.append(matching_result['cement_int_median'])
        concrete_results.append(matching_result['concrete_int_median'])
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(None)
        
    elif surface_class in [2]:
        matching_result = length * matching_value * 1000000
        
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(None)  # Append None for other columns
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(None)
        
    elif surface_class == 3:
        matching_result = length * matching_value * 1000000          
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(length * 155 * 1000000 * 0.6913)  # Append None for other columns
        bricks_results.append(length * 124.7 * 1000000 * 0.0381)
        stone_results.append(length * 255 * 1000000 * 0.2705)      
    elif surface_class == 4:
        matching_result = length * matching_value * 1000000      
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(None)  # Append None for other columns
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(length * 255  * 1000000)
    elif surface_class == 5:
        matching_result = length * matching_value * 1000000         
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(None)  # Append None for other columns
        pavingstone_results.append(None)
        bricks_results.append(length * 124.7 * 1000000)
        stone_results.append(None)     
    else:
        asphalt_results.append(None)  # Append None for all columns
        aggregate_results.append(None)  # Append None for all columns
        cement_results.append(None)  # Append None for all columns
        concrete_results.append(None)  # Append None for all columns
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(None)

# Append the calculated results as new columns in the dataframe
Parking_indexed_renamed['asphalt'] = asphalt_results
Parking_indexed_renamed['aggregate'] = aggregate_results
Parking_indexed_renamed['cement'] = cement_results
Parking_indexed_renamed['concrete'] = concrete_results
Parking_indexed_renamed['paving_stone'] = pavingstone_results
Parking_indexed_renamed['bricks'] = bricks_results
Parking_indexed_renamed['stone'] = stone_results

Mat_parking_country_by_roadtype = Parking_indexed_renamed.groupby(['country','IMAGE_region','Road_class']).sum()
Mat_parking_country = Parking_indexed_renamed.groupby(['country']).sum()
Mat_parking_IMAGE_by_roadtype = Parking_indexed_renamed.groupby(['IMAGE_region','Road_class']).sum()
Mat_parking_total_by_roadtype = Parking_indexed_renamed.groupby(['Road_class']).sum()
Mat_parking_total = Parking_indexed_renamed.groupby(['IMAGE_region']).sum()

# Merge the two dataframes based on the 'country' index column
mat_park_area_stat = pd.merge(aad_parking_area_stat, Mat_parking_country_by_roadtype, on='country')

# Divide population by area and create a new column 'population_density'
mat_park_area_stat['kg asphalt/capita'] = mat_park_area_stat['asphalt'] / mat_park_area_stat['population']
mat_park_area_stat['kg aggregate/capita'] = mat_park_area_stat['aggregate'] / mat_park_area_stat['population']
mat_park_area_stat['kg concrete/capita'] = mat_park_area_stat['concrete'] / mat_park_area_stat['population']
mat_park_area_stat['kg cement/capita'] = mat_park_area_stat['cement'] / mat_park_area_stat['population']
mat_park_area_stat['kg brick/capita'] = mat_park_area_stat['bricks'] / mat_park_area_stat['population']
mat_park_area_stat['kg stone/capita'] = mat_park_area_stat['stone'] / mat_park_area_stat['population']

# Specify the path and filename for the Excel file
excel_file_path = 'parking_area_mat_check_final.xlsx'

# Export the DataFrame to Excel
mat_park_area_stat.to_excel(excel_file_path, index=True)


#%%ROAD MATERIAL CALCULATIONS
from os import chdir
chdir('C:\your-directory\Example-results')

aac_country_stat = 'C:\your-directory\Output\Processed\country_stat.xlsx'
aac_country_stat = pd.read_excel( aac_country_stat,header=[0],index_col=[0])
# Divide population by area and create a new column 'population_density'
aac_country_stat['population_density'] = aac_country_stat['population'] / aac_country_stat['area']

# Divide GDP by population and create a new column 'GDP_per_capita'
aac_country_stat['GDP_per_capita'] = aac_country_stat['gdp'] / aac_country_stat['population']

# Define the file path of the Excel file
Mat_int = 'C:\your-directory\Output\Material intensities\mat_per_road_type.xlsx'

# Read the Excel file into a pandas DataFrame, specifying the first row as the header and the first column as the index
Mat_int = pd.read_excel( Mat_int,header=[0],index_col=[0])

# Group the data by 'GRIP region', 'GRIP road type', and 'Country Alpha-3 Code' and calculate the mean for each group
# Calculating the average based on climate class
average_per_country = Mat_int.groupby(['GRIP region','GRIP road type','Country Alpha-3 Code']).mean()

# Group the data by 'GRIP region' and 'GRIP road type', and calculate the mean for each group
# Calculating the average by region, taking the average of the countries
average_per_grip = average_per_country.groupby(['GRIP region','GRIP road type']).mean()
columns_to_drop = [0, 1, 3, 4, 6, 7, 9, 10]
average_per_grip_dropped = average_per_grip.drop(average_per_grip.columns[columns_to_drop], axis=1)

Mat_road = 'C:\your-directory\Output\Composition by area\mat_road_area.xlsx'

Mat_roads = pd.read_excel( Mat_road,header=[0,1],index_col=[0,1,2])
Mat_roads_indexed = Mat_roads.stack(level=[0, 1])
Mat_roads_indexed_renamed = Mat_roads_indexed.rename_axis(index=['country', 'GRIP_region', 'IMAGE_region', 'Road_class', 'Surface_type'])
Mat_roads_indexed_renamed_stat = Mat_roads_indexed.rename_axis(index=['country', 'GRIP_region', 'IMAGE_region', 'Road_class', 'Surface_type'])

Mat_roads_indexed_renamed = Mat_roads_indexed_renamed.to_frame()
Mat_roads_indexed_renamed_stat = Mat_roads_indexed_renamed_stat.to_frame()

# Rename the '0' column to 'length'
Mat_roads_indexed_renamed = Mat_roads_indexed_renamed.rename(columns={0: 'area'})
aaa_road_area_country_by_roadtype = Mat_roads_indexed_renamed_stat.rename(columns={0: 'area'})

aab_road_area_country_by_roadtype = aaa_road_area_country_by_roadtype.groupby(['country','GRIP_region','IMAGE_region','Road_class']).sum()

# Reset the index of aaa_road_area_country_by_roadtype to convert 'Road_class' from the index to a regular column
aab_road_area_country_by_roadtype = aab_road_area_country_by_roadtype.reset_index()

# Merge the two dataframes based on the 'country' index column
aab_road_area_stat = pd.merge(aac_country_stat, aab_road_area_country_by_roadtype, on='country')

# Divide population by area and create a new column 'population_density'
aab_road_area_stat['capita/km2 road'] = aab_road_area_stat['population'] / aab_road_area_stat['area_y']
aab_road_area_stat['GDP/km2 road'] = aab_road_area_stat['gdp'] / aab_road_area_stat['area_y']
aab_road_area_stat['road land use %'] = aab_road_area_stat['area_y'] / aab_road_area_stat['area_x']*100

aad_road_area_country_by_roadtype = aaa_road_area_country_by_roadtype.groupby(['country','GRIP_region','IMAGE_region']).sum()
# Merge the two dataframes based on the 'country' index column
aad_road_area_stat = pd.merge(aac_country_stat, aad_road_area_country_by_roadtype, on='country')
# Divide population by area and create a new column 'population_density'
aad_road_area_stat['capita/km2 road'] = aad_road_area_stat['population'] / aad_road_area_stat['area_y']
aad_road_area_stat['GDP/km2 road'] = aad_road_area_stat['gdp'] / aad_road_area_stat['area_y']
aad_road_area_stat['road land use %'] = aad_road_area_stat['area_y'] / aad_road_area_stat['area_x']*100
aad_road_area_stat['m2 road/capita'] = aad_road_area_stat['area_y'] / aad_road_area_stat['population']* 1000000


asphalt_results = []
aggregate_results = []
cement_results = []
concrete_results = []
pavingstone_results = []
bricks_results = []
stone_results = []

for index in Mat_roads_indexed_renamed.index:
    grip_region = index[1]  # Get the GRIP_region value from the index
    road_class = index[3]  # Get the Road_class value from the index
    surface_class = index[4]
    
    # Get the matching value from average_per_grip_dropped
    matching_value = average_per_grip_dropped.loc[(grip_region, road_class)]
    
    # Perform calculations
    length = Mat_roads_indexed_renamed.loc[index, 'area']  # Assuming 'length' is the column you want to multiply
    
    if surface_class == 1:
        matching_result = length * matching_value * 1000000

        asphalt_results.append(matching_result['asphalt_int_median'])
        aggregate_results.append(matching_result['granular_int_median'])
        cement_results.append(matching_result['cement_int_median'])
        concrete_results.append(matching_result['concrete_int_median'])
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(None)
        
    elif surface_class in [2]:
        matching_result = length * matching_value * 1000000    
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(None)  # Append None for other columns
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(None)      
    elif surface_class == 3:
        matching_result = length * matching_value * 1000000        
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(length * 155 * 1000000 * 0.6913)  # Append None for other columns
        bricks_results.append(length * 124.7 * 1000000 * 0.0381)
        stone_results.append(length * 255 * 1000000 * 0.2705)       
    elif surface_class == 4:
        matching_result = length * matching_value * 1000000     
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(None)  # Append None for other columns
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(length * 255 * 1000000)
    elif surface_class == 5:
        matching_result = length * matching_value * 1000000       
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(None)  # Append None for other columns
        pavingstone_results.append(None)
        bricks_results.append(length * 124.7 * 1000000)
        stone_results.append(None)
#When other surface_class      
    else:
        asphalt_results.append(None)  # Append None for all columns
        aggregate_results.append(None)  # Append None for all columns
        cement_results.append(None)  # Append None for all columns
        concrete_results.append(None)  # Append None for all columns
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(None)

# Append the calculated results as new columns in the dataframe
Mat_roads_indexed_renamed['asphalt'] = asphalt_results
Mat_roads_indexed_renamed['aggregate'] = aggregate_results
Mat_roads_indexed_renamed['cement'] = cement_results
Mat_roads_indexed_renamed['concrete'] = concrete_results
Mat_roads_indexed_renamed['paving_stone'] = pavingstone_results
Mat_roads_indexed_renamed['bricks'] = bricks_results
Mat_roads_indexed_renamed['stone'] = stone_results


Mat_roads_country_by_roadtype = Mat_roads_indexed_renamed.groupby(['country','IMAGE_region','Road_class']).sum()
Mat_roads_country = Mat_roads_indexed_renamed.groupby(['country']).sum()
Mat_roads_IMAGE_by_roadtype = Mat_roads_indexed_renamed.groupby(['IMAGE_region','Road_class']).sum()
Mat_roads_total_by_roadtype = Mat_roads_indexed_renamed.groupby(['Road_class']).sum()
Mat_roads_total = Mat_roads_indexed_renamed.groupby(['IMAGE_region']).sum()


# Merge the two dataframes based on the 'country' index column
mat_road_area_stat = pd.merge(aad_road_area_stat, Mat_roads_country, on='country')

# Divide population by area and create a new column 'population_density'
mat_road_area_stat['kg asphalt/capita'] = mat_road_area_stat['asphalt'] / mat_road_area_stat['population']
mat_road_area_stat['kg aggregate/capita'] = mat_road_area_stat['aggregate'] / mat_road_area_stat['population']
mat_road_area_stat['kg concrete/capita'] = mat_road_area_stat['concrete'] / mat_road_area_stat['population']
mat_road_area_stat['kg cement/capita'] = mat_road_area_stat['cement'] / mat_road_area_stat['population']
mat_road_area_stat['kg brick/capita'] = mat_road_area_stat['bricks'] / mat_road_area_stat['population']
mat_road_area_stat['kg stone/capita'] = mat_road_area_stat['stone'] / mat_road_area_stat['population']

# Specify the path and filename for the Excel file
excel_file_path = 'mat_road_area_stat_check.xlsx'

# Export the DataFrame to Excel
mat_road_area_stat.to_excel(excel_file_path, index=True)


#%% For Informal_Roads
from os import chdir
chdir('C:\your-directory\Example-results')

aac_country_stat = 'C:\your-directory\Output\Processed\country_stat.xlsx'
aac_country_stat = pd.read_excel( aac_country_stat,header=[0],index_col=[0])
# Divide population by area and create a new column 'population_density'
aac_country_stat['population_density'] = aac_country_stat['population'] / aac_country_stat['area']

# Divide GDP by population and create a new column 'GDP_per_capita'
aac_country_stat['GDP_per_capita'] = aac_country_stat['gdp'] / aac_country_stat['population']

# Define the file path of the Excel file
Mat_int = 'C:\your-directory\Output\Material intensities\mat_per_road_type.xlsx'

# Read the Excel file into a pandas DataFrame, specifying the first row as the header and the first column as the index
Mat_int = pd.read_excel( Mat_int,header=[0],index_col=[0])

# Group the data by 'GRIP region', 'GRIP road type', and 'Country Alpha-3 Code' and calculate the mean for each group
# Calculating the average based on climate class
average_per_country = Mat_int.groupby(['GRIP region','GRIP road type','Country Alpha-3 Code']).mean()

# Group the data by 'GRIP region' and 'GRIP road type', and calculate the mean for each group
# Calculating the average by region, taking the average of the countries
average_per_grip = average_per_country.groupby(['GRIP region','GRIP road type']).mean()
columns_to_drop = [0, 1, 3, 4, 6, 7, 9, 10]
#Uses the same code as material composition as road but takes the average of the two lowest classes of roads. This is done manually in Excel resulting in the Informal_road_avg_dropped_input.xlsx 
average_per_grip_dropped = average_per_grip.drop(average_per_grip.columns[columns_to_drop], axis=1)

Mat_road = 'C:\your-directory\Output\Composition by area\Informal_Mat_By_Road_Area.xlsx'

Mat_roads = pd.read_excel( Mat_road,header=[0,1],index_col=[0,1,2])
Mat_roads_indexed = Mat_roads.stack(level=[0, 1])
Mat_roads_indexed_renamed = Mat_roads_indexed.rename_axis(index=['country', 'GRIP_region', 'IMAGE_region', 'Road_class', 'Surface_type'])
Mat_roads_indexed_renamed_stat = Mat_roads_indexed.rename_axis(index=['country', 'GRIP_region', 'IMAGE_region', 'Road_class', 'Surface_type'])

Mat_roads_indexed_renamed = Mat_roads_indexed_renamed.to_frame()
Mat_roads_indexed_renamed_stat = Mat_roads_indexed_renamed_stat.to_frame()

# Rename the '0' column to 'length'
Mat_roads_indexed_renamed = Mat_roads_indexed_renamed.rename(columns={0: 'area'})
aaa_road_area_country_by_roadtype = Mat_roads_indexed_renamed_stat.rename(columns={0: 'area'})

aab_road_area_country_by_roadtype = aaa_road_area_country_by_roadtype.groupby(['country','GRIP_region','IMAGE_region','Road_class']).sum()

# Reset the index of aaa_road_area_country_by_roadtype to convert 'Road_class' from the index to a regular column
aab_road_area_country_by_roadtype = aab_road_area_country_by_roadtype.reset_index()

# Merge the two dataframes based on the 'country' index column
aab_road_area_stat = pd.merge(aac_country_stat, aab_road_area_country_by_roadtype, on='country')

# Divide population by area and create a new column 'population_density'
aab_road_area_stat['capita/km2 road'] = aab_road_area_stat['population'] / aab_road_area_stat['area_y']
aab_road_area_stat['GDP/km2 road'] = aab_road_area_stat['gdp'] / aab_road_area_stat['area_y']
aab_road_area_stat['road land use %'] = aab_road_area_stat['area_y'] / aab_road_area_stat['area_x']*100

aad_road_area_country_by_roadtype = aaa_road_area_country_by_roadtype.groupby(['country','GRIP_region','IMAGE_region']).sum()
# Merge the two dataframes based on the 'country' index column
aad_road_area_stat = pd.merge(aac_country_stat, aad_road_area_country_by_roadtype, on='country')
# Divide population by area and create a new column 'population_density'
aad_road_area_stat['capita/km2 road'] = aad_road_area_stat['population'] / aad_road_area_stat['area_y']
aad_road_area_stat['GDP/km2 road'] = aad_road_area_stat['gdp'] / aad_road_area_stat['area_y']
aad_road_area_stat['road land use %'] = aad_road_area_stat['area_y'] / aad_road_area_stat['area_x']*100
aad_road_area_stat['m2 road/capita'] = aad_road_area_stat['area_y'] / aad_road_area_stat['population']* 1000000
#aad_road_area_stat['pop/km2/km2-road'] = aad_road_area_stat['population_density'] / aad_road_area_stat['area_y']
#aad_road_area_stat['GDP/cap/km2-road'] = aad_road_area_stat['GDP_per_capita'] / aad_road_area_stat['area_y']

mat_comp_input =  'C:\your-directory\Output\Processed\Informal_road_avg_dropped_input.xlsx'
mat_comp_input = pd.read_excel( mat_comp_input,header=[0],index_col=[0,1])

asphalt_results = []
aggregate_results = []
cement_results = []
concrete_results = []
pavingstone_results = []
bricks_results = []
stone_results = []

for index in Mat_roads_indexed_renamed.index:
    grip_region = index[1]  # Get the GRIP_region value from the index
    road_class = index[3]  # Get the Road_class value from the index
    surface_class = index[4]
    
    # Get the matching value from average_per_grip_dropped
    matching_value = mat_comp_input.loc[(grip_region, road_class)]
    
    # Perform calculations
    length = Mat_roads_indexed_renamed.loc[index, 'area']  # Assuming 'area' is the column you want to multiply
    
    if surface_class == 1:
        matching_result = length * matching_value * 1000000

        asphalt_results.append(matching_result['asphalt_int_median'])
        aggregate_results.append(matching_result['granular_int_median'])
        cement_results.append(matching_result['cement_int_median'])
        concrete_results.append(matching_result['concrete_int_median'])
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(None)
        
    elif surface_class in [2]:
        matching_result = length * matching_value * 1000000
        
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(None)  # Append None for other columns
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(None)
        
    elif surface_class == 3:
        matching_result = length * matching_value * 1000000         
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(length * 155 * 1000000 * 0.6913)  # Append None for other columns
        bricks_results.append(length * 124.7 * 1000000 * 0.0381)
        stone_results.append(length * 255 * 1000000 * 0.2705)        
    elif surface_class == 4:
        matching_result = length * matching_value * 1000000       
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(None)  # Append None for other columns
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(length * 255 * 1000000)
    elif surface_class == 5:
        matching_result = length * matching_value * 1000000        
        asphalt_results.append(None)
        aggregate_results.append(matching_result['granular_int_median'])  # Append None for other columns
        cement_results.append(None)  # Append None for other columns
        concrete_results.append(None)  # Append None for other columns
        pavingstone_results.append(None)
        bricks_results.append(length * 124.7 * 1000000)
        stone_results.append(None)         
    else:
        asphalt_results.append(None)  # Append None for all columns
        aggregate_results.append(None)  # Append None for all columns
        cement_results.append(None)  # Append None for all columns
        concrete_results.append(None)  # Append None for all columns
        pavingstone_results.append(None)
        bricks_results.append(None)
        stone_results.append(None)

# Append the calculated results as new columns in the dataframe
Mat_roads_indexed_renamed['asphalt'] = asphalt_results
Mat_roads_indexed_renamed['aggregate'] = aggregate_results
Mat_roads_indexed_renamed['cement'] = cement_results
Mat_roads_indexed_renamed['concrete'] = concrete_results
Mat_roads_indexed_renamed['paving_stone'] = pavingstone_results
Mat_roads_indexed_renamed['bricks'] = bricks_results
Mat_roads_indexed_renamed['stone'] = stone_results

Mat_infroads_country_by_roadtype = Mat_roads_indexed_renamed.groupby(['country','IMAGE_region','Road_class']).sum()
Mat_roads_country = Mat_roads_indexed_renamed.groupby(['country']).sum()
Mat_roads_IMAGE_by_roadtype = Mat_roads_indexed_renamed.groupby(['IMAGE_region','Road_class']).sum()
Mat_roads_total_by_roadtype = Mat_roads_indexed_renamed.groupby(['Road_class']).sum()
Mat_roads_total = Mat_roads_indexed_renamed.groupby(['IMAGE_region']).sum()

# Merge the two dataframes based on the 'country' index column
mat_road_area_stat = pd.merge(aad_road_area_stat, Mat_roads_country, on='country')

# Divide population by area and create a new column 'population_density'
mat_road_area_stat['kg asphalt/capita'] = mat_road_area_stat['asphalt'] / mat_road_area_stat['population']
mat_road_area_stat['kg aggregate/capita'] = mat_road_area_stat['aggregate'] / mat_road_area_stat['population']
mat_road_area_stat['kg concrete/capita'] = mat_road_area_stat['concrete'] / mat_road_area_stat['population']
mat_road_area_stat['kg cement/capita'] = mat_road_area_stat['cement'] / mat_road_area_stat['population']
mat_road_area_stat['kg brick/capita'] = mat_road_area_stat['bricks'] / mat_road_area_stat['population']
mat_road_area_stat['kg stone/capita'] = mat_road_area_stat['stone'] / mat_road_area_stat['population']

# Specify the path and filename for the Excel file
excel_file_path = 'informal_mat_road_area_stat_check.xlsx'

# Export the DataFrame to Excel
mat_road_area_stat.to_excel(excel_file_path, index=True)

#%% Aggregation on final material results per type of infrastructure

ab = brtun_df
ac = rail_res
ad = Mat_parking_country_by_roadtype
ae = Mat_roads_country_by_roadtype
af = Mat_infroads_country_by_roadtype


ab.columns = [*ab.columns[:-1], 'part']
ac.columns = [*ac.columns[:-1], 'part']
# Reset the index to make "Road_class" a regular column
ad.reset_index(level='Road_class', inplace=True)

# Replace values containing 1 with 'parking' in the "Road_class" column
ad['Road_class'] = ad['Road_class'].replace(4, 'parking')
# Move the "Road_class" column to the last position
ad = ad[[col for col in ad.columns if col != 'Road_class'] + ['Road_class']]

# Reset the index to make "Road_class" a regular column
ae.reset_index(level='Road_class', inplace=True)

# Replace values in the "Road_class" column with the specified mappings
ae['Road_class'] = ae['Road_class'].replace({1: 'Highway', 2: 'Primary', 3: 'Secondary', 4: 'Tertiary', 5: 'Local'})

# Move the "Road_class" column to the last position
ae = ae[[col for col in ae.columns if col != 'Road_class'] + ['Road_class']]

# Reset the index to make "Road_class" a regular column
af.reset_index(level='Road_class', inplace=True)

# Replace values in the "Road_class" column with the specified mappings
af['Road_class'] = af['Road_class'].replace({11: 'Bridleway', 12: 'Cycleway', 13: 'Footway', 14: 'Path', 15: 'Pedestrian', 16: 'Steps', 17: 'Tracks'})

# Move the "Road_class" column to the last position
af = af[[col for col in af.columns if col != 'Road_class'] + ['Road_class']]

ad.columns = [*ad.columns[:-1], 'part']
ae.columns = [*ae.columns[:-1], 'part']
af.columns = [*af.columns[:-1], 'part']

# Reset the second index (IMAGE_region) to make it a regular column and remove it from dataframe ad
ad.reset_index(level='IMAGE_region', inplace=True, drop=True)

# Reset the second index (IMAGE_region) to make it a regular column and remove it from dataframe ae
ae.reset_index(level='IMAGE_region', inplace=True, drop=True)

# Reset the second index (IMAGE_region) to make it a regular column and remove it from dataframe af
af.reset_index(level='IMAGE_region', inplace=True, drop=True)

# Change the name of the index in dataframe ab to "country"
ab.index.name = 'country'

# Change the name of the index in dataframe ac to "country"
ac.index.name = 'country'

# Concatenate the dataframes along the rows (vertically)
all_parts = pd.concat([ab, ac, ad, ae, af], axis=0)
unique_column_names = set(all_parts.columns)
# Sum the specified columns by their locations and store the result in a new column "Concrete"
all_parts['Concrete_2'] = all_parts.iloc[:, [0, 17, 18]].sum(axis=1)
# Sum the specified columns by their locations and store the result in a new column "Concrete"
all_parts['Aggregate_2'] = all_parts.iloc[:, [5,16]].sum(axis=1)

# Drop the specified columns by their integer locations
all_parts.drop(all_parts.columns[[0, 5, 16, 17, 18]], axis=1, inplace=True)

# Get the column you want to move (assuming it's the fifth column, change the index if needed)
column_to_move = all_parts.pop(all_parts.columns[3])
# Insert the column at the front of the DataFrame
all_parts.insert(0, column_to_move.name, column_to_move)


am_roads = 'C:\your-directory\Output\Processed\mat_road_area_stat_check.xlsx'
am_roads = pd.read_excel( am_roads,header=[0],index_col=[0])

# Get the number of columns in am_roads
num_columns_to_keep = len(am_roads.columns) - 18

# Select the first num_columns_to_keep columns and create a new DataFrame
ag_country_stats = am_roads.iloc[:, :num_columns_to_keep]

# Merge the DataFrames on the 'country' index, adding information from columns 0 and 1 from ag_country_stats to all_parts
all_parts_region = all_parts.merge(ag_country_stats.iloc[:, [0, 1]], left_index=True, right_index=True, how='left')

# Set the index of ag_country_stats to include 'GRIP-region' and 'IMAGE-region'
ag_country_stats.set_index(['GRIP-region', 'IMAGE-region'], append=True, inplace=True)

ag_country = ag_country_stats.groupby(['country']).sum()
ag_IMAGE_stats = ag_country_stats.groupby(['IMAGE-region']).sum()
ag_GRIP_stats = ag_country_stats.groupby(['GRIP-region']).sum()

all_parts_IMAGE = all_parts_region.groupby(['IMAGE-region']).sum()
all_parts_GRIP = all_parts_region.groupby(['GRIP-region']).sum()
all_parts_parts = all_parts_region.groupby(['part']).sum()
all_parts_country = all_parts_region.groupby(['country']).sum()

all_parts_IMAGE_part = all_parts_region.groupby(['IMAGE-region','part']).sum()
all_parts_country_part = all_parts_region.groupby(['country','part']).sum()
all_parts_GRIP_part = all_parts_region.groupby(['GRIP-region','part']).sum()

all_parts_country_voronoi_part = all_parts_region.groupby(['GRIP-region','country']).sum()
index_mapping = {
    1.0: 'North America',
    2.0: 'Central and South America',
    3.0: 'Africa',
    4.0: 'Europe',
    5.0: 'Middle East and Central Asia',
    6.0: 'South and East Asia',
    7.0: 'Oceania'
}

# Rename the index using the mapping
all_parts_country_voronoi_part.rename(index=index_mapping, level=0, inplace=True)

all_parts_country_sunburst_parti = all_parts_region.groupby(['IMAGE-region','country','part']).sum()


all_parts_country_sunburst_part = all_parts_region.groupby(['GRIP-region','country','part']).sum()
all_parts_country_sunburst_parti = all_parts_region.groupby(['IMAGE-region','country','part']).sum()

all_parts_cap_sunburst_part = all_parts_region.groupby(['GRIP-region','country','part']).sum()


def add_and_divide(df):
    # Create a list of columns to exclude
    exclude_columns = ['area']

    # Exclude 'GRIP-region' and 'IMAGE-region' columns if they exist
    if 'GRIP-region' in df.columns:
        exclude_columns.append('GRIP-region')
    if 'IMAGE-region' in df.columns:
        exclude_columns.append('IMAGE-region')

    # Sum the values in all columns except the excluded ones
    sum_except_excluded = df.drop(exclude_columns, axis=1).sum(axis=1)

    # Divide the sum by 1,000,000,000
    sum_except_excluded /= 1000000000

    # Add the new column to the DataFrame
    df['Total(MT)'] = sum_except_excluded

# Call the function for each of your grouped DataFrames
add_and_divide(all_parts_IMAGE)
add_and_divide(all_parts_GRIP)
add_and_divide(all_parts_parts)
add_and_divide(all_parts_country)
add_and_divide(all_parts_IMAGE_part)
add_and_divide(all_parts_country_part)
add_and_divide(all_parts_GRIP_part)

# Divide the columns in all_parts_country by the "population" column in ag_country_stats
mat_cap_country = all_parts_country.div(ag_country['population'], axis=0)
mat_cap_IMAGE = all_parts_IMAGE.div(ag_IMAGE_stats['population'], axis=0)
mat_cap_GRIP = all_parts_GRIP.div(ag_GRIP_stats['population'], axis=0)

# For mat_cap_country DataFrame
mat_cap_country['mat/cap(t)'] = mat_cap_country.iloc[:, :-3].drop(columns=['area']).sum(axis=1)

# For mat_cap_IMAGE DataFrame
mat_cap_IMAGE['mat/cap(t)'] = mat_cap_IMAGE.iloc[:, :-3].drop(columns=['area']).sum(axis=1)

# For mat_cap_GRIP DataFrame
mat_cap_GRIP['mat/cap(t)'] = mat_cap_GRIP.iloc[:, :-3].drop(columns=['area']).sum(axis=1)

# Divide the columns in all_parts_country by the "population" column in ag_country_stats
mat_area_country = all_parts_country.div(ag_country['area_x'], axis=0)
mat_area_IMAGE = all_parts_IMAGE.div(ag_IMAGE_stats['area_x'], axis=0)
mat_area_GRIP = all_parts_GRIP.div(ag_GRIP_stats['area_x'], axis=0)

# For mat_cap_country DataFrame
mat_area_country['mat/area(t)'] = mat_area_country.iloc[:, :-3].drop(columns=['area']).sum(axis=1)/1000

# Create a Pandas Excel writer using ExcelWriter
with pd.ExcelWriter('Results_analysis_cor.xlsx') as writer:
    # Write each dataframe to a different sheet in the Excel file
    all_parts_IMAGE.to_excel(writer, sheet_name='all_parts_IMAGE')
    all_parts_GRIP.to_excel(writer, sheet_name='all_parts_GRIP')
    all_parts_parts.to_excel(writer, sheet_name='all_parts_parts')
    all_parts_country.to_excel(writer, sheet_name='all_parts_country')
    all_parts_IMAGE_part.to_excel(writer, sheet_name='all_parts_IMAGE_part')
    all_parts_country_part.to_excel(writer, sheet_name='all_parts_country_part')    
    all_parts_GRIP_part.to_excel(writer, sheet_name='all_parts_GRIP_part')
    mat_cap_country.to_excel(writer, sheet_name='mat_cap_country')
    mat_cap_IMAGE.to_excel(writer, sheet_name='mat_cap_IMAGE')
    mat_cap_GRIP.to_excel(writer, sheet_name='mat_cap_GRIP')
    mat_area_country.to_excel(writer, sheet_name='mat_area_country')
    mat_area_IMAGE.to_excel(writer, sheet_name='mat_area_IMAGE')
    mat_area_GRIP.to_excel(writer, sheet_name='mat_area_GRIP')

