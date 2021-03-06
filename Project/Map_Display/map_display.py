# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 13:07:09 2018

@author: Weinan(Eric) Li. w3li@ucsd.edu
"""

#requires pygal,pygal_maps_world,pandas,numpy

import pygal.maps.world
from IPython.display import SVG
from Project.Data_Cleaning import clean_data

def display(data,feature,year):
    '''
    Takes a CleanData object "data", a "feature" from this dataset other than Country
    or Year, and a specific year. On a world map, draws how this feature is distributed
    in the given year. The year should not be outside the range of the dataset.
    
    param: data     type: CleanData object
    param: feature  type: str
    param: year     type: int
    '''
    from pygal_maps_world.i18n import COUNTRIES
    
    assert isinstance(data, clean_data.CleanData)
    
    assert isinstance(feature,str)
    valid_features = list(data.modified.columns)
    valid_features.remove('Country')
    valid_features.remove('Year')
    assert feature in valid_features
    
    assert isinstance(year,int)
    modified = data.modified
    assert modified.Year.min() <= year <= modified.Year.max()   
    
    #match the country codes
    countries={value:key for key, value in COUNTRIES.items()}
    countries['United States of America']='us' # there're more needs to manually match
    
    display_data=dict()
    
    for i in range(modified.shape[0]):
        row=modified.loc[i]
        if row['Year']==year:
            countryname=row['Country']
            display_feature=row[feature]
            try:
                display_data[countries[countryname]]=display_feature
            except:
                pass
    
    #colors need to be adjusted for clearer display
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = '{0} in the year {1}'.format(feature,year)
    worldmap_chart.add('In {0}'.format(year), display_data)
    
    return SVG(worldmap_chart.render())