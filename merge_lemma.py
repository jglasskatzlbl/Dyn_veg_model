'''

This script is to merge and clean vegetation datasets.
It merges plant traits to species found in the pacific
northwest. Several datasets have been combined to create
this body of information. Citations for the data can be found in
the notes file.

'''

import pandas as pd
import os
import numpy as np


os.chdir('/Users/jsg1/Desktop/Plant_Traits')

lemma = pd.read_csv('Lemma_link.csv' )
#trim appropriately
sp = lemma['species']
sp = sp[:95].append(sp[ 96:])

#Get names right
x= []
for spec in sp:
    t = spec.split('/')
    g =spec.split()
    if len(t) > 1:
        for n in range(1,len(t)):
            x.append(t[0])
            x.append((g[0] + ' ' + t[n]))
    elif len(g)>2:
        x.append((g[0]+ ' '+ g[1]))
        x.append((g[0]+ ' '+ g[3]))
    else:
        x.append(spec)

#Bind into new dataframe
df = pd.DataFrame({'Species':x})
df.shape
#read in the bulk of work
priorities= pd.read_csv('Priorities.csv')
#clean names
priorities.iloc[0,0] = 'Pinus'
priorities.iloc[33,0] = 'Quercus'
#fix capitalization
priorities.loc[:,'Species'] = priorities.Species.str.capitalize()

#merge the two foundational data sets together
df = df.merge(priorities, how ='left', on = 'Species')
df.shape
#check performance of the merge
#df.isna().sum()
#No AGB matches?? Will need to correct later. At min, have AGB eq's for general
#can add in later
#Cols w/matches >1:
    #BAT, maxheight, latosa, p50, leaf long, slatop, wood density,
#read in all data sets to be merged
ch = pd.read_csv('Choat_et_al_2012_data.xls .csv')
wd = pd.read_csv('GlobalWoodDensityDatabase.csv')
nacp1 = pd.read_csv('NACP_TERRA_PNW_forest_biomass_productivity.csv', skiprows =range(1,2))
nacp2 = pd.read_csv('NACP_TERRA_PNW_leaf_trait.csv', skiprows =range(1,2))
le = pd.read_csv('WrightReich_leaf_economics.csv', skiprows = range(0,10))

#merge in the first of the data sets
df = df.merge(ch, how='left', on = 'Species')
df.shape
#clean it up
df = df.dropna(axis = 'columns',how='all')
#prep wood density
wd = wd.rename(index=str, columns={'Unnamed: 2': 'Species', 'Unnamed: 3': 'Wood_Density'})
wd = wd[['Species','Wood_Density']]
wd = wd.groupby('Species').agg({'Wood_Density':'mean'})
#merge then drop duplicates
df = df.merge(wd, how='left', on = 'Species')
df.shape
df['wood_density'] = df['wood_density'].fillna(df['Wood_Density'])
df = df.drop(['Wood_Density'], axis = 'columns')

#nacp can be worked together

nacp2['Species'] = nacp2['GENUS'] + ' ' + nacp2['SPECIES']

ncdic = {'PINPON':'Pinus ponderosa', 'LAROCC':'Larix occidentalis', 'ABIGRA':'Abies grandis',
         'PSEMEN':'Pseudotsuga menziesii', 'PICSIT':'Picea sitchensis', 'TSUHET':'Tsuga heterophylla',
       'ABIPRO':'Abies procera', 'ABIAMA':'Abies amabilis', 'PINCON':'Pinus contorta',
       'THUPLI':'Thuja plicata', 'JUNOCC':'Juniperus occidentalis', 'ABICON':'Abies concolor',
       'ABILAS':'Abies lasiocarpa', 'PICENG':'Picea engelmannii', 'QUECHR':'Quercus chrysolepis',
       'PINJEF':'Pinus jeffreyi', 'PINMON':'Pinus monticola', 'ABIMAG':'Abies magnifica',
       'CALDEC':'Calocedrus decurrens'}

nacp1['Species'] = nacp1['SPP_O1_ABBREV'].replace(ncdic)
#Here we are using just the main species group for each clump.
#Alternatives may include doing weighted averages
#I have not found an effective way for seperating each.
#The fraction of basal area for each species is available
#For now drop all those with main species fractions less than 80
nacp1 = nacp1.loc[pd.to_numeric(nacp1['SPP_O1_BASAL_AREA_FRACTION'], errors ='coerce')>79]
#may want to replace with na instead
nacp1 = nacp1.replace(to_replace =-9999,value =np.NaN)
#Get means
nacp_1 = nacp1.groupby('Species').agg({ 'LAI_O' : 'mean',
 'HEIGHTC':'mean',
 'AG_BIOMASS_TREE_WOOD_AS_CARBON':'mean',
 'AG_BIOMASS_TREE_FOLIAGE_AS_CARBON':'mean',
 'AG_BIOMASS_TREE_TOTAL_AS_CARBON':'mean',
 'AG_PROD_TREE_WOOD_AS_CARBON':'mean',
 'AG_PROD_TREE_FOLIAGE_AS_CARBON':'mean',
 'AG_PROD_TREE_TOTAL_AS_CARBON':'mean'})
#Set the ref
nacp_1['reference'] = 'NACP_TERRA_bp'
#merge it in
df = df.merge(nacp_1, how = 'left', on = 'Species')
df.shape

#now add in nacp2
nacp2 = nacp2.replace(to_replace =-9999,value =np.NaN)
nacp_2 = nacp2.groupby('Species').agg({ 'LEAF_PSA':'mean',
 'PSA_to_HSA':'mean',
 'LEAF_HSA':'mean',
 'LEAF_DRY_WT':'mean',
 'LEAF_CARBON_WT':'mean',
 'SLA_PSA':'mean',
 'SLA_HSA':'mean',
 'LEAF_CARBON':'mean',
 'LEAF_NITROGEN':'mean',
 'LEAF_CN':'mean',
 'LEAF_LIFE':'mean'})

nacp_2['reference'] = 'NACP_TERRA_lt'

df = df.merge(nacp_2, how = 'left', on = 'Species')
df.shape

#Add in leaf economics
le1 = le.groupby('Species').mean()
le1['reference'] = 'WrightReich'
df = df.merge(le1, how = 'left', on = 'Species')
df.shape
