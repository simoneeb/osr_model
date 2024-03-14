

import matplotlib.pyplot as plt
import numpy as np
import random
import os
import pandas as pd
import h5py
from scipy.ndimage import gaussian_filter
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy import stats

import pickle
import itertools








# functions to load data 


#load osr info
def get_OSR_response(cell,experiment_name,experimenter, IDs, drug):
    
    filename = f"/user/sebert/home/Documents/Experiments/Results/{experiment_name}_{experimenter}/resultfiles/{experiment_name}_osr_raster_count_peak_slope.pkl"
    with open(filename, "rb") as handle:   #Pickling
        osrdict = pickle.load(handle)
        
    key = f'temp_{cell}'
    
    responses_control = []
    responses_strychnine = []
    rasters_control = []
    rasters_strychnine = []
    osr_times = []
    flashstarts = []
    flashends = []
    lastflashends = []
    peaks_control = []
    peaks_strychnine = []
    
    for ID in IDs:
        
        #get responses
        responses_control.append(osrdict[key]['control'][ID]["rate_smoothed"])
        responses_strychnine.append(osrdict[key][drug][ID]["rate_smoothed"])
        
        rasters_control.append(osrdict[key]['control'][ID]["rasters"])
        rasters_strychnine.append(osrdict[key][drug][ID]["rasters"])

        #get plotting stuff
        flashstarts.append(osrdict['stimulus_info'][ID]['flashstart'])
        flashends.append(osrdict['stimulus_info'][ID]['flashend'])
        osr_times.append(osrdict['stimulus_info'][ID]["osr_time"])
        lastflashends.append(osrdict['stimulus_info'][ID]["lastflashend"])
        peaks_control.append(osrdict[key]['control'][ID]["peak"])
        peaks_strychnine.append(osrdict[key][drug][ID]["peak"])
        
    return [responses_control,
            responses_strychnine,
            rasters_control,
            rasters_strychnine,
            osr_times,
            flashstarts,
            flashends,
            lastflashends,
            peaks_control,
            peaks_strychnine]
        

    
    
      
    
# load data of slopes from manually detected peaks
def get_slope_data(cell,experiment_name,experimenter, fn = None):
    filename = f"/user/sebert/home/Documents/Experiments/Results/{experiment_name}_{experimenter}/resultfiles/{experiment_name}_manual_slopes.pkl"
    with open(filename, "rb") as handle:   #Pickling
        slopedict = pickle.load(handle)
    
    key = f'temp_{cell}'

    if fn is None:
        out = [slopedict[key]['slope_control'],
        slopedict[key]['slope_strych'],
                
        slopedict[key]['peaks_control'],
        slopedict[key]['peaks_strych'],
        
        slopedict[key]['offset_control'],
        slopedict[key]['offset_strych'],
        
        slopedict[key]['amps_control'],
        slopedict[key]['amps_strych']]

    else: 
        out = [slopedict[f'{fn} Flashes'][key]['slope_control'],
        slopedict[f'{fn} Flashes'][key]['slope_strych'],
                
        slopedict[f'{fn} Flashes'][key]['peaks_control'],
        slopedict[f'{fn} Flashes'][key]['peaks_strych'],
        
        slopedict[f'{fn} Flashes'][key]['offset_control'],
        slopedict[f'{fn} Flashes'][key]['offset_strych'],
        
        slopedict[f'{fn} Flashes'][key]['amps_control'],
        slopedict[f'{fn} Flashes'][key]['amps_strych']]


    return out
    
    
       

#load sta info 
def get_STA_info(cell,experiment_name,experimenter):
    filename = f"/user/sebert/home/Documents/Experiments/Results/{experiment_name}_{experimenter}/resultfiles/{experiment_name}_sta_data.pkl"
    with open(filename, "rb") as handle:   #Pickling
        stadict = pickle.load(handle)


    return_dict = {}
    return_dict['temporal'] = stadict['temporal'][cell]
    return_dict['spatial'] = stadict['spatial'][cell]
    return_dict['polarity'] = stadict['polarity'][cell]
    return_dict['is_STA'] = stadict['is_STA'][cell]
    return_dict['STA'] = stadict['STAs'][cell]
    return_dict['ellipse'] = stadict['ellipses'][:,:,cell]
    
    return return_dict

