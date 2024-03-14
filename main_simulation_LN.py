from LN_Model import LN_Model
from filter import filter_alpha_norm, filter_biphasic_norm
from convolutions import convolve_1D
from dynamical_systems import IPL_rectified, IPL_rectified_occupancy, IPL_rectified_occupancy_nV,IPL_occupancy,IPL
from nonlinearities import N
from utils import  make_param_dict, save_dict,save_fig,make_directory
from stimuli import impulse_stimulus, step_stimulus,periodic_flashes_fixed_luminance
from load_data import get_euler_stimulus
from simulate import simulate_OSR
from matplotlib.backends import backend_pdf
from matplotlib import pyplot as plt
import os
import numpy as np
import json

#name the simulation
folder_name = 'params_final_LN_stimnorm'

#True if load and existing dataset and not create a new one
load_params = False


#choose which functions to use 
linear_filter = filter_biphasic_norm
nonlinearity = N
convolution_type = 'same'
polarities = ['ON']
occupancy = 'fixed'
stimnorm = False

#hyperparameter
dt = 0.002
filterlength = 1



#model parameter 
scale_mV = 0.05 # [mV]


#time constants
tau_B_init = 0.08       # [s]
tau_A1_init = 0.08       # [s]
tau_A2_init = 0.12       # [s]
tau_G_init = 0.06        # [s]
tau_VR = 0.02 


#weights
wB_init = 15.0             # [1/s]
wA1_init = -18.0 #-90.0    #20.8   # [1/s]
wA2_init = 0 # -80.0     #10.0  # [1/s]



#thresholds 
theta_A1_init =    0 #-1 * scale_mV     # [mV]
theta_A2_init =    -1 * scale_mV     # [mV]

#nonlinearity
slope = 200
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

params_model['SFA2'] = params_model['SFA2'] * (180/50)

model_functions = { 'linear_filter' : f'{linear_filter}',      
                    'nonlinearity' : f'{nonlinearity}'}

print(model_functions)

hyperparameter = {'dt' : dt,
                    'filterlength' : filterlength,
                    "polarities" : polarities }




params = { "params_model": params_model,
            "model_functions" : model_functions,
            "hyperparameter" : hyperparameter}




# create folder automatically and load parameterset
filepath = "/user/sebert/home/Documents/Simulations/osr_model/"
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

Model = LN_Model(linear_filter = linear_filter,      
                 convolution = convolve_1D,
                 nonlinearity = nonlinearity,
                 convolution_type = convolution_type,
                 stimnorm = stimnorm,

                 params = params_model,
                 
                 polarities = polarities,
                 filterlength = filterlength,
                 dt = dt)


kernel_fig = Model.plot_kernels()
save_fig(f'{filepath_paramset}/kernels.png',kernel_fig)




# ============================================================================================
# simulate and save impulse response
# ============================================================================================


simulation_name = 'impulse'

#TODO save hyperparameter for every simulation

print(f'{simulation_name} simulation')

stimulus,time  = impulse_stimulus(dt = dt, amplitude = 1/dt)
simulation = Model.predict(stimulus,time,simulation_name)
figure = Model.plot_response(simulation)


#TODO save in method
filename = f"simulation_{simulation['name']}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
save_dict(f'{filepath_simulation}.pickle',simulation)
save_fig(f'{filepath_simulation}.png',figure)




# ============================================================================================
# simulate and save chirp response
# ============================================================================================

simulation_name = 'chirp'

#TODO save hyperparameter for every simulation

print(f'{simulation_name} simulation')
stimulus,time  = get_euler_stimulus(dt=dt)
print(len(stimulus))
print(len(time))
simulation = Model.predict(stimulus,time,simulation_name)
figure= Model.plot_response(simulation,xlims = (0,30))


#TODO save in method
filename = f"simulation_{simulation['name']}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
save_dict(f'{filepath_simulation}.pickle',simulation)
save_fig(f'{filepath_simulation}.png',figure)



# ============================================================================================
# simulate and save osr response 12 flashes
# ============================================================================================

fn = 12 
frequencies = np.array([6,8,10,12,16])
periods = 1/frequencies

osrparams = {'flashnumber' : fn,
            'frequencies' : frequencies,
            'periods' : periods}


simulation_name = 'osr'
print(f'{simulation_name} simulation')
filename = f"simulation_{simulation_name}_{fn}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt, xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle', show = True)
# TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()



# ============================================================================================
# simulate and save osr response 12 flashes with variable flashduration
# ============================================================================================

fn = 12 
frequencies = np.array([6,8,10,12,16])
periods = 1/frequencies

osrparams = {'flashnumber' : fn,
            'frequencies' : frequencies,
            'periods' : periods}


simulation_name = 'osr_variable_flashduration'
print(f'{simulation_name} simulation')
filename = f"simulation_{simulation_name}_{fn}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt, xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle', show = True, fdtype='vary')
# TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()






# ============================================================================================
# simulate and save osr response 12 flashes with equal luminance stim from data
# ============================================================================================

fn = 12 
frequencies = np.array([6,8,10,12,16])
periods = 1/frequencies

osrparams = {'flashnumber' : fn,
            'frequencies' : frequencies,
            'periods' : periods}


simulation_name = 'osr_equal_luminance_datastim'
print(f'{simulation_name} simulation')
filename = f"simulation_{simulation_name}_{occupancy}_{fn}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
stimfie = '/user/sebert/home/Documents/Experiments/OSR/Results/Luminance/20230523_Thomas2/plot_stimulus.csv'

osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,periodic_flashes_fixed_luminance,
                dt = dt, xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle', show = False)
# TODO make figure 


# ============================================================================================
# simulate and save osr response 5 flashes
# ============================================================================================

fn = 5 
frequencies = np.array([6,8,10,12,16])
periods = 1/frequencies

osrparams = {'flashnumber' : fn,
            'frequencies' : frequencies,
            'periods' : periods}


simulation_name = 'osr'
print(f'{simulation_name} simulation')
filename = f"simulation_{simulation_name}_{fn}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt,xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle')
# TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()





# ============================================================================================
# simulate and save osr response 25 flashes
# ============================================================================================

fn = 25 
frequencies = np.array([6,8,10,12,16])
periods = 1/frequencies

osrparams = {'flashnumber' : fn,
            'frequencies' : frequencies,
            'periods' : periods}


simulation_name = 'osr'
print(f'{simulation_name} simulation')
filename = f"simulation_{simulation_name}_{fn}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt,xlims = (1.9,7),filepath = f'{filepath_simulation}.pickle')
# TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()




# ============================================================================================
# simulate and save osr response different  flashnumbers
# ============================================================================================

flashnumbers = np.array([2,3,4,6,7,8,9,10,11,13,14,15,16,17,18,19,20])
frequencies = np.array([6,8,10,12,16])
periods = 1/frequencies

for fn in flashnumbers:

    osrparams = {'flashnumber' : fn,
                'frequencies' : frequencies,
                'periods' : periods}


    simulation_name = 'osr'
    print(f'{simulation_name} simulation')
    filename = f"simulation_{simulation_name}_{fn}"
    filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


    osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt,xlims = (1.9,7),filepath = f'{filepath_simulation}.pickle')
# TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()



# ============================================================================================
# simulate and save response to one short flash 
# ============================================================================================


simulation_name = 'short_flash'

#TODO save hyperparameter for every simulation

print(f'{simulation_name} simulation')

stimulus,time  = step_stimulus(start = 1, stop = 1.04, dt = dt, amplitude = -1)
simulation = Model.predict(stimulus,time,simulation_name)
figure = Model.plot_response(simulation)


#TODO save in method
filename = f"simulation_{simulation['name']}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
save_dict(f'{filepath_simulation}.pickle',simulation)
save_fig(f'{filepath_simulation}.png',figure)


# TODO make simulation to one long flash
# ============================================================================================
# simulate and save response to a long flash
# ============================================================================================

simulation_name = 'long_flash'

#TODO save hyperparameter for every simulation

print(f'{simulation_name} simulation')

stimulus,time  = step_stimulus(dt = dt, amplitude  = -1)
simulation = Model.predict(stimulus,time,simulation_name)
figure = Model.plot_response(simulation,xlims = (0.9,3))


#TODO save in method
filename = f"simulation_{simulation['name']}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
save_dict(f'{filepath_simulation}.pickle',simulation)
save_fig(f'{filepath_simulation}.png',figure)
