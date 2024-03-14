from B_Model import B_Model
from filter import filter_alpha_norm, filter_biphasic_norm, filter_biphasic_norm
from convolutions import convolve_1D
from dynamical_systems import IPL_rectified, IPL_rectified_occupancy, IPL_rectified_occupancy_nV,IPL_occupancy_bipolar,IPL
from nonlinearities import N
from utils import  make_param_dict, save_dict,save_fig,make_directory
from stimuli import impulse_stimulus, step_stimulus,periodic_flashes_fixed_luminance,periodic_flashes_variable_flashlength
from load_data import get_euler_stimulus
from simulate import simulate_OSR
from matplotlib.backends import backend_pdf
from matplotlib import pyplot as plt
import os
import numpy as np
import json


#name the simulation
folder_name = 'bipolar_only/params_final_biphasic_nonlin'
#folder_name = 'params_manual_N_fixed_OFF_dt0.002_strychnine_wA240_slope'


#True if load and existing dataset and not create a new one
load_params = False


linear_filter = filter_biphasic_norm
system =  IPL_occupancy_bipolar
nonlinearity = N
occupancy = 'dynamic'
convolution_type = 'VR'#'same'
polarities = ['ON', 'OFF', 'ON']
stimfunction = 'sigmoid_late'


#hyperparameter
dt = 0.002
filterlength = 1


#model parameter 
scale_mV = 0.05 # [mV]


#time constants
tau_B_init = 0.1        # [s]
tau_A1_init = 0.08      # [s]
tau_A2_init = 0.2       # 0.27   # [s]
tau_G_init = 0.05       # 0.04     # [s]
tau_VR = 0.1            # 0.02 
tau_VR2 = 0.2           # 0.02 


#weights
wB_init = 300.0             # [1/s]
wA1_init = 0 # [1/s]
wA2_init = 0 # [1/s]


#thresholds 
theta_A1_init =     0  # 38* scale_mV     # [mV]
theta_A2_init =    -1 * scale_mV     # [mV]

#nonlinearity
slope = 2200
threshold = 0

#occupancy
k_rel_init = 80.3#8.5 # 8.5 # 10.0           # [1/s]
k_rec_init = 1.0 #10.0              # [1/s]
beta_init =38.6#0.# 80.6# 80.6 #0 #15


slope_on = 1  # [Hz/mV] # 2200  # [Hz/V]
threshold_on = 0 # [mV]
max_val_on = 2  # [mV]

# ============================================================================================
# set up folder and parameter dictionary
# ============================================================================================

params_init = {'tau_B': tau_B_init,
                     'tau_A1':tau_A1_init,
                     'tau_A2':tau_A2_init,
                     'tau_G':tau_G_init,
                     'tau_VR':tau_VR,
                     'tau_VR2':tau_VR2,
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


                    'slope_on' : slope_on,  # [Hz/mV] # 2200  # [Hz/V]
                    'threshold_on' : threshold_on, # [mV]
                    'max_val_on' : max_val_on  # [mV]                 
                       }



params_model = make_param_dict(params_init)
params_model['SFA2'] =  1.1
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
filepath = "/user/sebert/home/Documents/Simulations/osr_model/bipolar_only"
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

Model = B_Model(linear_filter = linear_filter,   
                 filtertype = 'biphasic',
                 convolution = convolve_1D,
                 system  = system,
                 nonlinearity = nonlinearity,
                 occupancy = occupancy,
                 convolution_type = convolution_type,
                 stimfunction = stimfunction,

                 params = params_model,
                 
                 polarities = polarities,
                 filterlength = filterlength,
                 dt = dt)


kernel_fig = Model.plot_kernels()
kernel_fig = Model.plot_sigmoid_late()
save_fig(f'{filepath_paramset}/kernels.png',kernel_fig)


# ============================================================================================
# simulate and save impulse response
# ============================================================================================


simulation_name = 'impulse'

#TODO save hyperparameter for every simulation

print(f'{simulation_name} simulation')

stimulus,time  = impulse_stimulus(dt = dt, amplitude = 1/dt)
simulation = Model.predict(stimulus,time,simulation_name )
figure = Model.plot_response(simulation)


#TODO save in method
filename = f"simulation_{simulation['name']}_{occupancy}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
save_dict(f'{filepath_simulation}.pickle',simulation)
#save_fig(f'{filepath_simulation}.png',figure)


# # ============================================================================================
# # simulate and save chirp response
# # ============================================================================================

# simulation_name = 'chirp'

# #TODO save hyperparameter for every simulation

# print(f'{simulation_name} simulation')
# stimulus,time  = get_euler_stimulus(dt=dt)
# print(len(stimulus))
# print(len(time))
# simulation = Model.predict(stimulus,time,simulation_name)
# figure= Model.plot_response(simulation,xlims = (0,30))


# #TODO save in method
# filename = f"simulation_{simulation['name']}_{occupancy}"
# filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
# save_dict(f'{filepath_simulation}.pickle',simulation)
# save_fig(f'{filepath_simulation}.png',figure)



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
filename = f"simulation_{simulation_name}_{occupancy}_{fn}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt, xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle', show = True)
# TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()

print('12 Flashes done')


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
filename = f"simulation_{simulation_name}_{occupancy}_{fn}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt,xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle')
# TODO make figure 

# pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
# pdf.savefig(figure)
# pdf.close()

print('5 Flashes done')


# ============================================================================================
# simulate and respone to one short bright flash 
# ============================================================================================



simulation_name = 'short_flash_bright'

#TODO save hyperparameter for every simulation

print(f'{simulation_name} simulation')

stimulus,time  = step_stimulus(start = 1, stop = 1.04, dt = dt, amplitude = 1)
simulation = Model.predict(stimulus,time,simulation_name)
#figure = Model.plot_response(simulation)


#TODO save in method
filename = f"simulation_{simulation['name']}_{occupancy}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
save_dict(f'{filepath_simulation}.pickle',simulation)
#save_fig(f'{filepath_simulation}.png',figure)




# ============================================================================================
# simulate and respone to one short dark flash 
# ============================================================================================



simulation_name = 'short_flash_dark'

#TODO save hyperparameter for every simulation

print(f'{simulation_name} simulation')

stimulus,time  = step_stimulus(start = 1, stop = 1.04, dt = dt, amplitude = -1)
simulation = Model.predict(stimulus,time,simulation_name)
#figure = Model.plot_response(simulation)


#TODO save in method
filename = f"simulation_{simulation['name']}_{occupancy}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
save_dict(f'{filepath_simulation}.pickle',simulation)
#save_fig(f'{filepath_simulation}.png',figure)



# # ============================================================================================
# # simulate and save response to a long dark flash with different lumincance levels 
# # ============================================================================================

# from smallest lumninance step (corresponding to low frequency) to high step (correspinding to fast frequency)
lums_experiment = [118,108,98,85,77,64,43] #luminance levels used in experiment, 128 being  grey background and 0 being black


range_exp = [0,255]

lum_norm = []
for lum in lums_experiment:
    lum_norm.append(2*(lum/range_exp[1])-1)

simulations={}
fig,ax = plt.subplots(8,1, sharex = True)
for i,lum in enumerate(lum_norm): 
    simulation_name = f'long_flash_lum_{lum}'

    #TODO save hyperparameter for every simulation

    print(f'{simulation_name} simulation')

    stimulus,time  = step_stimulus(dt = dt, amplitude  = lum)
    simulation = Model.predict(stimulus,time,simulation_name)
    #figure = Model.plot_response(simulation,xlims = (0.9,3))

    st = ax[0].plot(time,stimulus, label = f'{lum}')
    #ax[i+1].plot(time,simulation['sol'].y[-2] * simulation['sol'].y[1], label = f'{lum}', color = st[0].get_color())
    ax[i+1].plot(time,simulation['RG'], label = f'{lum}', color = st[0].get_color())
    if i > 2:
        None
    if i >= 2:
        ax[i+1].set_ylabel(frequencies[i-2])
    ax[0].set_title('Stimulus')
    ax[1].set_title('$I_{OFF}$ Response')
    simulations[f'lum_{lum}'] = simulation
    simulations[f'lum_{lum}']['stimend'] = 2
    # filename = f"simulation_{simulation['name']}_{occupancy}"
    # filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
    # save_dict(f'{filepath_simulation}.pickle',simulation)


filename = f"simulation_contrast_{occupancy}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")

save_dict(f'{filepath_simulation}.pickle',simulations)
save_fig(f'{filepath_paramset}/step_contrast.png',fig)




# # ============================================================================================
# # simulate and save response to a long dark flash with differnet durations
# # ============================================================================================

# from long (corresponding to low frequency) to short (corresponding to fast frequency)
durs_experiment = np.asarray([2.03,1.43, 1.19, 0.95, 0.71])

simulations = {}
fig,ax = plt.subplots(6,1, sharex = True)
for i,dur in enumerate(durs_experiment): 
    simulation_name = f'long_flash_dur_{dur}'

    #TODO save hyperparameter for every simulation

    print(f'{simulation_name} simulation')

    stimulus,time  = step_stimulus(length = 5, start = 1, stop = 1+dur, dt = dt, amplitude  = -1)
    simulation = Model.predict(stimulus,time,simulation_name)
    #figure = Model.plot_response(simulation,xlims = (0.9,3))

    st = ax[0].plot(time-(1+dur),stimulus, label = f'{lum}')
    #ax[i+1].plot(time,simulation['sol'].y[-2] * simulation['sol'].y[1], label = f'{lum}', color = st[0].get_color())
    ax[i+1].plot(time-(1+dur),simulation['RG'], label = f'{lum}', color = st[0].get_color())
    ax[0].set_title('Stimulus')
    ax[1].set_title('$I_{OFF}$ Response')
    #TODO save in method
    # filename = f"simulation_{simulation['name']}_{occupancy}"
    #filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
    #save_dict(f'{filepath_simulation}.pickle',simulation)
    simulations[f'dur_{dur}'] = simulation
    simulations[f'dur_{dur}']['stimend'] = 1+dur

filename = f"simulation_duration_{occupancy}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")

save_dict(f'{filepath_simulation}.pickle',simulations)
save_fig(f'{filepath_paramset}/step_duration.png',fig)





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
filename = f"simulation_{simulation_name}_{occupancy}_{fn}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,periodic_flashes_variable_flashlength,
                dt = dt, xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle', show = False)
# TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()


# ============================================================================================
# simulate and save osr response 12 flashes with equal luminance stim from data
# ============================================================================================

fn = 12 
frequencies = np.array([6,8,10,12])
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

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()
