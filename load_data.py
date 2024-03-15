
import os
import pickle
import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.interpolate import interp1d




def get_euler_response(cell, experiment_name):
    filename = f"/user/sebert/home/Documents/Experiments/OSR/Results/{experiment_name}_Thomas/resultfiles/{experiment_name}_euler_grade_isi.pkl"
    with open(filename, "rb") as handle:   #Pickling
        infodict = pickle.load(handle)
    
    return infodict[f'temp_{cell}']['control']['euler_count']


#load  euler stim stimulus 
def get_euler_stimulus(dt = 0.02):
    stimeuler = pd.read_csv('stimuli/chirp_luminance_profile.csv')
    euler = np.asarray(stimeuler['luminance'])
    euler = euler/euler.max()
    # euler = euler - euler.std()
    euler_time = np.arange(0,30,0.02)

    if dt == 0.02: 
        return euler,euler_time
        
    else: 
        print(dt)
        eulerfun = interp1d(euler_time,euler,fill_value="extrapolate")
        euler_time2 = np.arange(0,30,dt)
        euler2 = eulerfun(euler_time2)

        return euler2, euler_time2

    

#load osr info
def get_OSR_response(cell,experiment_name, IDs):
    
    filename = f"/user/sebert/home/Documents/Experiments/OSR/Results/{experiment_name}_Thomas/resultfiles/{experiment_name}_osr_raster_count_peak_slope.pkl"
    with open(filename, "rb") as handle:   #Pickling
        osrdict = pickle.load(handle)


    filename_slope = f"/user/sebert/home/Documents/Experiments/OSR/Results/{experiment_name}_Thomas/resultfiles/{experiment_name}_manual_slopes.pkl"
    with open(filename_slope, "rb") as handle:   #Pickling
        slopedict = pickle.load(handle)
        
    key = f'temp_{cell}'
    
    responses = []
    osr_times = []
    flashstarts = []
    flashends = []
    lastflashends = []
    peaks = []
    
    for ID in IDs:
        
        #get responses
        responses.append(osrdict[key]['control'][ID]["rate_smoothed"])

        #get plotting stuff
        
        flashstarts.append(osrdict['stimulus_info'][ID]['flashstart'])
        flashends.append(osrdict['stimulus_info'][ID]['flashend'])
        osr_times.append(osrdict['stimulus_info'][ID]["osr_time"])
        lastflashends.append(osrdict['stimulus_info'][ID]["lastflashend"])

    peaks = slopedict[key]['peaks_control']
    slope = slopedict[key]['slope_control']
    offset = slopedict[key]['offset_control']
    
    return responses,osr_times,flashstarts,flashends,lastflashends,peaks,slope,offset
        

#OSR Stim
def get_OSR_stimulus(experiment_name):
    result_filepath = f'/user/sebert/home/Documents/Experiments/Results/{experiment_name}_Thomas/resultfiles'
    plotstimulus = pd.read_csv(os.path.join(result_filepath, 'plot_stimulus.csv'), index_col = 0)
    IDs = np.array(plotstimulus.columns)
    stimulus_info = pd.read_csv(f'/user/sebert/home/Documents/Experiments/StimulusDesgin/Stimulus_JAN21_OSR_AmacrineInhibition_50Hz/stimulus_OSR_jan21ID_info.csv')
    return plotstimulus, stimulus_info, IDs



#read sta info
def get_STA(experiment_name,cell):
    filename = f'/user/sebert/home/Documents/Experiments/Results/{experiment_name}_Thomas/resultfiles/sta_data.pkl'
    with open(filename, "rb") as handle:   #Pickling
        stadict = pickle.load(handle)

    stadict.keys()

    STAs = stadict['STAs']
    rasters_check_rep = stadict['rasters_check_repeated']
    rasters_check = stadict['rasters_check']
    temporal = stadict['temporal']
    spatial = stadict['spatial']




    c = 242
    time_rf = np.flip(temporal[c])
    time_rf_smooth = gaussian_filter(time_rf,1)
    data = time_rf_smooth.copy()

    return data
