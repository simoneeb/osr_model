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
folder_name = 'params_exploration_weight'

load_params = False


#choose which functions to use 
linear_filter = filter_alpha_norm
system =  IPL_occupancy
nonlinearity = N
occupancy = 'dynamic'
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
tau_G_init = 0.06        # [s]
tau_VR = 0.02 

#weights
wB_init = 50.0             # [1/s]
wA1_init = -60 # -60.0    #20.8   # [1/s]
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
filepath = "/user/sebert/home/Documents/Simulations/osr_model/explore_weight_params"
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
tau_ns = np.round(np.arange(0.005,0.05,0.001),3)
weights = np.arange(0,100,1) * -1
k_rec = 1
# range of beta
beta = 126
# calculate analytically 
def calc_n_f(krel,krec,bet,frec):
    return krec/(krec+krel*bet*frec)


Model.modify_params('k_rec',k_rec)
Model.modify_params('beta',beta)


df = pandas.DataFrame(columns = ['w_A1','k_rec', 'k_rel', 'k_ratio', 'beta', 'tau_n', 'slope', 'n_diff','n_diff_calc'])


for tau_n in tau_ns:
    print(f'tau_n {tau_n}')
    for w_A1 in weights: 
        print(f'w_A1 {w_A1}')
        k_rel = (1/tau_n/beta)-(k_rec/beta)
        k_ratio = k_rec/k_rel

        simulation_name = f'osr_tau_n_{tau_n}_w_A1_{w_A1}'
        print(f'{simulation_name} simulation')
        filename = f"simulation_{simulation_name}"
        filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


        # TODO use Model.modify_params
        Model.modify_params('k_rel',k_rel)
        Model.modify_params('w_A1',w_A1)

        osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt, xlims = (1.9,5), filepath = f'{filepath_simulation}.pickle', show = False, print_steps = False)



        # get slope 
        slope = osr_simulation['slope']

        # measure n_diff
        n_diff = osr_simulation['maxs_n'][0] - osr_simulation['maxs_n'][-1]

        n_calcs = calc_n_f(k_rec,k_rel,beta,frequencies)
        n_diff_calc = n_calcs[0]-n_calcs[-1]


        # append to df 
        df = df.append({'k_rec' : k_rec,
                    'k_rel' : k_rel,
                    'k_ratio' : k_ratio,
                    'beta' : beta,
                    'tau_n' : tau_n,
                    'w_A1': w_A1,
                    'slope' : slope,
                    'n_diff' : n_diff,
                    'n_diff_calc' : n_diff_calc},
                    ignore_index=True)



# save the dataframe
df.to_csv(f'{filepath}/DataFrame_weight_params_slope_effect.csv')


