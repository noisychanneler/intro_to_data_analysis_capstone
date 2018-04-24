#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 17:04:59 2018

@author: andrew.guindiibm.com

Capstone - CodeAcademy Introduction to Data Analysis
"""
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

species = pd.read_csv('species_info.csv')
print(species.head())

species_count = species.scientific_name.nunique()
print('Species Count: '+ str(species_count))

species_type = species.category.unique()
print('Types of Species: \n' + str(species_type))


conservation_statuses = species.conservation_status.unique()
#print(conservation_statuses)

conservation_counts = species.groupby([species.conservation_status])\
                                        .scientific_name.nunique().reset_index()
#print('\nConservation Status: \n' + str(conservation_counts))

#This shows that a rather large number of speicies are threatned threatened  
#Quite a bunch of the rest are also of concern.

species.fillna('No Intervention', inplace = True) #this piece of code is to handle missing data and 
#fill it with a value that shows its meaning instead of having a NULL or NaN Since GroupBy does not
#Include NaN or NULL values.

conservation_counts_fixed = species.groupby([species.conservation_status])\
                                        .scientific_name.nunique().reset_index()
print('\nConservation Status: \n' + str(conservation_counts_fixed))

#--------------------------------------------------------------------------#
#The following block of code is to analyze the data at hand using visualization.

protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')
    
   
fig = plt.figure(figsize=[10,4])
ax=fig.add_subplot(111)

plt.bar(range(protection_counts.scientific_name.nunique()), protection_counts.scientific_name
       )    

ax.set(xticks = range(protection_counts.conservation_status.nunique()),
       xticklabels = protection_counts.conservation_status.unique(),
       ylabel = 'Number of Species',
       title = 'Conservation Status by Species'
       )
plt.show()
plt.savefig('conservation_status_by_species.png')

species['is_protected'] = species.conservation_status != 'No Intervention'
print(species.is_protected.unique())

category_counts = species.groupby(['category', 'is_protected']).\
                                scientific_name.nunique().reset_index()

category_pivot = category_counts.pivot(columns = 'is_protected',
                                       index = 'category', 
                                       values = 'scientific_name').reset_index()

print('\nPIVOT CATEGORY TABLE:\n\n')

category_pivot.rename(columns = { False: 'not_protected', True: 'protected'}, inplace = True)

category_pivot['percent_protected'] = category_pivot.protected*100 / \
                                    (category_pivot.protected + category_pivot.not_protected)

category_pivot_sorted = category_pivot.sort_values('percent_protected',ascending=0).reset_index()
print(category_pivot_sorted)

print('\CHI SQUARED TESTING:\n\n')

#       protected       not_protected
#Mammal  ...               .....
#Bird    ...               ......
contingency = [[30,146],
               [75,413]]
x, pval_mammal_bird,y,z = chi2_contingency(contingency)
print('Pval for Mammal vs Bird Chi2 test: ' + str(pval_mammal_bird))

rep_mam_contingency = [[5,73],
                      [30,146]]

x, pval_reptile_mammal,y,z = chi2_contingency(rep_mam_contingency) 

print('Pval for Reptile vs Mammal Chi2 test: ' + str(pval_reptile_mammal))

"""
Q2 - Observations DataFrame
"""

observations = pd.read_csv('observations.csv')
print(observations.head())

species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)

species.head()

species_is_sheep = species[species.is_sheep == True]
sheep_species = species_is_sheep[species_is_sheep.category == 'Mammal']

print(sheep_species)

sheep_observations = sheep_species.merge(observations)

obs_by_park = sheep_observations.groupby(['park_name']).observations.sum().reset_index()

#--------------------------------------------------------------------------#
"""
PLOTTING SHEEP SIGHTINGS
"""

fig = plt.figure(figsize=[16,4])
ax = fig.add_subplot(111)
ax.bar(range(len(obs_by_park.observations)), obs_by_park.observations)
ax.set(xticks=range(obs_by_park.park_name.count()),
       xticklabels = obs_by_park.park_name,
      ylabel = 'Number of Observations',
      title = 'Observations of Sheep per Week')
plt.show()
plt.savefig('observations_sheep_per_week.png')
#--------------------------------------------------------------------------#
"""
FOOT AND MOUTH REDUCTION EFFORT
"""
#SAMPLE SIZE DETERMINATION

baseline = 15
minimum_detectable_effect = 33.3
level_of_confidence = 90.0
sample_size_per_variant = 510 #Using a sample size calculator at 90% confidence

yellowstone_weeks_observing = 510/507.0
bryce_weeks_observing = 510/250.0

