import numpy as np
import pandas as pd 
from scipy.interpolate import interp1d



# periodic flashes
def periodic_flashes (frequency, flashnumber, dt = 0.002, delay = 2, flashduration = 0.04, polarity = -1, baseline = 0.0) :
    
    frequency = frequency#*0.001
    period = (1/frequency) /dt
    flashduration = flashduration  /dt
    delay = delay /dt

    period = np.round(period)
    flashduration = np.round(flashduration)
    delay = np.round(delay)


    length =int( period * flashnumber + 2 * delay)
    timeline = np.arange(0,length)*dt
    
    stimulus = np.zeros(length)
    tp_startflashes = int(delay)
    tp_endflashes = tp_startflashes + int(flashnumber * period)  - int(1)

    stimulus[0:tp_startflashes] = baseline

    i=-1
    for tp in range (tp_startflashes, tp_endflashes) :
        i=i+1
        if i% (period) < (flashduration):
            stimulus[tp] = polarity
        else:
            stimulus[tp] = baseline

    stimulus[tp_endflashes:] = baseline
    
    lastflashend = timeline[np.where(np.diff(stimulus) == -1*(polarity-baseline))[0][-1]+int(1)]


    return np.asarray(stimulus),timeline,lastflashend



# periodic flashes
def periodic_flashes_biphasic (frequency, flashnumber, dt = 0.002, delay = 2, flashduration = 0.04, polarity = -1, baseline = 0) :
    
    period = (1/frequency) /dt
    flashduration = flashduration  /dt
    delay = delay /dt

    period = np.round(period)
    flashduration = np.round(flashduration)
    delay = np.round(delay)


    length =int( period * flashnumber + 2 * delay)
    timeline = np.arange(0,length)*dt
    
    stimulus = np.zeros(length)
    tp_startflashes = int(delay)
    tp_endflashes = tp_startflashes + int(flashnumber * period)  - int(1)

    stimulus[0:tp_startflashes] = baseline

    i=-1
    for tp in range (tp_startflashes, tp_endflashes) :
        i=i+1
        if i% (period) < (flashduration):
            stimulus[tp] = polarity
        elif i% (period) >= (flashduration) and  i% (period) < (2*flashduration):
            stimulus[tp] = polarity*-1
        else:
            stimulus[tp] = baseline

    stimulus[tp_endflashes:] = baseline
    
    lastflashend = timeline[np.where(np.diff(stimulus) == -2*polarity)[0][-1]+int(1)]


    return np.asarray(stimulus),timeline,lastflashend



def periodic_flashes_fixed_luminance (frequency, flashnumber, luminance_ratio = 1.,dt = 0.002, delay = 2, flashduration = 0.04, polarity = -1, baseline = 0) :
    
    period = (1/frequency) /dt
    flashduration = flashduration  /dt
    delay = delay /dt

    period = np.round(period)
    flashduration = np.round(flashduration)
    delay = np.round(delay)

    interflash_duration = period -flashduration

    ratio = (flashnumber*flashduration)/(luminance_ratio*(flashnumber-1)*interflash_duration)

    interflash_val = polarity*-1*ratio
    
    length =int( period * flashnumber + 2 * delay)
    timeline = np.arange(0,length)*dt
    
    stimulus = np.zeros(length)
    tp_startflashes = int(delay)
    tp_endflashes = tp_startflashes + int(flashnumber * period)  - int(interflash_duration)

    stimulus[0:tp_startflashes] = baseline

    i=-1
    for tp in range (tp_startflashes, tp_endflashes) :
        i=i+1
        if i% (period) < (flashduration):
            stimulus[tp] = polarity
        else:
            stimulus[tp] = interflash_val

    stimulus[tp_endflashes:] = baseline
    
    lastflashend = timeline[np.where(np.diff(stimulus) == (-1*polarity))[0][-1]+int(1)]

    print(f'luminaince = {np.sum(stimulus)}')

    return np.asarray(stimulus),timeline,lastflashend



def periodic_flashes_fixed_luminance_rebound (frequency, flashnumber, dt = 0.002, delay = 2, flashduration = 0.04, polarity = -1, baseline = 0) :
    
    period = (1/frequency) /dt
    flashduration = flashduration  /dt
    delay = delay /dt

    period = np.round(period)
    flashduration = np.round(flashduration)
    delay = np.round(delay)

    interflash_duration = period -flashduration

    ratio = flashduration/interflash_duration

    interflash_val = polarity*-1*ratio
    
    length =int( period * flashnumber + 2 * delay)
    timeline = np.arange(0,length)*dt
    
    stimulus = np.zeros(length)
    tp_startflashes = int(delay)
    tp_endflashes = tp_startflashes + int(flashnumber * period)  - int(1)

    stimulus[0:tp_startflashes] = baseline

    i=-1
    for tp in range (tp_startflashes, tp_endflashes) :
        i=i+1
        if i% (period) < (flashduration):
            stimulus[tp] = polarity
        else:
            stimulus[tp] = interflash_val

    stimulus[tp_endflashes:] = baseline
    
    lastflashend = timeline[np.where(np.diff(stimulus) == (-1*polarity+interflash_val))[0][-1]+int(1)]

    return np.asarray(stimulus),timeline,lastflashend



x =1

# periodic flashes
def periodic_flashes_mixed_polarities(frequency, flashnumber, dt = 0.002, delay = 2, flashduration = 0.04, polarities = -1*np.ones(12), baseline = 0) :
    
    period = (1/frequency) /dt
    flashduration = flashduration  /dt
    delay = delay /dt

    period = np.round(period)
    flashduration = np.round(flashduration)
    delay = np.round(delay)


    length =int( period * flashnumber + 2 * delay)
    timeline = np.arange(0,length)*dt
    
    stimulus = np.ones(length) * baseline
    tp_startflashes = int(delay)
    tp_endflashes = tp_startflashes + int(flashnumber * period)  - int(1)


    i=-1
    x = -1
    flash = 0
    for tp in range (tp_startflashes, tp_endflashes) :
        i=i+1
        if i% (period) < (flashduration):
            x = x +1
            

            if x != i:
                flash = flash+1
                x = i
            
            stimulus[tp] = polarities[flash]

            
        
        else:
            stimulus[tp] = baseline
        

    
    lastflashend = timeline[np.where(np.diff(stimulus) == polarities[-1])[0][-2]+int(1)] 


    return np.asarray(stimulus),timeline,lastflashend




# periodic flashes
def periodic_flashes_variable_flashlength (frequency, flashnumber, dt = 0.002, delay = 2, flashduration = 0.04, polarity = -1, baseline = 0) :
    
    period = (1/frequency) /dt
    flashduration = flashduration  /dt
    delay = delay /dt

    period = np.round(period)
    flashduration = np.round(flashduration)
    delay = np.round(delay)


    length =int( period * flashnumber + 2 * delay)
    timeline = np.arange(0,length)*dt
    
    stimulus = np.zeros(length)
    tp_startflashes = int(delay)
    tp_endflashes = tp_startflashes + int(flashnumber * period)  - int(1)

    stimulus[0:tp_startflashes] = baseline

    i=-1
    for tp in range (tp_startflashes, tp_endflashes) :
        i=i+1
        if i% (period) < (period/2):
            stimulus[tp] = polarity
        else:
            stimulus[tp] = baseline

    stimulus[tp_endflashes:] = baseline
    
    lastflashend = timeline[np.where(np.diff(stimulus) == -1*polarity)[0][-1]+int(1)]


    return np.asarray(stimulus),timeline,lastflashend


#make impulse stimulus
def impulse_stimulus(length = 2,impulse_timepoint = 1,dt = 0.002, amplitude = 1):

    stimframes = int(length/dt)
    impulse_idx = int(impulse_timepoint/dt)
    stimulus= np.zeros(stimframes)
    stimulus[impulse_idx] = amplitude

    timeline = np.arange(0,length,dt)

    return np.asarray(stimulus),timeline



#simple step stimulus
def step_stimulus(length = 3, start = 1, stop = 2, dt = 0.02, amplitude = 1, baseline = 0):

    stimulus = (np.heaviside(np.arange(-start,length - start, dt), 1) - 1 * np.heaviside(
        np.arange(-stop, length - stop, step = dt),1)) * (amplitude-baseline)
    stimulus = stimulus + baseline
    timeline = np.arange(0,length,dt)


    return np.asarray(stimulus),timeline



def step_stimulus_luminance(frequency,fn,polarity = -1, flashduration = 0.04, length = 3, start = 1, stop = 2, dt = 0.002, amplitude = 1):

    

    amplitude = (frequency*flashduration*polarity)/(stop-start)


    stimulus = (np.heaviside(np.arange(-start,length - start, dt), 1) - 1 * np.heaviside(
        np.arange(-stop, length - stop, step = dt),1)) * amplitude
    timeline = np.arange(0,length,dt)


    return np.asarray(stimulus),timeline,stop


x = 1


#get euler stimulus
def get_euler_stimulus(dt = 0.02, amplitude = 1):

    stimeuler = pd.read_csv('/user/sebert/home/Documents/Experiments/StimulusDesgin/Euler_Baptiste/euler_luminance_profile.csv')
    euler = np.asarray(stimeuler['luminance'])
    euler = (euler/euler.max()) * amplitude
    #euler = euler - euler.std()

    euler_time = np.arange(0,30,0.02)

    if dt != 0.02:
        euler_fun = interp1d(euler_time,euler,fill_value="extrapolate")
        euler_time = np.arange(0,30,dt)
        stim_dt = euler_fun(euler_time)
    
    return euler,euler_time


# load stimulus from experiments

x = 0


def get_stimulus_from_data(stimfile,dt = 0.002):

    sti = pd.read_csv(stimfile, header = None)
    stimdict = {}
    
    for key in sti.keys():
         stim = sti[key].dropna()
         stim = (stim-128)/128
         stimdict[key] = stim


    euler = (euler/euler.max()) * amplitude
    #euler = euler - euler.std()

    euler_time = np.arange(0,30,0.02)

    if dt != 0.02:
        euler_fun = interp1d(euler_time,euler,fill_value="extrapolate")
        euler_time = np.arange(0,30,dt)
        stim_dt = euler_fun(euler_time)
    
    return euler,euler_time
