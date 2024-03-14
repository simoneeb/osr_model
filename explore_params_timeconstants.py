from BA1A2_Model import BA1A2_Model
from filter import filter_alpha_norm
from convolutions import convolve_1D
from dynamical_systems import IPL_rectified, IPL_rectified_occupancy, IPL_rectified_occupancy_nV,IPL_occupancy,IPL
from nonlinearities import N
from utils import  make_param_dict, save_dict,save_fig,make_directory
from stimuli import impulse_stimulus, step_stimulus
from load_data import get_euler_stimulus
from simulate import simulate_OSR
from matplotlib.backends import backend_pdf
from matplotlib import pyplot as plt
import os
import numpy as np
import json
import pandas 
import seaborn as sns

#name the simulation
folder_name = 'params_exploration_timeconstants'

load_params = False


#choose which functions to use 
linear_filter = filter_alpha_norm
system =  IPL
nonlinearity = N
occupancy = 'fixed'
convolution_type = 'same'
polarities = ['ON', 'OFF', 'ON']


#hyperparameter
dt = 0.002
filterlength = 1



#model parameter 
scale_mV = 0.05 # [mV]


#time constants
tau_B_init = 0.05        # [s]
tau_A1_init = 0.08      # [s]
tau_A2_init = 0.08       # [s]
tau_G_init = 0.10      # [s]
tau_VR = 0.05

#weights
wB_init = 50.0             # [1/s]
wA1_init = 0 # -60.0    #20.8   # [1/s]
wA2_init =  -80 # -80.0     #10.0  # [1/s]



#thresholds 
theta_A1_init =    0 #-1 * scale_mV     # [mV]
theta_A2_init =    -1 * scale_mV     # [mV]

#nonlinearity
slope = 2200
threshold = 0


#occupancy
k_rel_init = 10.0             # [1/s]
k_rec_init = 10.0              # [1/s]
beta_init = 15





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
                     "threshold" : threshold }



params_model = make_param_dict(params_init)


model_functions = { 'linear_filter' : f'{linear_filter}',      
                    'system'  : f'{system}',
                    'nonlinearity' : f'{nonlinearity}'}

print(model_functions)

hyperparameter = {'dt' : dt,
                    'filterlength' : filterlength,
                    'occupancy' : occupancy,
                    "polarities" : polarities }




params = { "params_model": params_model,
            "model_functions" : model_functions,
            "hyperparameter" : hyperparameter}




# create folder automatically and load parameterset
filepath = "/user/sebert/home/Documents/Simulations/osr_model/explore_timeconstants_params"
filepath_paramset = make_directory(filepath,folder_name)



if load_params is True:
    with open(f'{filepath_paramset}/params.json') as json_file:
        params = json.load(json_file)
        print(params)


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
                 params = params_model,
                 polarities = polarities,
                 filterlength = filterlength,
                 dt = dt)


# kernel_fig = Model.plot_kernels()
# save_fig(f'{filepath_paramset}/kernels.png',kernel_fig)



fn = 20
frequencies = np.array([6,8,10,12,16])
periods = 1/frequencies

osrparams = {'flashnumber' : fn,
            'frequencies' : frequencies,
            'periods' : periods}


print('Model ceated')


# ============================================================================================
# simulate and calculate n_eq for a range of values for k_rel and k_rec
# ============================================================================================



# range of k_rel 
tau_Bs = np.round(np.arange(0.01,0.3,0.02),2)
tau_A2s =np.round(np.arange(0.01,0.3,0.02),2) 

w_ratios = np.round(np.concatenate((np.arange(0.5,1,0.1),np.arange(1,2,0.1))),1)
w_B = 100

df = pandas.DataFrame(columns = ['tau_B', 'tau_A2', 'w_B', 'w_A2','w_ratio', 'slope', 'delay_16Hz'])
for tau_B in tau_Bs:
    print(f'tau_B {tau_B}')
    for tau_A2 in tau_A2s: 
        print(f'tau_A2 {tau_A2}')
        for w_ratio in w_ratios: 
            print(f'w_ratio {w_ratio}')
            

            w_A2 = w_B * w_ratio *-1

            simulation_name = f'osr_tau_B_{tau_B}_tau_A2_{tau_A2}_w_B_{w_B}_w_A2_{w_A2}'
            print(f'{simulation_name} simulation')
            filename = f"simulation_{simulation_name}"
            filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


            # TODO use Model.modify_params
            Model.modify_params('tau_B',tau_B)
            Model.modify_params('tau_A2',tau_A2)
            Model.modify_params('w_B',w_B)
            Model.modify_params('w_A2',w_A2)

            osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt, xlims = (1.9,5), filepath = f'{filepath_simulation}.pickle', show = False, print_steps = False)

            delay = osr_simulation['delays'][-1]


            # get slope 
            slope = osr_simulation['slope']


            # append to df 
            df = df.append({
                        'slope' : slope,
                        'delay_16Hz' : delay, 
                        'tau_B' : tau_B,
                        'tau_A2' : tau_A2, 
                        'w_B' : w_B, 
                        'w_A2' : w_A2,
                        'w_ratio' : w_ratio},
                        ignore_index=True)



# save the dataframe
df.to_csv(f'{filepath}/DataFrame_timeconstants_params_slope_effect.csv')


