'''

This script is to merge and clean vegetation datasets.
It merges plant traits to species found in the pacific
northwest. Several datasets have been combined to create
this body of information. Citations for the data can be found in
the notes file.

'''

import pandas as pd
import os


os.chdir('C:\\Users\\jsg1\\Desktop\\Plant_Traits')

df = pd.read_csv('Lemma_link.csv' )
#trim appropriately
df = df.loc['species']

priorities= pd.read_csv('Priorities.csv')
#merge the two foundational data sets together
df = df.merge(priorities, how ='left', left_on='species',right_on='Species')

#read in all data sets to be merged
ch1 = pd.read_csv('Choat_et_al_2012_data.xls .csv')
ch2 = pd.read_csv('Choat_et_al_2012_xylem.csv')
leafspec = pd.read_csv('fresh-leaf-spectra-to-estimate-leaf-traits-for-california-ecosystems.csv')
wd = pd.read_csv('GlobalWoodDensityDatabase.csv')
lai = pd.read_csv('LAI_Woody_Plants_Database.csv')
nacp1 = pd.read_csv('NACP_TERRA_PNW_forest_biomass_productivity.csv')
nacp2 = pd.read_csv('NACP_TERRA_PNW_leaf_trait.csv')
le = pd.read_csv('WrightReich_leaf_economics.csv')
bark = pd.read_csv('SCBI_bark_depth.csv')
