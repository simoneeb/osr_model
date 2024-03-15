
from stimuli import periodic_flashes
from stimuli import periodic_flashes_mixed_polarities
from stimuli import periodic_flashes_variable_flashlength
from stimuli import periodic_flashes_biphasic
from stimuli import periodic_flashes_fixed_luminance
from stimuli import periodic_flashes_fixed_luminance_rebound
import numpy as np
from scipy.optimize import curve_fit
from utils import save_dict, slope_fun




def simulate_OSR(Model,osrparams,hyperparams,params,
                stim_function = periodic_flashes,
                dt = 0.02,
                xlims = (1.9,5),
                filepath = None,
                show = False,
                fdtype = 'fixed',
                flashpolarity = -1.0,
                flashpolarities = [False],
                modified_weights = [False],
                print_steps = False):

    frequencies = osrparams['frequencies']
    periods = osrparams['periods']
    fn = osrparams['flashnumber']


    simulation_osr = {}
    simulation_osr['simulations'] =  {}
    simulation_osr['osrparams'] = osrparams
    #simulation_osr['frequencies'] = frequencies

    delays = np.zeros(len(frequencies))
    peak_amplitudes =  np.zeros(len(frequencies))
    maxs_n =  np.zeros(len(frequencies))


    initial_weight = params['w_A1']
    #print(f'inital weight: {initial_weight}')


    for i,freq in enumerate(frequencies):
       
        if any(flashpolarities):
            stimulus,time,lastflashend = stim_function(freq, fn,dt = dt, polarities = flashpolarities)
        else: 
            stimulus,time,lastflashend = stim_function(freq, fn,dt = dt, polarity = flashpolarity)

        if any(modified_weights):
            Model.modify_params('w_A1', modified_weights[i]*initial_weight)
            mw = Model.get_param_value('w_A1')
            print(f'modified for {freq} Hz : {mw}')
            simulation = Model.predict(stimulus,time,f'{freq} Hz', print_steps = print_steps)
        else:
            simulation = Model.predict(stimulus,time,f'{freq} Hz', print_steps = print_steps)

        if show == True:
            figure = Model.plot_response(simulation,xlims)

        time = simulation['time']
        try :
            delay = time[simulation['RG'][int((lastflashend+(1/freq))/dt):].argmax()+int((lastflashend+(1/freq))/dt)] - lastflashend
            peak_amp = simulation['RG'].max()
        except:
            delay = np.nan
            peak_amp = np.nan
        try:  
            if hyperparams['occupancy'] == 'dynamic':
                if hyperparams['polarities'][1] == 'ON':
                    max_n = simulation['sol'].y[3][100:].max()
                if hyperparams['polarities'][1] == 'OFF':
                    max_n = simulation['sol'].y[3][100:].min()
            else:
                max_n = params['n_A1_star']
        except:
            max_n = None

        simulation['lastflash_tp'] = lastflashend
        simulation['frequency'] = freq
        simulation['peak_amplitude'] = peak_amp
        simulation['delay'] = delay
        simulation['max_occupancy'] =max_n

        delays[i] = delay
        peak_amplitudes[i] = peak_amp
        maxs_n[i] = max_n

        simulation_osr['simulations'][f'{freq}_Hz'] = simulation



    try:
        popt,_ = curve_fit(slope_fun,periods,delays)
    except: 
        popt = [0.0,0.0]
    simulation_osr['slope'] = popt[0]
    simulation_osr['offset'] = popt[1]
    simulation_osr['delays'] = delays
    simulation_osr['peak_amplitudes'] = peak_amplitudes
    simulation_osr['maxs_n'] = maxs_n

    if filepath is not None: 
        save_dict(filepath, simulation_osr)

    return simulation_osr






   

