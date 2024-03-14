import matplotlib.pyplot as plt
from utils import slope_fun
import numpy as np






def plot_response(simulation,ax,color,label,align_last_flash = False):

    response = simulation['RG']

    if align_last_flash == False:
        time = simulation['time']
    else: 
        time = simulation['time'] - simulation['lastflash_tp']


    ax.plot(time, response, color = color ,linewidth = 3,alpha = 1, linestyle = '-', label = label)

    



def plot_data(data,ax,color,label):

    time = data['time']
    response = data['response']

    ax.plot(time,response, color = color ,linewidth = 3,alpha = 1, linestyle = '-', label = label)






def plot_response_with_stimulus(simulation,data = None):

    time = simulation['time']
    stimulus = simulation['stimulus']
    name = simulation['name']


    fig = plt.figure(figsize = (10,10))
    ax1 = fig.add_subplot(211)
    ax1.plot(time, stimulus, color = 'k', label = 'stimulus')


    ax2 = fig.add_subplot(212)




    plot_response(simulation,ax2,'blue','firing rate prediction')

    if data is not None:
        plot_data(data,'gray', 'cell')

    ax2.set_xlabel('time [s]')
    ax1.set_title(f'Response of Mechanistic Model to {name}')
    fig.legend()

    plt.show()

    return fig




def plot_OSR_simulation(simulations_inp,colors, labels, xlims = (-1,1), data = None, lw = 4):


    
    frequencies = simulations_inp[0]['osrparams']['frequencies']

    fig,ax = plt.subplots(len(frequencies),1, figsize = (10,5), sharex = True, sharey = 'col')

    for x,simulation_dict in enumerate(simulations_inp):

        simulations = simulation_dict['simulations']


        
        for i,key in enumerate(simulations):

            simulation = simulations[key]


            if i == 0:
            

                plot_response(simulation,ax[i],color = colors[x],label = labels[x],align_last_flash = True)
                ax[i].axvline(simulation['delay'], color = colors[x], alpha = .5, linestyle = ':',linewidth = lw, label = 'model peak')

            else:
                    
                plot_response(simulation,ax[i],color = colors[x],label = None,align_last_flash = True)
                ax[i].axvline(simulation['delay'], color = colors[x], alpha = .5, linestyle = ':',linewidth = lw)

            if x == 0: 
                ax[i].set_ylabel(f'{frequencies[i]} Hz')




    ax[-1].set_xlabel('time [s]')
    ax[-1].set_xlim(xlims)

    fig.legend()

    plt.show()

    return fig





def plot_slope(simulations,colors,labels,lw = 4):

    fig = plt.figure(figsize = (10,5))

    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)


    for x,simulation_dict in enumerate(simulations): 

        periods = simulation_dict['osrparams']['periods']
        delays = simulation_dict['delays']
        maxs_n = simulation_dict['maxs_n']

        slope = simulation_dict['slope']
        offset = simulation_dict['offset']



        
        ax1.plot(periods,delays, color = colors[x],alpha = 1, linewidth = lw)
        ax1.plot(periods,slope_fun(periods,slope,offset), linestyle = ':', color = colors[x],linewidth = lw, alpha = 0.5,label = f'slope = {slope:.2f},  {labels[x]} ')
        
        ax2.plot(periods,maxs_n,color = colors[x],alpha = 1, linewidth = lw)

    ax1.set_xlabel('periods [s]')
    ax1.set_ylabel('delay [s]')
    ax1.legend()
    ax1.set_title('Predictive Delay Curve')
    

    ax2.set_xlabel('periods [s]')
    ax2.set_ylabel(f'nA1 max')
    ax2.set_title('Maximum Occupancy after Flash Train')
    
    
    plt.show()

    return fig


def plot_OSR_3F_oneresponse(simulation, keys, 
    fontsize = 40,
    fontsize_legend = 25,
    fontsize_ticks = 20,
    lw = 5):    


    fig = plt.figure()
    gs = fig.add_gridspec(3,1)

    fig.subplots_adjust(
    top=0.875,
    bottom=0.085,
    left=0.43,
    right=0.885,
    hspace=0.4,
    wspace=0.3
    )

    
    frequencies = simulation['osrparams']['frequencies']
    #plot response traces for 3 different frequencies

    for i,key in enumerate(keys):
        
            time = simulation['simulations'][key]['time']

            stim = simulation['simulations'][key]['stimulus']

            lastflashend = simulation['simulations'][key]['lastflash_tp']

            
            # simulation 1 
            response = simulation['simulations'][key]['RG']
            delay = simulation['simulations'][key]['delay']
            peak_amp = simulation['simulations'][key]['peak_amplitude']
            
            # simulation 1 


            traces = fig.add_subplot(gs[i, 0])#, sharex = traces, sharey = traces)
            flashes = np.where(np.diff(stim) != 0)[0].tolist()

            for f in range(len(flashes)):  
                if  not f % 2 :
                    traces.axvspan(time[flashes[f]]-lastflashend, time[flashes[f+1]+1]-lastflashend, color = 'k', alpha = 0.1)

            if i == 0  or i == 1: 
                traces.plot(time-lastflashend,response, color='black', linewidth = lw)

            else:
                traces.plot(time-lastflashend,response, color='black',linewidth = lw, label = 'full model')
                traces.set_xlabel('time [s]', fontsize = fontsize, fontweight = 'bold')



            traces.scatter(delay,peak_amp, color = 'k',)

            traces.axvline(delay, color = 'k', alpha = 1, linewidth = 5 )




            traces.set_ylabel(f'{frequencies[i]} Hz',  fontsize = fontsize, fontweight = 'bold')

            traces.locator_params(axis = 'x', nbins=5)
            #traces.set_ylim(0, 8)
            traces.set_xlim(-.4, 1)
            traces.spines['top'].set_visible(False)
            traces.spines['right'].set_visible(False)
            traces.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
            traces.tick_params(axis='both', which='major', labelsize=fontsize_ticks)


    #fig.legend(fontsize = fontsize_legend, ncol= 3,frameon=False )
    
    #plt.show()
    return fig   
    
    
def plot_OSR_3F(simulation, simulation2, keys, color, labels,
    letter = 'A',
    fontsize_legend = 20,
    fontsize_labels = 20,
    fontsize_panellabel = 30,
    fontsize_ticks = 10,
    lw = 3,
    ms = 20,
    panellabel_position = [-0.1, 1.15],
    frequencytext_position = [0.15,1.1],
    figsize = (5,5)
    ):    


    fig = plt.figure(figsize = figsize)
    gs = fig.add_gridspec(3,1)

    fig.subplots_adjust(top=0.81,
    bottom=0.115,
    left=0.16,
    right=0.96,
    hspace=0.275,
    wspace=0.2)

    A = fig.add_subplot(gs[0:,0], frameon = False)
    A.set_xticks([])
    A.spines['left'].set_color('white')
    A.tick_params(axis='y', colors='white')
    A.text(*panellabel_position, letter, transform=A.transAxes,
      fontsize=fontsize_panellabel, fontweight='bold', va='top', ha='right')
    A.set_ylabel('Firing Rate',fontsize = fontsize_labels)
    
    frequencies = simulation['osrparams']['frequencies']
    #plot response traces for 3 different frequencies

    for i,key in enumerate(keys):
        
            time = simulation['simulations'][key]['time']
            time2 = simulation2['simulations'][key]['time']

            stim = simulation['simulations'][key]['stimulus']

            lastflashend = simulation['simulations'][key]['lastflash_tp']
            lastflashend2 = simulation2['simulations'][key]['lastflash_tp']

            
            # simulation 1 
            response = simulation['simulations'][key]['RG']
            delay = simulation['simulations'][key]['delay']
            peak_amp = simulation['simulations'][key]['peak_amplitude']
            
            # simulation 1 
            response2 = simulation2['simulations'][key]['RG']
            delay2 = simulation2['simulations'][key]['delay']
            peak_amp2 = simulation2['simulations'][key]['peak_amplitude']


            traces = fig.add_subplot(gs[i, 0], sharey = A)#, sharex = traces, sharey = traces)
            flashes = np.where(np.diff(stim) != 0)[0].tolist()

            for f in range(len(flashes)):  
                if  not f % 2 :
                    traces.axvspan(time[flashes[f]]-lastflashend, time[flashes[f+1]+1]-lastflashend, color = 'k', alpha = 0.1)

            if i == 0  or i == 1: 
                traces.plot(time2-lastflashend2,response2, color = color, alpha =.7, linewidth = lw)
                traces.plot(time-lastflashend,response, color='black', linewidth = lw)

            else:
                traces.plot(time2-lastflashend2,response2, color = color, alpha =.7, linewidth = lw, label = labels[1])
                traces.plot(time-lastflashend,response, color='black',linewidth = lw, label = labels[0])
                traces.set_xlabel('time [s]', fontsize = fontsize_labels)



            traces.scatter(delay,peak_amp, color = 'k',)
            traces.scatter(delay2,peak_amp2, color = color)

            traces.axvline(delay, color = 'k', alpha = .5, linewidth = 5 )
            traces.axvline(delay2, color = color, alpha = .5,linewidth = 5)

            traces.axvspan(delay,delay2, color = color, alpha = 0.1)


            traces.set_title(key,fontsize = fontsize_labels, loc = 'left')
            #traces.set_ylabel(f'{frequencies[i]} Hz',  fontsize = fontsize, fontweight = 'bold')

            traces.locator_params(axis = 'x', nbins=5)
            traces.locator_params(axis = 'y', nbins=2)
            #traces.set_ylim(0, 8)
            traces.set_xlim(-.4, 1)
            traces.spines['top'].set_visible(False)
            traces.spines['right'].set_visible(False)
            traces.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
            traces.tick_params(axis='both', which='major', labelsize=fontsize_ticks)


    #fig.legend(fontsize = fontsize_legend, bbox_to_anchor = (.5,.5))
    
    #plt.show()
    return fig




def plot_delay_figure(simulation, simulation2,color,
    letter = 'B',
    fontsize_legend = 20,
    fontsize_labels = 20,
    fontsize_panellabel = 30,
    fontsize_ticks = 10,
    lw = 3,
    ms = 20,
    panellabel_position = [-0.1, 1.15],
    frequencytext_position = [0.15,1.1],
    figsize = (5,5)
    ):    

    

    fig = plt.figure(figsize = figsize)
    gs = fig.add_gridspec(1,1)

    fig.subplots_adjust(top=0.81,
    bottom=0.115,
    left=0.16,
    right=0.96)
    
    A = fig.add_subplot(gs[0:,0], frameon = False)
    A.set_xticks([])
    A.spines['left'].set_color('white')
    A.tick_params(axis='y', colors='white')
    A.text(*panellabel_position, letter, transform=A.transAxes,
      fontsize=fontsize_panellabel, fontweight='bold', va='top', ha='right')
    
    # simulation 1 
    delays = simulation['delays']*1000
    slope = simulation['slope']
    offset = simulation['offset']*1000

    # simulation 1 
    delays2 = simulation2['delays']*1000
    slope2 = simulation2['slope']
    offset2 = simulation2['offset']*1000

    periods = simulation['osrparams']['periods']*1000

    delay = fig.add_subplot(gs[0,0])
    delay.plot(periods,delays,color = 'k', linewidth = lw)
    delay.scatter(periods,delays,marker ='o',color ='k', s = ms)

    delay.plot(periods,delays2, color = color, linewidth = lw)
    delay.scatter(periods,delays2, marker ='o',color = color, s = ms)

    #delay.set_title('Delay between \n last flash and OSR',  fontsize = 30, fontweight = 'bold')
    delay.plot(periods,slope_fun(periods,slope,offset), ":", alpha = .5, color = 'black',linewidth = lw, label = f'slope = {slope:.2f}')
    delay.plot(periods,slope_fun(periods,slope2,offset2), ":", alpha = .5, color = color, linewidth = lw, label = f'slope = {slope2:.2f}')
    #delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    #delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    #delay.set_xticks(periods)

    #delay.legend(fontsize = fontsize_legend)
    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    #delay.locator_params(axis = 'x', nbins=3)
    delay.set_xticks(np.round(periods,0))
    delay.set_yticks(np.round(delays,0))
    #C.set_xticklabels(['170', '120'  , '100' , '80', '60'])
    #delay.locator_params(axis = 'y', nbins=2)

    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)
    delay.set_xlabel('flash period [ms]',  fontsize = fontsize_labels)
    delay.set_ylabel('delay [ms]',  fontsize = fontsize_labels)
    #
    fig.legend(fontsize = fontsize_legend, bbox_to_anchor = (1.0,0.4))
    print(f'simulation slope = {slope}')
    print(f'simulation2 slope = {slope2}')
    #plt.show()
    return fig


def plot_delay_figure_one(simulation,fontsize = 40,
    fontsize_legend = 25,
    fontsize_ticks = 20,
    markersize = 120,
    lw = 5):

    

    fig = plt.figure()
    gs = fig.add_gridspec(1,1)

    fig.subplots_adjust(
    top=0.875,
    bottom=0.085,
    left=0.43,
    right=0.885,
    hspace=0.4,
    wspace=0.3
    )

        
    # simulation 1 
    delays = simulation['delays']*1000
    slope = simulation['slope']
    offset = simulation['offset']*1000

    # simulation 1 

    periods = simulation['osrparams']['periods']*1000



    delay = fig.add_subplot(gs[0,0])
    delay.plot(periods,delays,color = 'k', linewidth = lw)
    delay.scatter(periods,delays,marker ='o',color ='k', s = markersize)


    #delay.set_title('Delay between \n last flash and OSR',  fontsize = 30, fontweight = 'bold')
    delay.plot(periods,slope_fun(periods,slope,offset), ":", alpha = .5, color = 'black',linewidth = lw, label = f'slope = {slope:.2f}')
    delay.plot(periods,slope_fun(periods,1,offset), "--", color = 'black',linewidth = lw, label = f'slope = {1}')
    #delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    #delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')

    delay.locator_params(axis = 'y', nbins=5)
    #delay.set_xticks(periods)

    #delay.legend(fontsize = fontsize_legend)
    delay.spines['top'].set_visible(False)
    delay.spines['right'].set_visible(False)
    delay.locator_params(axis = 'x', nbins=3)
    delay.locator_params(axis = 'y', nbins=2)

    delay.tick_params(axis='both', which='minor', labelsize=fontsize_ticks)
    delay.tick_params(axis='both', which='major', labelsize=fontsize_ticks)
    delay.set_xlabel('flash period [ms]',  fontsize = fontsize, fontweight = 'bold')
    delay.set_ylabel('delay [ms]',  fontsize = fontsize, fontweight = 'bold')
    #
    #fig.legend(fontsize = 20, ncol= 1, frameon = False)#, loc = 'upper center', bbox_to_anchor=(0.6, 1.05),)
    print(f'simulation slope = {slope}')
    #plt.show()
    return fig