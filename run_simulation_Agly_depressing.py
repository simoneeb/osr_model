from BA1A2_Model import BA1A2_Model
from filter import filter_alpha_norm
from convolutions import convolve_1D
from dynamical_systems import IPL_rectified, IPL_rectified_occupancy, IPL_rectified_occupancy_nV,IPL_occupancy,IPL,IPL_occupancy_shunting
from nonlinearities import N
from utils import  make_param_dict, save_dict,save_fig,make_directory
from stimuli import impulse_stimulus, step_stimulus, periodic_flashes_fixed_luminance, periodic_flashes_variable_flashlength
from load_data import get_euler_stimulus
from simulate import simulate_OSR
from matplotlib.backends import backend_pdf
from matplotlib import pyplot as plt
import os
import numpy as np
import json


# filepath for simulations to be saved
filepath = 'output'

#name the simulation
folder_name = 'params_final_nonlin_fixed'


#True if load and existing dataset and not create a new one
load_params = False
load_folder_name = 'params_final_nonlin'


#choose which functions to use 
linear_filter = filter_alpha_norm
system =  IPL_rectified_occupancy
nonlinearity = N
occupancy = 'dynamic'
convolution_type = 'VR'
polarities = ['ON', 'OFF', 'ON']
stimfunction ='sigmoid_late'


#hyperparameter
dt =  0.002      # [s]  
filterlength = 1 # [s] 

#model parameter 
scale_mV = 20 # [mV] #


#time constants
tau_B_init =  0.08   # [s]
tau_A1_init = 0.085  # [s]
tau_A2_init = 0.12    # [s]
tau_G_init =  0.11   # [s]
tau_VR =      0.0030 # [s] 


#weights
wB_init =  50.           # [1/s]

wA1_init = -53.       # [1/s]
wA2_init = -65.       # [1/s]

# wA1_init = 0.     # [1/s]  # use to simulate strychnine
# wA2_init = -42.   # [1/s]  # use to simulate strychnine

#thresholds 
theta_A1_init =    0     * scale_mV     # [mV]
theta_A2_init =    -1. * scale_mV     # [mV]

#nonlinearity
slope = 12       # [Hz/mV] 
threshold = 0.0  # [mV]

slope_on = 14      # [1]
threshold_on = -.5 # [1]
max_val_on = 1     # [1]

slope_off = 12     # [1]
threshold_off = .5 # [1]
max_val_off = 1    # [1]

#occupancy
k_rel_init = 10.0    # [1/s]
k_rec_init = 10.0   # [1/s]
beta_init =  0.086 # [1/mV]

# beta_init =  0.0 # [1/mV]   # use to simulate model without dynamical synapse

cm = 0.1 # [nF]


# ============================================================================================
# set up folder and parameter dictionary
# ============================================================================================


params_init = {'tau_B': tau_B_init,
                     'tau_A1':tau_A1_init,
                     'tau_A2':tau_A2_init,
                     'tau_G':tau_G_init,
                     'tau_VR':tau_VR,
                     'w_B':wB_init,
                     'w_A1':wA1_init,
                     'w_A2':wA2_init,

                     'theta_A1':theta_A1_init,  
                     'theta_A2':theta_A2_init, 
    
                     'k_rec':k_rec_init,
                     'k_rel':k_rel_init,
                     'beta':beta_init,

                     'scale_mV':scale_mV,
                     "slope": slope,
                     "threshold" : threshold, 

                     "slope_on": slope_on,
                     "threshold_on" : threshold_on, 
                     "max_val_on" : max_val_on, 
                      
                     "slope_off": slope_off,
                     "threshold_off" : threshold_off, 
                     "max_val_off" : max_val_off, 
                      
                      "cm" : cm }

params_model = make_param_dict(params_init)

model_functions = { 'linear_filter' : f'{linear_filter}',      
                    'system'  : f'{system}',
                    'nonlinearity' : f'{nonlinearity}'}

hyperparameter = {'dt' : dt,
                    'filterlength' : filterlength,
                    'occupancy' : occupancy,
                    "polarities" : polarities }

params = { "params_model": params_model,
            "model_functions" : None,
            "hyperparameter" : hyperparameter}



# create folder automatically and load parameterset


if load_params is True:
    filepath_paramset = make_directory(filepath, load_folder_name)
    with open(f'{filepath_paramset}/params.json') as json_file:
        params = json.load(json_file)
        print(params)

        params_model = params['params_model']

filepath_paramset = make_directory(filepath,folder_name)

#save parameter as json file 
with open(f'{filepath_paramset}/params.json', 'w') as outfile:
    json.dump(params, outfile, indent = 4)



# ============================================================================================
# create the mdoel
# ============================================================================================

Model = BA1A2_Model(linear_filter = linear_filter,      
                 convolution = convolve_1D,
                 system  = system,
                 nonlinearity = nonlinearity,
                 occupancy = occupancy,
                 convolution_type = convolution_type,
                 stimfunction=stimfunction,


                 params = params_model,
                 
                 polarities = polarities,
                 filterlength = filterlength,
                 dt = dt)


kernel_fig = Model.plot_kernels()
sig = Model.plot_sigmoid_late()
Model.show_params()
save_fig(f'{filepath_paramset}/kernel.png',kernel_fig)
save_fig(f'{filepath_paramset}/nonlinearites.png',sig)



# ============================================================================================
# simulate and save osr response 12 flashes
# ============================================================================================

fn = 12 
frequencies = np.array([6,8,10,12,16])
periods = 1/frequencies

osrparams = {'flashnumber' : fn,
            'frequencies' : frequencies,
            'periods' : periods}


simulation_name = f'osr_{fn}'
print(f'{simulation_name} simulation')
filename = f"simulation_{simulation_name}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt, xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle', show = False)



# ============================================================================================
# simulate and save osr response 12 flashes with variable flashduration
# ============================================================================================

fn = 12 
frequencies = np.array([6,8,10,12,16])
periods = 1/frequencies

osrparams = {'flashnumber' : fn,
            'frequencies' : frequencies,
            'periods' : periods}


simulation_name = 'osr_duration'
print(f'{simulation_name} simulation')
filename = f"simulation_{simulation_name}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model, periodic_flashes_variable_flashlength,
                dt = dt, xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle', show = False)



# ============================================================================================
# simulate and save osr response 12 flashes with equal luminance stim from data
# ============================================================================================

fn = 12 
frequencies = np.array([6,8,10,12])
periods = 1/frequencies

osrparams = {'flashnumber' : fn,
            'frequencies' : frequencies,
            'periods' : periods}


simulation_name = 'osr_intensity'
print(f'{simulation_name} simulation')
filename = f"simulation_{simulation_name}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")

osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model, periodic_flashes_fixed_luminance,
                dt = dt, xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle', show = False)


# ============================================================================================
# simulate and save osr response 5 flashes
# ============================================================================================

fn = 5 
frequencies = np.array([6,8,10,12,16])
periods = 1/frequencies

osrparams = {'flashnumber' : fn,
            'frequencies' : frequencies,
            'periods' : periods}


simulation_name = f'osr_{fn}'
print(f'{simulation_name} simulation')
filename = f"simulation_{simulation_name}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt,xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle')



# # ============================================================================================
# # simulate and save response to a long dark flash with different lumincance levels 
# # ============================================================================================

# from smallest lumninance step (corresponding to low frequency) to high step (correspinding to fast frequency)
lums_experiment = [118,108,98,85,77,64,43] #luminance levels used in experiment, 128 being  grey background and 0 being black
lums_experiment = [98,85,77,64,43] # luminance levels used in experiment, 128 being  grey background and 0 being black, only the ones shown in the paper

range_exp = [0,255]

lum_norm = []
for lum in lums_experiment:
    lum_norm.append(2*(lum/range_exp[1])-1)

simulations={}

for i,lum in enumerate(lum_norm): 
    simulation_name = f'long_flash_lum_{lum}'

    #TODO save hyperparameter for every simulation

    print(f'{simulation_name} simulation')

    stimulus,time  = step_stimulus(dt = dt, amplitude  = lum)
    simulation = Model.predict(stimulus,time,simulation_name)

    simulations[f'lum_{lum}'] = simulation
    simulations[f'lum_{lum}']['stimend'] = 2
   
filename = f"simulations_step_dimming"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")

save_dict(f'{filepath_simulation}.pickle',simulations)




# # ============================================================================================
# # simulate and save response to a long dark flash with differnet durations
# # ============================================================================================

# from long (corresponding to low frequency) to short (corresponding to fast frequency)
durs_experiment = np.asarray([2.03,1.43, 1.19, 0.95, 0.71])

simulations = {}
for i,dur in enumerate(durs_experiment): 
    simulation_name = f'long_flash_dur_{dur}'

    #TODO save hyperparameter for every simulation

    print(f'{simulation_name} simulation')

    stimulus,time  = step_stimulus(length = 5, start = 1, stop = 1+dur, dt = dt, amplitude  = -1)
    simulation = Model.predict(stimulus,time,simulation_name)
    
    simulations[f'dur_{dur}'] = simulation
    simulations[f'dur_{dur}']['stimend'] = 1+dur

filename = f"simulation_step_duration"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")

save_dict(f'{filepath_simulation}.pickle',simulations)

