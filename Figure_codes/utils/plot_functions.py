
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import pandas as pd
#import h5py
from scipy.ndimage import gaussian_filter
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy import stats

import pickle
import itertools
#import seaborn as sns


# periodic flashes
def periodic_flashes(frequency, flashnumber, dt = 0.02, delay = 2, flashduration = 0.04, polarity = -1, baseline = 0) :
    
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
    
    lastflashend = timeline[np.where(np.diff(stimulus) == -1*polarity)[0][-1]+int(1)]


    return np.asarray(stimulus),timeline,lastflashend




# periodic flashes
def periodic_flashes_mixed_polarities(frequency, flashnumber, dt = 0.02, delay = 2, flashduration = 0.04, polarities = -1*np.ones(12), baseline = 0) :
    
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
def periodic_flashes_variable_flashlength (frequency, flashnumber, dt = 0.02, delay = 2, flashduration = 0.04, polarity = -1, baseline = 0) :
    
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






# plotting functions       
def slope(x,s,i):
    return s * x + i

    
def plot_one_cell(cell,cells_dict, 
    color = 'r',
    fontsize = 20,
    fontsize_legend = 10,
    fontsize_ticks = 10,
    lw = 3,
    frequencies = ['6_Hz','8_Hz','10_Hz','12_Hz','16_Hz'],
    periods = np.array([170,120,100,80,60])):    
    

    fig = plt.figure(figsize = (10,5))
    gs = fig.add_gridspec(5,3)
    

#     fig.subplots_adjust(
#     top=0.875,
#     bottom=0.085,
#     left=0.43,
#     right=0.885,
#     hspace=0.4,
#     wspace=0.3
#     )

    
    delays_control = []
    delays_strych = []
    
    for i,frq in enumerate(frequencies):
        
            time = cells_dict[cell]['response_data']['osr_times'][i]
            lastflashend = cells_dict[cell]['response_data']['lastflashends'][i]
            
            resp_control = cells_dict[cell]['response_data']['responses_control'][i]
            resp_strych = cells_dict[cell]['response_data']['responses_strychnine'][i]
            
            
            #peak automatically detected
            peak_control = cells_dict[cell]['response_data']['peaks_control'][i]
            peak_strych = cells_dict[cell]['response_data']['peaks_strychnine'][i]
            
            #delays from automatically detected peak
            delays_control.append(peak_control - lastflashend)
            delays_strych.append(peak_strych - lastflashend)
          
            peak_control_man = cells_dict[cell]['slope_data']['peaks_control'][i]
            peak_strych_man = cells_dict[cell]['slope_data']['peaks_strych'][i]
            

            
            
            #TODO plot flashes
#             for f in range(0,len(flashstarts[0])):
#             if row == 0 and f == 0:
#                 traces.axvspan(flashstarts[i][f]-lastflashends[i],flashends[i][f]-lastflashends[i], color = 'black', alpha = .2,label = 'flash')
#             else:    
#                 traces.axvspan(flashstarts[i][f]-lastflashends[i],flashends[i][f]-lastflashends[i], color = 'black', alpha = .2)
#             traces.axvline(flashstarts[i][f]+np.mean(np.diff(flashstarts[i]) -flashends[i][-1]),linestyle = ':',color = 'k', alpha = .5)
#             traces.axvline(flashends[i][f]+np.mean(np.diff(flashends[i])-flashends[i][-1]),linestyle = ':',color = 'k', alpha = .5)


            traces = fig.add_subplot(gs[i, 0]) #, sharex = traces, sharey = traces)
           
            traces.plot(time-lastflashend,resp_control, color = 'k', alpha =.7, linewidth = lw)
            traces.plot(time-lastflashend,resp_strych, color = color, alpha =.7, linewidth = lw)
            
            
            
            traces.axvline(peak_control-lastflashend,linestyle = ':', color = 'k', alpha =.1, linewidth = lw)
            traces.axvline(peak_strych-lastflashend,linestyle = ':', color = color, alpha =.1, linewidth = lw)
            
            traces.axvline(peak_control_man,linestyle = ':', color = 'k', alpha =.7, linewidth = lw)
            traces.axvline(peak_strych_man,linestyle = ':', color = color, alpha =.7, linewidth = lw)
           
           
            traces.set_xlabel('time [s]', fontsize = fontsize, fontweight = 'bold')
            traces.set_ylabel(frq,  fontsize = fontsize, fontweight = 'bold')

            
            
            traces.locator_params(axis = 'x', nbins=5)
            #traces.set_ylim(0, 8)
            traces.set_xlim(-.5, 1)
            traces.spines['top'].set_visible(False)
            traces.spines['right'].set_visible(False)
            traces.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
            traces.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

            
            
    #slope of automatically detected peak
    delays_control = np.array(delays_control)*1000
    delays_strych = np.array(delays_strych)*1000

    try:  
        [sl_control,i_control],_ = curve_fit(slope,periods[~np.isnan(delays_control)],delays_control[~np.isnan(delays_control)])
        [sl_strych,i_strych],_ = curve_fit(slope,periods[~np.isnan(delays_strych)],delays_strych[~np.isnan(delays_strych)])

    except:
        [sl_control,i_control] = [0,0]
        [sl_strych,i_strych] = [0,0]

                
    #slope of manually detected peak
    slope_control_man = cells_dict[cell]['slope_data']['slope_control']
    slope_strych_man = cells_dict[cell]['slope_data']['slope_strych'] 
            
    offset_control_man = cells_dict[cell]['slope_data']['offset_control'] * 1000
    offset_strych_man = cells_dict[cell]['slope_data']['offset_strych'] * 1000
    
         
    # TODO check if slope is the same  
    
    delay = fig.add_subplot(gs[:,1])
    
    #autmatic peak    
    delay.plot(periods,delays_control,'k-o', linewidth = lw, alpha = 0.1)
    delay.plot(periods,slope(periods,sl_control,i_control), ":", alpha = .1, color = 'black',linewidth =lw, label = f'slope = {sl_control:.2f}')
      
    delay.plot(periods,delays_strych,'r-o', linewidth = lw, alpha = 0.1)
    delay.plot(periods,slope(periods,sl_strych,i_strych), ":", alpha = .1, color = color, linewidth =lw, label = f'slope = {sl_strych:.2f}')
    
    #manual peak
    delay.plot(periods,cells_dict[cell]['slope_data']['peaks_control']*1000,'k-o', linewidth = lw)
    delay.plot(periods,slope(periods,slope_control_man,offset_control_man), ":", alpha = .5, color = 'black',linewidth =lw, label = f'slope = {slope_control_man:.2f}')
      
    delay.plot(periods,cells_dict[cell]['slope_data']['peaks_strych']*1000,'r-o', linewidth = lw)
    delay.plot(periods,slope(periods,slope_strych_man,offset_strych_man), ":", alpha = .5, color = color, linewidth =lw, label = f'slope = {slope_strych_man:.2f}')
    
    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    delay.set_xticks(periods)

    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)
    
    delay.legend()


    try:
    
        # temporal STA
        temporal = fig.add_subplot(gs[0:2,2])

        temporal.plot(cells_dict[cell]['STA']['temporal'])
        temporal.set_xlabel('time [s]')

        
        # spatial STA
        spatial = fig.add_subplot(gs[3:,2])
        spatial.imshow(cells_dict[cell]['STA']['spatial'])
        spatial.plot(cells_dict[cell]['STA']['ellipse'][1,:],cells_dict[cell]['STA']['ellipse'][0,:],color = 'r')

    except: 
        None
    
    
    # TODO get ellipses

    fig.suptitle(f'{cell}')
    
    return fig

def plot_one_cell_rasters_control(cell,cells_dict, 
    color = 'r',
    fontsize = 20,
    fontsize_legend = 10,
    fontsize_ticks = 10,
    lw = 3,
    frequencies = ['6_Hz','8_Hz','10_Hz','12_Hz','16_Hz'],
    periods = np.array([170,120,100,80,60])):    
    

    fig = plt.figure(figsize = (10,5))
    gs = fig.add_gridspec(5,3)
    

#     fig.subplots_adjust(
#     top=0.875,
#     bottom=0.085,
#     left=0.43,
#     right=0.885,
#     hspace=0.4,
#     wspace=0.3
#     )

    
    delays_control = []
    
    for i,frq in enumerate(frequencies):
        
            time = cells_dict[cell]['response_data']['osr_times'][i]
            lastflashend = cells_dict[cell]['response_data']['lastflashends'][i]
            flashstarts = cells_dict[cell]['response_data']['flashstarts'][i]
            flashends = cells_dict[cell]['response_data']['flashends'][i]
            
            rasters_control = np.asarray(cells_dict[cell]['response_data']['rasters_control'][i])-lastflashend
            #rasters_control = rasters_control[:30]
            

           
            
            #delays from automatically detected peak
          
            peak_control = cells_dict[cell]['slope_data']['peaks_control'][i]            
            delays_control.append(peak_control - lastflashend)



            traces = fig.add_subplot(gs[i, 0]) #, sharex = traces, sharey = traces)

            
            
            #TODO plot flashes
            for f in range(0,len(flashstarts)):
             
                traces.axvspan(flashstarts[f]-lastflashend,flashends[f]-lastflashend, color = 'black', alpha = .2)
            traces.axvline(flashstarts[f]+np.mean(np.diff(flashstarts) -lastflashend),linestyle = ':',color = 'k', alpha = .5)
            traces.axvline(flashends[f]+np.mean(np.diff(flashends)-lastflashend),linestyle = ':',color = 'k', alpha = .5)


           
            traces.eventplot(rasters_control, color = 'k', alpha =.7, linewidth = lw)
            #traces.eventplot(time-lastflashend,rasters_control, color = 'k', alpha =.7, linewidth = lw)
            
            
            traces.axvline(peak_control,linestyle = ':', color = 'm', alpha =1, linewidth = lw)
            
           
            traces.set_xlabel('time [s]', fontsize = fontsize, fontweight = 'bold')
            traces.set_ylabel(frq,  fontsize = fontsize, fontweight = 'bold')

            
            
            traces.locator_params(axis = 'x', nbins=5)
            #traces.set_ylim(0, 8)
            traces.set_xlim(-.5, 1)
            traces.spines['top'].set_visible(False)
            traces.spines['right'].set_visible(False)
            traces.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
            traces.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    
    return fig

def plot_one_cell_control(cell,cells_dict, 
    sigma = None,
    smooth_peak = True,
    color = 'r',
    fontsize = 20,
    fontsize_legend = 10,
    fontsize_ticks = 10,
    lw = 3,
    frequencies = ['6_Hz','8_Hz','10_Hz','12_Hz','16_Hz'],
    periods = np.array([170,120,100,80,60])):    
    

    fig = plt.figure(figsize = (10,5))
    gs = fig.add_gridspec(2,2)

    lfe = fig.add_subplot(gs[0, 0]) #, sharex = traces, sharey = traces)
    ofe = fig.add_subplot(gs[1, 0]) #, sharex = traces, sharey = traces)


#     fig.subplots_adjust(
#     top=0.875,
#     bottom=0.085,
#     left=0.43,
#     right=0.885,
#     hspace=0.4,
#     wspace=0.3
#     )

    
    delays_control = []
    
    for i,frq in enumerate(frequencies):

        
        time = cells_dict[cell]['response_data']['osr_times'][i]
        lastflashend = cells_dict[cell]['response_data']['lastflashends'][i]
        flashends = cells_dict[cell]['response_data']['flashends'][i]
        omittedflashend = lastflashend + np.mean(np.diff(flashends))

        resp = cells_dict[cell]['response_data']['responses_control'][i]

        if sigma is not None:
            resp = gaussian_filter(resp,sigma)
            delays_control.append(time[np.argmax(resp)]-lastflashend)


        lfe.plot(time-lastflashend,resp, label = f'{frq}')    
        ofe.plot(time-omittedflashend,resp)
    
    
        
        ofe.set_xlabel('time relative to last flash [s]', fontsize = fontsize, fontweight = 'bold')
        lfe.set_xlabel('time relative to omitted flash [s]', fontsize = fontsize, fontweight = 'bold')

    
        ofe.locator_params(axis = 'x', nbins=5)
        #ofe.set_ylim(0, 8)
        ofe.set_xlim(-.5, 1)
        ofe.spines['top'].set_visible(False)
        ofe.spines['right'].set_visible(False)
        ofe.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
        ofe.tick_params(axis='both', which='major', labelsize=fontsize_ticks) 
        lfe.locator_params(axis = 'x', nbins=5)
        #lfe.set_ylim(0, 8)
        lfe.set_xlim(-.5, 1)
        lfe.spines['top'].set_visible(False)
        lfe.spines['right'].set_visible(False)
        lfe.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
        lfe.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    fig.legend()


    delays_lf = cells_dict[cell]['slope_data']['peaks_control']*1000
    delays_of = cells_dict[cell]['slope_data']['peaks_control']*1000-periods

    

    if smooth_peak is True:
        delays_lf = np.asarray(delays_control)*1000
        delays_of = np.asarray(delays_control)*1000 - periods

    popt_of,_ = curve_fit(slope,periods[~np.isnan(delays_of)],delays_of[~np.isnan(delays_of)])
    popt_lf,_ = curve_fit(slope,periods[~np.isnan(delays_lf)],delays_lf[~np.isnan(delays_lf)])




    delay = fig.add_subplot(gs[:,1])

    
    #manual peak
    #delay.plot(periods, slope(periods,all_slopes_control[i],all_offsets_control[i]), color = 'k', linestyle = ':', alpha = 0.1)

    delay.plot(periods,delays_lf,'k-o', linewidth = lw, alpha = 1)
    delay.scatter(periods,delays_lf)

    delay.plot(periods,delays_of,'k-o', linewidth = lw, alpha = 0.1)
    delay.scatter(periods,delays_of)

    if sigma is not None : 

        delay.plot(periods, slope(periods,*popt_lf),
                                color = 'k', linestyle = '--',
                                label = popt_lf[0]) 
        delay.plot(periods, slope(periods,1,popt_lf[1]), color = 'k', linestyle = ':', alpha = 1, label = '1')

    else:
        delay.plot(periods, slope(periods,cells_dict[cell]['slope_data']['slope_control'],cells_dict[cell]['slope_data']['offset_control']*1000),
                             color = 'k', linestyle = '--',
                             label = cells_dict[cell]['slope_data']['slope_control'])
        delay.plot(periods, slope(periods,1,cells_dict[cell]['slope_data']['offset_control']*1000), color = 'k', linestyle = ':', alpha = 1, label = '1')
        
    delay.plot(periods, slope(periods,*popt_of), color = 'k',
                              linestyle = '--', alpha = .1,
                              label = popt_of[0])
    
    delay.plot(periods, slope(periods,0,popt_of[1]), color = 'k', linestyle = ':', alpha = .1, label = '0')



    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('relative delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    delay.set_xticks(periods)

    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    delay.legend()

    return fig


def plot_mean_control(all_responses,mean_delays,std_delays,cells_dict, 
    sigma = None,
    smooth_peak = True,
    color = 'r',
    fontsize = 20,
    fontsize_legend = 10,
    fontsize_ticks = 10,
    lw = 3,
    frequencies = ['6_Hz','8_Hz','10_Hz','12_Hz','16_Hz'],
    periods = np.array([170,120,100,80,60])):    
    

    fig = plt.figure(figsize = (10,5))
    gs = fig.add_gridspec(2,2)

    lfe = fig.add_subplot(gs[0, 0]) #, sharex = traces, sharey = traces)
    ofe = fig.add_subplot(gs[1, 0]) #, sharex = traces, sharey = traces)


#     fig.subplots_adjust(
#     top=0.875,
#     bottom=0.085,
#     left=0.43,
#     right=0.885,
#     hspace=0.4,
#     wspace=0.3
#     )

    
    delays_control = []
    
    for i,frq in enumerate(frequencies):

        
        time = cells_dict['cell_0']['response_data']['osr_times'][i]
        lastflashend = cells_dict['cell_0']['response_data']['lastflashends'][i]
        flashends = cells_dict["cell_0"]['response_data']['flashends'][i]
        omittedflashend = lastflashend + np.mean(np.diff(flashends))

        #resp = cells_dict["cell_0"]['response_data']['responses_control'][i]
        resp = all_responses[frq]['means']['control']
        std = all_responses[frq]['stds']['control']
        #delays_control.append((time[np.argmax(resp)]-lastflashend)*1000)




        if sigma is not None:
            resp = gaussian_filter(resp,sigma)
            delays_control.append((time[np.argmax(resp)]-lastflashend)*1000)


        lfe.plot(time-lastflashend,resp, label = f'{frq}')    
        lfe.fill_between(time-lastflashend,resp-std,resp+std, alpha=.1)

        ofe.plot(time-omittedflashend,resp)
        ofe.fill_between(time-omittedflashend,resp-std,resp+std, alpha=.1)

    
        
        ofe.set_xlabel('time relative to last flash [s]', fontsize = fontsize, fontweight = 'bold')
        lfe.set_xlabel('time relative to omitted flash [s]', fontsize = fontsize, fontweight = 'bold')

    
        ofe.locator_params(axis = 'x', nbins=5)
        #ofe.set_ylim(0, 8)
        ofe.set_xlim(-.5, 1)
        ofe.spines['top'].set_visible(False)
        ofe.spines['right'].set_visible(False)
        ofe.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
        ofe.tick_params(axis='both', which='major', labelsize=fontsize_ticks) 
        lfe.locator_params(axis = 'x', nbins=5)
        #lfe.set_ylim(0, 8)
        lfe.set_xlim(-.5, 1)
        lfe.spines['top'].set_visible(False)
        lfe.spines['right'].set_visible(False)
        lfe.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
        lfe.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    fig.legend()


    delays_lf = mean_delays
    delays_of = mean_delays-periods
   

    if smooth_peak is True :
        delays_lf = np.asarray(delays_control)
        delays_of = np.asarray(delays_control)-periods
        # delays_lf = np.asarray(mean_delays)
        # delays_of = np.asarray(mean_delays) - periods

        #delays_lf = np.nanmean(delays_control)
        #delays_of = np.nanmean(delays_control)-periods



    delay = fig.add_subplot(gs[:,1])

    popt_of,_ = curve_fit(slope,periods,delays_of)
    popt_lf,_ = curve_fit(slope,periods,delays_lf)

    #manual peak
    #delay.plot(periods, slope(periods,all_slopes_control[i],all_offsets_control[i]), color = 'k', linestyle = ':', alpha = 0.1)

    delay.plot(periods,delays_lf,'k', linewidth = lw, alpha = 1)
    delay.scatter(periods,delays_lf)
    delay.fill_between(periods,delays_lf-std_delays, delays_lf+std_delays, alpha = 0.1, color = 'k')

    delay.plot(periods,delays_of,'g', linewidth = lw, alpha = 0.1)
    delay.scatter(periods,delays_of)
    delay.fill_between(periods,delays_of-std_delays, delays_of+std_delays, alpha = 0.1, color = 'g')



    delay.plot(periods, slope(periods,*popt_lf),
                                color = 'k', linestyle = '--',
                                label = popt_lf[0]) 
    delay.plot(periods, slope(periods,1,popt_lf[1]), color = 'k', linestyle = ':', alpha = 1, label = '1')

   
        
    delay.plot(periods, slope(periods,*popt_of), color = 'k',
                              linestyle = '--', alpha = .1,
                              label = popt_of[0])
    
    delay.plot(periods, slope(periods,0,popt_of[1]), color = 'k', linestyle = ':', alpha = .1, label = '0')



    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('relative delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    delay.set_xticks(periods)

    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    delay.legend()

    return fig


def plot_all_STAs(cells_dict,sigma = 1, smooth = True):
    
    fig, ax = plt.subplots(2,2, figsize = (20,10))
    time = np.arange(0,1,0.025)

    ax[0,0].set_title('ON Cells') 
    ax[0,1].set_title('OFF Cells') 

    ON_keys = []
    ON_profiles = []

    OFF_keys = []
    OFF_profiles = []

    for cell in cells_dict: 

        print(cell)

        if cells_dict[cell]["STA"]['polarity'] == 'ON':

            if smooth == True:
                profile = gaussian_filter(cells_dict[cell]["STA"]['temporal'],sigma)
            if smooth == False : 
                profile = cells_dict[cell]["STA"]['temporal']

            ax[0,0].plot(time,profile, label = cell, alpha = 0.2, linewidth = 5)
            ax[1,0].plot(cells_dict[cell]['STA']['ellipse'][1,:],cells_dict[cell]['STA']['ellipse'][0,:],
                       label = cell, alpha = 0.2, linewidth = 5)       


            ON_keys.append(cell)
            ON_profiles.append(profile)

        if cells_dict[cell]["STA"]['polarity'] == 'OFF':


            if smooth == True:
                profile = gaussian_filter(cells_dict[cell]["STA"]['temporal'],sigma)
            if smooth == False : 
                profile = cells_dict[cell]["STA"]['temporal']

            ax[0,1].plot(time,profile, label = cell, alpha = 0.2, linewidth = 5)
            ax[1,1].plot(cells_dict[cell]['STA']['ellipse'][1,:],cells_dict[cell]['STA']['ellipse'][0,:],
                       label = cell, alpha = 0.2, linewidth = 5)       


            OFF_keys.append(cell)
            OFF_profiles.append(profile)

    ON_mean = np.mean(ON_profiles, axis = 0)
    OFF_mean = np.mean(OFF_profiles, axis = 0)
    
    ON_std = np.std(ON_profiles, axis = 0)
    OFF_std = np.std(OFF_profiles, axis = 0)

    try:
        ax[0,0].plot(time,ON_mean, color = 'orange', linewidth = 10)
    except:
        None
        
    try: 
        ax[0,1].plot(time,OFF_mean, color = 'blue', linewidth = 10)
    except:
        None
        
    ax[0,0].legend() 
    ax[0,1].legend()
    ax[1,0].legend()
    ax[1,1].legend()
    
    return fig,[ON_keys, ON_profiles,ON_mean,ON_std,OFF_keys,OFF_profiles,OFF_mean,OFF_std]



def plot_mean_STA(ON_mean,ON_std, OFF_mean,OFF_std):
    fig, ax = plt.subplots(1,2, figsize = (20,10))
    time = np.arange(0,1,0.025)


    ax[0].set_title('ON Cells') 
    ax[1].set_title('OFF Cells') 


    ax[0].plot(time,ON_mean, color = 'orange', linewidth = 10)
    ax[0].fill_between(time,ON_mean-ON_std,ON_mean+ON_std, alpha=.1, color = 'orange')

    try:
        ax[1].plot(time,OFF_mean, color = 'blue', linewidth = 10)
        ax[1].fill_between(time,OFF_mean-OFF_std,OFF_mean+OFF_std, alpha=.1, color = 'blue')
    except: 
        None

    
    ax[0].set_xlabel( 'time [s]')
    ax[1].set_xlabel( 'time [s]')
    
    return fig

   
def plot_all_cells_in_one(cells_dict,
    color = 'r',
    fontsize = 20,
    fontsize_legend = 10,
    fontsize_ticks = 10,
    lw = 3) :  
    
    frequencies = ['6_Hz','8_Hz','10_Hz','12_Hz','16_Hz']
    periods = np.array([170,120,100,80,60])    

    fig = plt.figure(figsize = (10,5))
    gs = fig.add_gridspec(5,4)


    #     fig.subplots_adjust(
    #     top=0.875,
    #     bottom=0.085,
    #     left=0.43,
    #     right=0.885,
    #     hspace=0.4,
    #     wspace=0.3
    #     )

    all_responses = {}

    # get all slopes
    all_slopes_control = []
    all_slopes_strychnine = []

    all_delays_control = []
    all_delays_strychnine = []

    all_amps_control = []
    all_amps_strychnine = []

    all_offsets_control = []
    all_offsets_strychnine = []



    for i,frq in enumerate(frequencies):

            time = cells_dict["cell_0"]['response_data']['osr_times'][i]
            lastflashend = cells_dict["cell_0"]['response_data']['lastflashends'][i]

            traces = fig.add_subplot(gs[i, 0]) #, sharex = traces, sharey = traces)

            traces.set_xlabel('time [s]', fontsize = fontsize, fontweight = 'bold')
            traces.set_ylabel(frq,  fontsize = fontsize, fontweight = 'bold')

            traces.locator_params(axis = 'x', nbins=5)
            #traces.set_ylim(0, 8)
            traces.set_xlim(-.5, 1)
            traces.spines['top'].set_visible(False)
            traces.spines['right'].set_visible(False)
            traces.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
            traces.tick_params(axis='both', which='major', labelsize=fontsize_ticks)


            resps_control = []
            resps_strych = []

            all_responses[frq] = {}



            for cell in cells_dict:


                #get response
                resp_control = cells_dict[cell]['response_data']['responses_control'][i]
                resp_strych = cells_dict[cell]['response_data']['responses_strychnine'][i]

                resps_control.append(resp_control)
                resps_strych.append(resp_strych)


                if i == 0:
                    sl = cells_dict[cell]['slope_data']['slope_control']
                    dls = np.array(cells_dict[cell]['slope_data']['peaks_control'])*1000
                    amps = cells_dict[cell]['slope_data']['amps_control']
                    off = cells_dict[cell]['slope_data']['offset_control']*1000

                    all_slopes_control.append(sl)
                    all_delays_control.append(dls)
                    all_amps_control.append(amps)
                    all_offsets_control.append(off)

                    sl_s = cells_dict[cell]['slope_data']['slope_strych']
                    dls_s = np.array(cells_dict[cell]['slope_data']['peaks_strych'])*1000
                    amps_s = cells_dict[cell]['slope_data']['amps_strych']
                    off_s = cells_dict[cell]['slope_data']['offset_strych']*1000

                    all_slopes_strychnine.append(sl_s)
                    all_delays_strychnine.append(dls_s)
                    all_amps_strychnine.append(amps_s)
                    all_offsets_strychnine.append(off_s)


                peak_control_man = cells_dict[cell]['slope_data']['peaks_control'][i]
                peak_strych_man = cells_dict[cell]['slope_data']['peaks_strych'][i]

                traces.plot(time-lastflashend,resp_control, color = 'k', alpha =.1, linewidth = lw)
                traces.plot(time-lastflashend,resp_strych, color = color, alpha =.1, linewidth = lw)


                traces.axvline(peak_control_man,linestyle = ':', color = 'k', alpha =.1, linewidth = lw)
                traces.axvline(peak_strych_man,linestyle = ':', color = color, alpha =.1, linewidth = lw)



            all_responses[frq]['control'] = resps_control
            all_responses[frq]['strychnine'] = resps_strych


    delay = fig.add_subplot(gs[:,1])



    for i in range(len(cells_dict)):

        #manual peak
        delay.plot(periods, slope(periods,all_slopes_control[i],all_offsets_control[i]), color = 'k', linestyle = ':', alpha = 0.1)
        delay.plot(periods, slope(periods,all_slopes_strychnine[i],all_offsets_strychnine[i]), color = 'r', linestyle = ':',alpha = 0.1)

        delay.plot(periods,all_delays_control[i],'k-o', linewidth = lw, alpha = 0.1)
        delay.plot(periods,all_delays_strychnine[i],'r-o', linewidth = lw, alpha = 0.1)


    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    delay.set_xticks(periods)

    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    delay.legend()






    delay = fig.add_subplot(gs[:,2])

    all_delays_control_centered0 = []
    all_delays_strychnine_centered0 = []
    all_amps_control_centered0 = []
    all_amps_strychnine_centered0 = []

    for i in range(len(cells_dict)):

        delay.plot(periods,(all_delays_control[i]-all_delays_control[i][-1]),'k-o', linewidth = lw, alpha = 0.1)
        delay.plot(periods,(all_delays_strychnine[i]-all_delays_strychnine[i][-1]),'r-o', linewidth = lw, alpha = 0.1)

        all_delays_control_centered0.append(all_delays_control[i]-all_delays_control[i][-1])
        all_delays_strychnine_centered0.append(all_delays_strychnine[i]-all_delays_strychnine[i][-1])
        
        all_amps_control_centered0.append(all_amps_control[i]-all_amps_control[i][0])
        all_amps_strychnine_centered0.append(all_amps_strychnine[i]-all_amps_control[i][0])


    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    delay.set_xticks(periods)

    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    delay.legend()


    delay = fig.add_subplot(gs[:,3])


    all_delays_control_centeredmean = []
    all_delays_strychnine_centeredmean = []


    for i in range(len(cells_dict)):

        delay.plot(periods,(all_delays_control[i]-np.mean(all_delays_control[i])),'k-o', linewidth = lw, alpha = 0.1)
        delay.plot(periods,(all_delays_strychnine[i]-np.mean(all_delays_strychnine[i])),'r-o', linewidth = lw, alpha = 0.1)

        all_delays_control_centeredmean.append(all_delays_control[i]-np.mean(all_delays_control[i]))
        all_delays_strychnine_centeredmean.append(all_delays_strychnine[i]-np.mean(all_delays_strychnine[i]))



    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    delay.set_xticks(periods)

    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    delay.legend()
    
    return fig, [all_responses,
                 
                all_slopes_control,
                all_slopes_strychnine,

                all_delays_control,
                all_delays_strychnine,

                all_delays_control_centeredmean,
                all_delays_strychnine_centeredmean, 

                all_delays_control_centered0,
                all_delays_strychnine_centered0,

                all_amps_control,
                all_amps_strychnine,
                 
                all_amps_control_centered0,
                all_amps_strychnine_centered0,

                all_offsets_control,
                all_offsets_strychnine]


def plot_all_cells_control_aligned(cells_dict,
    color = 'r',
    fontsize = 20,
    fontsize_legend = 10,
    fontsize_ticks = 10,
    lw = 3) :  
    
    frequencies = ['6_Hz','8_Hz','10_Hz','12_Hz','16_Hz']
    periods = np.array([170,120,100,80,60])    

    fig = plt.figure(figsize = (10,5))
    gs = fig.add_gridspec(5,4)


    #     fig.subplots_adjust(
    #     top=0.875,
    #     bottom=0.085,
    #     left=0.43,
    #     right=0.885,
    #     hspace=0.4,
    #     wspace=0.3
    #     )

    all_responses = {}

    # get all slopes
    all_slopes_control = []

    all_delays_control = []

    all_amps_control = []

    all_offsets_control = []



    for i,frq in enumerate(frequencies):

            time = cells_dict["cell_0"]['response_data']['osr_times'][i]
            lastflashend = cells_dict["cell_0"]['response_data']['lastflashends'][i]

            traces = fig.add_subplot(gs[i, 0]) #, sharex = traces, sharey = traces)

            traces.set_xlabel('time [s]', fontsize = fontsize, fontweight = 'bold')
            traces.set_ylabel(frq,  fontsize = fontsize, fontweight = 'bold')

            traces.locator_params(axis = 'x', nbins=5)
            #traces.set_ylim(0, 8)
            #traces.set_xlim(-.5, 1)
            traces.spines['top'].set_visible(False)
            traces.spines['right'].set_visible(False)
            traces.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
            traces.tick_params(axis='both', which='major', labelsize=fontsize_ticks)


            resps_control = []

            all_responses[frq] = {}



            for cell in cells_dict:


                #get response
                resp_control = cells_dict[cell]['response_data']['responses_control'][i]

                resps_control.append(resp_control)


                if i == 0:
                    sl = cells_dict[cell]['slope_data']['slope_control']
                    dls = np.array(cells_dict[cell]['slope_data']['peaks_control'])*1000
                    amps = cells_dict[cell]['slope_data']['amps_control']
                    off = cells_dict[cell]['slope_data']['offset_control']*1000

                    all_slopes_control.append(sl)
                    all_delays_control.append(dls)
                    all_amps_control.append(amps)
                    all_offsets_control.append(off)


                peak_control_man = cells_dict[cell]['slope_data']['peaks_control'][i]
                peak_16Hz = cells_dict[cell]['slope_data']['peaks_control'][-1]+lastflashend

                traces.plot(time-peak_16Hz,resp_control, alpha =.1, linewidth = lw)


                traces.axvline(peak_control_man-peak_16Hz+lastflashend,linestyle = ':', alpha =.1, linewidth = lw)



            all_responses[frq]['control'] = resps_control

  



    delay = fig.add_subplot(gs[:,2])

    all_delays_control_centered0 = []
    all_delays_strychnine_centered0 = []

    for i in range(len(cells_dict)):

        delay.plot(periods,(all_delays_control[i]-all_delays_control[i][-1]),'k-o', linewidth = lw, alpha = 0.1)

        all_delays_control_centered0.append(all_delays_control[i]-all_delays_control[i][-1])


    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    delay.set_xticks(periods)

    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    delay.legend()


    
    return fig, [all_responses,
                 
                all_slopes_control,

                all_delays_control,

                all_delays_control_centered0,

                all_amps_control,

                all_offsets_control]
  

    
    
def plot_mean_all_cells(cells_dict,
                       all_responses,
                    mean_slopes_control,
            mean_delays_control_centeredmean,
            mean_delays_control_centered0,
            mean_delays_control,
            mean_amps_control,
            mean_offsets_control,

            mean_slopes_strychnine,
            mean_delays_strychnine_centeredmean,
            mean_delays_strychnine_centered0,
            mean_delays_strychnine,
            mean_amps_strychnine,
            mean_offsets_strychnine,
                        std_slopes_control,
                std_delays_control_centeredmean,
                std_delays_control_centered0,
                std_delays_control,
                std_amps_control,
                std_offsets_control,

                std_slopes_strychnine,
                std_delays_strychnine_centeredmean,
                std_delays_strychnine_centered0,
                std_delays_strychnine,
                std_amps_strychnine,
                std_offsets_strychnine,
                          
                popt_control_mean_centered0,
                popt_strychnine_mean_centered0,
                popt_control_mean_centeredmean,
                popt_strychnine_mean_centeredmean,   
                all_responses_2 = None,
     
                color = 'r',
    fontsize = 20,
    fontsize_legend = 10,
    fontsize_ticks = 10,
    lw = 3 ):
       
    frequencies = ['6_Hz','8_Hz','10_Hz','12_Hz','16_Hz']
    periods = np.array([170,120,100,80,60])    

    fig = plt.figure(figsize = (10,5))
    gs = fig.add_gridspec(5,4)


    #     fig.subplots_adjust(
    #     top=0.875,
    #     bottom=0.085,
    #     left=0.43,
    #     right=0.885,
    #     hspace=0.4,
    #     wspace=0.3
    #     )



    for i,frq in enumerate(frequencies):

            time = cells_dict['cell_0']['response_data']['osr_times'][i]
            lastflashend = cells_dict['cell_0']['response_data']['lastflashends'][i]

            traces = fig.add_subplot(gs[i, 0]) #, sharex = traces, sharey = traces)

            traces.set_xlabel('time [s]', fontsize = fontsize, fontweight = 'bold')
            traces.set_ylabel(frq,  fontsize = fontsize, fontweight = 'bold')

            traces.locator_params(axis = 'x', nbins=5)
            #traces.set_ylim(0, 8)
            traces.set_xlim(-.5, 1)
            traces.spines['top'].set_visible(False)
            traces.spines['right'].set_visible(False)
            traces.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
            traces.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

            # plot mean response
            traces.plot(time-lastflashend,all_responses[frq]['means']['control'], color = 'k', alpha =1, linewidth = lw)
            if all_responses_2 is None:
                traces.plot(time-lastflashend,all_responses[frq]['means']['strychnine'], color = color, alpha =1, linewidth = lw)
            else:
                traces.plot(time-lastflashend,all_responses_2[frq]['means']['control'], color = color, alpha =1, linewidth = lw)


            # plot std response
            traces.fill_between(time-lastflashend,all_responses[frq]['means']['control'] + all_responses[frq]['stds']['control'],
                                                  all_responses[frq]['means']['control'] - all_responses[frq]['stds']['control'],
                                                  color = 'k', alpha =0.1)
            if all_responses_2 is None:
                traces.fill_between(time-lastflashend,all_responses[frq]['means']['strychnine'] + all_responses[frq]['stds']['strychnine'],
                                          all_responses[frq]['means']['strychnine'] - all_responses[frq]['stds']['strychnine'],
                                          color = color, alpha =0.1)
            else:
                traces.fill_between(time-lastflashend,all_responses_2[frq]['means']['control'] + all_responses_2[frq]['stds']['control'],
                                          all_responses_2[frq]['means']['control'] - all_responses_2[frq]['stds']['control'],
                                          color = color, alpha =0.1)


            # plot mean peak
            traces.axvline(mean_delays_control[i]/1000,linestyle = ':', color = 'k', alpha =1, linewidth = lw)
            traces.axvline(mean_delays_strychnine[i]/1000,linestyle = ':', color = color, alpha =1, linewidth = lw)

            # plot std peak
            traces.axvspan(mean_delays_control[i]/1000 + std_delays_control[i]/1000,
                           mean_delays_control[i]/1000 - std_delays_control[i]/1000,
                           color = 'k', alpha =0.1)
            traces.axvspan(mean_delays_strychnine[i]/1000 + std_delays_strychnine[i]/1000,
                           mean_delays_strychnine[i]/1000 - std_delays_strychnine[i]/1000,
                           color = color, alpha =0.1)



    #plot delay curve raw       
    delay = fig.add_subplot(gs[:,1])

    # plot slope
    delay.plot(periods, slope(periods,mean_slopes_control,mean_offsets_control), color = 'k', linestyle = ':', alpha = 1 , label = f'slope = {mean_slopes_control:.2f}')
    delay.plot(periods, slope(periods,mean_slopes_strychnine,mean_offsets_strychnine), color = 'r', linestyle = ':',alpha = 1, label = f'slope = {mean_slopes_strychnine:.2f}')


    # plot mean delays
    delay.plot(periods,mean_delays_control,'k-o', linewidth = lw, alpha = 1)
    delay.plot(periods,mean_delays_strychnine,'r-o', linewidth = lw, alpha = 1)



    # plot std delays
    delay.fill_between(periods,mean_delays_control + std_delays_control,
                               mean_delays_control - std_delays_control,
                               color = 'k',alpha = 0.1)

    delay.fill_between(periods,mean_delays_strychnine + std_delays_strychnine,
                               mean_delays_strychnine - std_delays_strychnine,
                               color = 'r',alpha = 0.1)


    #plot errorbars
    delay.errorbar(periods,mean_delays_control, yerr = std_delays_control, color = 'k')
    delay.errorbar(periods,mean_delays_strychnine, yerr = std_delays_strychnine, color = 'r')




    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    delay.set_xticks(periods)

    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    delay.legend()



    # delay curve centered around 0 


    delay = fig.add_subplot(gs[:,2])



    # plot slope mean responses 
    delay.plot(periods, slope(periods,*popt_control_mean_centered0),
               color = 'k', linestyle = ':', alpha = 1 , label = f'slope = {popt_control_mean_centered0[0]:.2f}')
    delay.plot(periods, slope(periods,*popt_strychnine_mean_centered0),
               color = 'r', linestyle = ':',alpha = 1, label = f'slope = {popt_strychnine_mean_centered0[0]:.2f}')

    # plot slope all responses 
    # delay.plot(periods, slope(periods,*popt_control_all_centered0),
    #            color = 'k', linestyle = ':', alpha = 1 , label = f'slope = {popt_control_all_centered0[0]:.2f}')
    # delay.plot(periods, slope(periods,*popt_strychnine_all_centered0),
    #            color = 'r', linestyle = ':',alpha = 1, label = f'slope = {popt_strychnine_all_centered0[0]:.2f}')



    #plot mean 
    delay.plot(periods,mean_delays_control_centered0,'k-o', linewidth = lw, alpha = 1)
    delay.plot(periods,mean_delays_strychnine_centered0,'r-o', linewidth = lw, alpha = 1)


    # plot std delays
    delay.fill_between(periods,mean_delays_control_centered0 + std_delays_control_centered0,
                               mean_delays_control_centered0 - std_delays_control_centered0,
                               color = 'k',alpha = 0.1)

    delay.fill_between(periods,mean_delays_strychnine_centered0 + std_delays_strychnine_centered0,
                               mean_delays_strychnine_centered0 - std_delays_strychnine_centered0,
                               color = 'r',alpha = 0.1)


    #plot errorbars
    delay.errorbar(periods,mean_delays_control_centered0, yerr = std_delays_control_centered0, color = 'k')
    delay.errorbar(periods,mean_delays_strychnine_centered0, yerr = std_delays_strychnine_centered0, color = 'r')



    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    delay.set_xticks(periods)

    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    delay.legend()



    #plot delay curve centered around mean



    delay = fig.add_subplot(gs[:,3])

    # plot slope mean response
    delay.plot(periods, slope(periods,*popt_control_mean_centeredmean),
               color = 'k', linestyle = ':', alpha = 1 , label = f'slope = {popt_control_mean_centeredmean[0]:.2f}')
    delay.plot(periods, slope(periods,*popt_strychnine_mean_centeredmean),
               color = 'r', linestyle = ':',alpha = 1, label = f'slope = {popt_strychnine_mean_centeredmean[0]:.2f}')

    # plot slope all responses
    # delay.plot(periods, slope(periods,*popt_control_all_centeredmean),
    #            color = 'k', linestyle = ':', alpha = 1 , label = f'slope = {popt_control_all_centeredmean[0]:.2f}')
    # delay.plot(periods, slope(periods,*popt_strychnine_all_centeredmean),
    #            color = 'r', linestyle = ':',alpha = 1, label = f'slope = {popt_strychnine_all_centeredmean[0]:.2f}')


    #plot response
    delay.plot(periods,mean_delays_control_centeredmean,'k-o', linewidth = lw, alpha = 1)
    delay.plot(periods,mean_delays_strychnine_centeredmean,'r-o', linewidth = lw, alpha = 1)

    # plot std delays
    delay.fill_between(periods,mean_delays_control_centeredmean + std_delays_control_centeredmean,
                               mean_delays_control_centeredmean - std_delays_control_centeredmean,
                               color = 'k',alpha = 0.1)

    delay.fill_between(periods,mean_delays_strychnine_centeredmean + std_delays_strychnine_centeredmean,
                               mean_delays_strychnine_centeredmean - std_delays_strychnine_centeredmean,
                               color = 'r',alpha = 0.1)    

    #plot errorbars
    delay.errorbar(periods,mean_delays_control_centeredmean, yerr = std_delays_control_centeredmean, color = 'k')
    delay.errorbar(periods,mean_delays_strychnine_centeredmean, yerr = std_delays_strychnine_centeredmean, color = 'r')



    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    delay.set_xticks(periods)

    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)

    delay.legend()
    
    return fig




def plot_boxplot(all_slopes_control,all_slopes_strychnine,  
                 color = 'r',
                 ticklabels = ['control', 'strychnine'],
    fontsize = 20,
    fontsize_legend = 10,
    fontsize_ticks = 10,
    lw = 3 ):
    #ttest
    stat, p = stats.ttest_rel(all_slopes_control, all_slopes_strychnine)

    if p < 0.05:
        print(f"significant difference, p = {p:.2e}")
    if p > 0.05 : 
        print(f"NOT significant, p = {p:.2e}")




    fig, ax = plt.subplots(1,1, figsize = (10,10))


    ax.set_ylabel('slope') 

    c = "k"
    ax.boxplot(all_slopes_control,
                patch_artist=True,
                positions = [1],
                boxprops=dict(facecolor=c, color=c, alpha = 0.5),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c),
                )

    c = color
    ax.boxplot(all_slopes_strychnine,
                patch_artist=True,
                positions = [2],
                boxprops=dict(facecolor=c, color=c, alpha = 0.5),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c),
                )



    #ax.boxplot([all_slopes_control, all_slopes_strychnine], labels =['control','strychnine'])

    ax.set_ylabel('slope',  fontsize = fontsize, fontweight = 'bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks([1,2],
                  ticklabels)

    ax.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    ax.tick_params(axis='both', which='major', labelsize=fontsize_ticks)
    
    return fig
   


def plot_amplitudes(all_amps_control,all_amps_strychnine,color = 'r',
                    
        fontsize = 20,
        fontsize_legend = 10,
        fontsize_ticks = 10,
        lw = 3):

    
        frequencies = ['6_Hz','8_Hz','10_Hz','12_Hz','16_Hz']

        fig, ax = plt.subplots(1,1, figsize = (10,10))

        ax.set_title('Amplitudes Control vs Strychnine') 

    
        ax.scatter(all_amps_control,all_amps_control, color = 'r')
        ax.plot(np.arange(0,60,1), slope(np.arange(0,60,1),1,0), color = 'k', linestyle = '--')
        ax.set_xlabel('control amplitude',  fontsize = fontsize, fontweight = 'bold')
        ax.set_ylabel('strychnine amplitude',  fontsize = fontsize, fontweight = 'bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


        ax.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
        ax.tick_params(axis='both', which='major', labelsize=fontsize_ticks)
        
        return fig

    
def plot_amplitudes_by_frequency(all_amps_control,all_amps_strychnine,color = 'r',
        labels = ['control amplitude', 'strychnine amplitude'],          
        fontsize = 20,
        fontsize_legend = 10,
        fontsize_ticks = 10,
        lw = 3):

    
        frequencies = ['6_Hz','8_Hz','10_Hz','12_Hz','16_Hz']

        fig, ax = plt.subplots(1,1, figsize = (10,10))

        ax.set_title('Amplitudes Control vs Strychnine') 
        
        palette = sns.color_palette(None,len(frequencies))

        for i,frq in enumerate(frequencies):
            ax.scatter(np.asarray(all_amps_control)[:,i],np.asarray(all_amps_strychnine)[:,i], label = frq, 
                       color = palette[i], alpha = 1)
          
            ax.scatter(np.nanmean(all_amps_control,axis = 0)[i],np.nanmean(all_amps_control,axis = 0)[i],
                   color = palette[i])
        ax.plot(np.arange(0,60,1), slope(np.arange(0,60,1),1,0), color = 'k', linestyle = '--')
        ax.set_xlabel(labels[0],  fontsize = fontsize, fontweight = 'bold')
        ax.set_ylabel(labels[1],  fontsize = fontsize, fontweight = 'bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


        ax.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
        ax.tick_params(axis='both', which='major', labelsize=fontsize_ticks)
        
        fig.legend()
        return fig

    
     
  
def plot_amplitudes_by_cell(all_amps_control,all_amps_strychnine,color = 'r',
                    
        fontsize = 20,
        fontsize_legend = 10,
        fontsize_ticks = 10,
        lw = 3):

        
        frequencies = ['6_Hz','8_Hz','10_Hz','12_Hz','16_Hz']

        fig, ax = plt.subplots(1,1, figsize = (10,10))

        ax.set_title('Amplitudes Control vs Strychnine') 
        palette = sns.color_palette(None,len(all_amps_control))


        for i in range(len(all_amps_control)):
            ax.scatter(np.asarray(all_amps_control)[i,:],np.asarray(all_amps_strychnine)[i,:],
                       color = palette[i],
                       label = f'cell {i}', alpha = 0.5)
          
            ax.scatter(np.nanmean(all_amps_control,axis = 1)[i],np.nanmean(all_amps_strychnine,axis = 1)[i],
                   color = palette[i])
        ax.plot(np.arange(0,60,1), slope(np.arange(0,60,1),1,0), color = 'k', linestyle = '--')
        ax.set_xlabel('control amplitude',  fontsize = fontsize, fontweight = 'bold')
        ax.set_ylabel('strychnine amplitude',  fontsize = fontsize, fontweight = 'bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


        ax.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
        ax.tick_params(axis='both', which='major', labelsize=fontsize_ticks)
        
        ax.legend()
        
        return fig


