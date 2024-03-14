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

#name the simulation
folder_name = 'params_final_nonlin_test'
#folder_name = 'params_manual_N_fixed_OFF_dt0.002_strychnine_wA240_slope'

#True if load and existing dataset and not create a new one
load_params = False


#choose which functions to use 
linear_filter = filter_alpha_norm
system =  IPL_rectified_occupancy
nonlinearity = N
occupancy = 'dynamic'
convolution_type = 'VR'#'same'
polarities = ['ON', 'OFF', 'ON']
stimfunction ='sigmoid_late'
#hyperparameter
dt =  0.002 # [s]  # 0.002 #[s]
filterlength = 1 # [s]  # 1 #[s]



#model parameter 
scale_mV = 20 # [mV] # 0.05 # [V]


#time constants
tau_B_init =  0.08#0.25 #0.050 # [ms] # 0.05        # [s]
tau_A1_init =0.085# 0.115#0.64 #0.080 # [ms] # 0.08      # [s]
tau_A2_init = 0.12#0.12#0.64 #0.080 # [ms] # 0.08     # 0.27   # [s]
tau_G_init = 0.11 # [ms] # 0.1 #0.04     # [s]
tau_VR = 0.0030 # [ms] 0.02 


#weights
wB_init =  50.#70.# 50.    # [kHz] #  50.0 #51.0             # [1/s]
wA1_init = -53.#43.   # -68.#-20.# -72 # [kHz] # 95.0 #0 #-115.0 #-95.0 #-60 # -60.0    #20.8   # [1/s]
wA2_init =-65.#85.#-36.#-42. # [kHz] # -82.0 #-53.0 #-42.0 #-82.0 #-84.0 # -50.0 # 52.0# -100.0 # -80.0     #10.0  # [1/s]

gB_init = 0  # [kHz] #  50.0 #51.0             # [1/s]
gA1_init = 0 #-52 # [kHz] # 95.0 #0 #-115.0 #-95.0 #-60 # -60.0    #20.8   # [1/s]
gA2_init = 0 # [kHz] # -82.0 #-53.0 #-42.0 #-82.0 #-84.0 # -50.0 # 52.0# -100.0 # -80.0     #10.0  # [1/s]

#thresholds 
theta_A1_init =    0 #-1 * scale_mV     # [mV]
theta_A2_init =    -.25 * scale_mV     # [mV]

#nonlinearity
slope = 12#20     # [Hz/mV] # 2200  # [Hz/V]
threshold = 0.0  # [mV]

slope_on = 14  # [Hz/mV] # 2200  # [Hz/V]
threshold_on = -.5 # [mV]
max_val_on = 1  # [mV]

slope_off = 12  # [Hz/mV] # 2200  # [Hz/V]
threshold_off = .5 # [mV]
max_val_off = 1  # [mV]

#occupancy
k_rel_init = 5.0 # 10.0           # [1/s]
k_rec_init = 10.0 #10.0              # [1/s]
beta_init =  0.0826 #0.0380 #0 #15


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

                     'g_B':gB_init,
                     'g_A1':gA1_init,
                     'g_A2':gA2_init,

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


print(model_functions)


hyperparameter = {'dt' : dt,
                    'filterlength' : filterlength,
                    'occupancy' : occupancy,
                    "polarities" : polarities }



# params = { "params_model": params_model,
#             "model_functions" : model_functions,
#             "hyperparameter" : hyperparameter}

params = { "params_model": params_model,
            "model_functions" : None,
            "hyperparameter" : hyperparameter}



# create folder automatically and load parameterset
filepath_parameset_load = "/user/sebert/home/Documents/Simulations/osr_model"
filepath_paramset = make_directory(filepath_parameset_load,'params_final')



if load_params is True:
    with open(f'{filepath_paramset}/params.json') as json_file:
        params = json.load(json_file)
        print(params)

        params_model = params['params_model']

filepath =  "/user/sebert/home/Documents/Simulations/osr_model/"
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
save_fig(f'{filepath_paramset}/kernels.png',kernel_fig)



# ============================================================================================
# simulate and save impulse response
# ============================================================================================


simulation_name = 'impulse'

#TODO save hyperparameter for every simulation

print(f'{simulation_name} simulation')

stimulus,time  = impulse_stimulus(length = 2000, impulse_timepoint = 1000, dt = dt, amplitude = 1/dt)
simulation = Model.predict(stimulus,time,simulation_name)
#figure = Model.plot_response(simulation)


#TODO save in method
filename = f"simulation_{simulation['name']}_{occupancy}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
save_dict(f'{filepath_simulation}.pickle',simulation)
#save_fig(f'{filepath_simulation}.png',figure)




# # ============================================================================================
# # simulate and save chirp response
# # ============================================================================================

simulation_name = 'chirp'

#TODO save hyperparameter for every simulation

print(f'{simulation_name} simulation')
stimulus,time  = get_euler_stimulus(dt=dt)
print(len(stimulus))
print(len(time))
simulation = Model.predict(stimulus,time,simulation_name)
figure= Model.plot_response(simulation,xlims = (0,30))


#TODO save in method
filename = f"simulation_{simulation['name']}_{occupancy}"
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
filename = f"simulation_{simulation_name}_{occupancy}_{fn}"
filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt, xlims = (1.9,5),filepath = f'{filepath_simulation}.pickle', show = False)
# TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()
print('12 Flashes done')




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



# # ============================================================================================
# # simulate and save osr response 25 flashes
# # ============================================================================================

# fn = 25 
# frequencies = np.array([6,8,10,12,16])
# periods = 1/frequencies

# osrparams = {'flashnumber' : fn,
#             'frequencies' : frequencies,
#             'periods' : periods}


# simulation_name = 'osr'
# print(f'{simulation_name} simulation')
# filename = f"simulation_{simulation_name}_{occupancy}_{fn}"
# filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


# osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt,xlims = (1.9,7),filepath = f'{filepath_simulation}.pickle')
# # TODO make figure 

# #pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
# #pdf.savefig(figure)
# #pdf.close()




# ============================================================================================
# simulate and save osr response different flashnumbers
# ============================================================================================

# flashnumbers = np.array([2,3,4,6,7,8,9,10,11,13,14,15,16,17,18,19,20])
# frequencies = np.array([6,8,10,12,16])
# periods = 1/frequencies

# for fn in flashnumbers:

#     osrparams = {'flashnumber' : fn,
#                 'frequencies' : frequencies,
#                 'periods' : periods}


#     simulation_name = 'osr'
#     print(f'{simulation_name} simulation')
#     filename = f"simulation_{simulation_name}_{occupancy}_{fn}"
#     filepath_simulation = os.path.join(filepath_paramset,f"{filename}")


#     osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt,xlims = (1.9,7),filepath = f'{filepath_simulation}.pickle')
# TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()


# ============================================================================================
# simulate and save osr response different flashnumbers with the last flash being bright
# ============================================================================================

# flashnumbers = np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25])
# frequencies = np.array([6,8,10,12,16])
# periods = 1/frequencies


# for fn in flashnumbers:

#     osrparams = {'flashnumber' : fn,
#                 'frequencies' : frequencies,
#                 'periods' : periods}

#     flashpolarities = np.ones(fn)*-1
#     flashpolarities[-1] = 1

#     simulation_name = 'osr_mixed_polrities'
#     print(f'{simulation_name} simulation')
#     filename = f"simulation_{simulation_name}_{occupancy}_{fn}"
#     filepath_simulation = os.path.join(filepath_paramset,f"{filename}")

#     osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt,flashpolarities = flashpolarities, xlims = (1.9,7),filepath = f'{filepath_simulation}.pickle')
# TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()

# ============================================================================================
# simulate and save osr response different flashnumbers with middle flash being bright
# ============================================================================================

# flashnumbers = np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25])
# frequencies = np.array([6,8,10,12,16])
# periods = 1/frequencies


# for fn in flashnumbers:

#     osrparams = {'flashnumber' : fn,
#                 'frequencies' : frequencies,
#                 'periods' : periods}

#     flashpolarities = np.ones(fn)*-1
#     flashpolarities[int(fn/2)] = 1

#     simulation_name = 'osr_middle_bright'
#     print(f'{simulation_name} simulation')
#     filename = f"simulation_{simulation_name}_{occupancy}_{fn}"
#     filepath_simulation = os.path.join(filepath_paramset,f"{filename}")

#     osr_simulation = simulate_OSR(Model,osrparams,hyperparameter,params_model,dt = dt,flashpolarities = flashpolarities, xlims = (1.9,7),filepath = f'{filepath_simulation}.pickle')
# # TODO make figure 

#pdf = backend_pdf.PdfPages(f"{filepath_simulation}.pdf")
#pdf.savefig(figure)
#pdf.close()



# ============================================================================================
# simulate and save response to one short flash 
# ============================================================================================


# simulation_name = 'short_flash'

# #TODO save hyperparameter for every simulation

# print(f'{simulation_name} simulation')

# stimulus,time  = step_stimulus(start = 1, stop = 1.04, dt = dt, amplitude = -1)
# simulation = Model.predict(stimulus,time,simulation_name)
# figure = Model.plot_response(simulation)


# #TODO save in method
# filename = f"simulation_{simulation['name']}_{occupancy}"
# filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
# save_dict(f'{filepath_simulation}.pickle',simulation)
# save_fig(f'{filepath_simulation}.png',figure)
# 
# 
# ============================================================================================
# simulate and save response to one short flash bright
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


# # TODO make simulation to one long flash
# # ============================================================================================
# # simulate and save response to a long flash
# # ============================================================================================

# simulation_name = 'long_flash'

# #TODO save hyperparameter for every simulation

# print(f'{simulation_name} simulation')

# stimulus,time  = step_stimulus(dt = dt, amplitude  = -1)
# simulation = Model.predict(stimulus,time,simulation_name)
# figure = Model.plot_response(simulation,xlims = (0.9,3))


# #TODO save in method
# filename = f"simulation_{simulation['name']}_{occupancy}"
# filepath_simulation = os.path.join(filepath_paramset,f"{filename}")
# save_dict(f'{filepath_simulation}.pickle',simulation)
# save_fig(f'{filepath_simulation}.png',figure)



# # ============================================================================================
# # simulate and save response to a long dark flash with different lumincance levels 
# # ============================================================================================

# from smallest lumninance step (corresponding to low frequency) to high step (correspinding to fast frequency)
lums_experiment = [118,108,98,85,77,64,43] #luminance levels used in experiment, 128 being  grey background and 0 being black
lums_experiment = [98,85,77,64,43] #luminance levels used in experiment, 128 being  grey background and 0 being black


range_exp = [0,255]

lum_norm = []
for lum in lums_experiment:
    #lum_norm.append(-1*(1-(lum/255)))
    lum_norm.append(2*(lum/range_exp[1])-1)

simulations={}

#lum_norm = [-.4,-.5,-.6,-.7,-.8,-.9,-1]
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


filename = f"simulation_contrast_{occupancy}_strong_dimming"
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
