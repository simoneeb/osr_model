
import numpy as np 
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt
from nonlinearities import sig

from utils import calculate_VG_baseline, calculate_n_eq


class B_Model(object):
    
    def __init__(self,
                 linear_filter,  
                 filtertype, 
                 convolution,
                 system,
                 nonlinearity,
                 stimfunction,
                 
                 params,

                 occupancy = 'dynamic',
                 convolution_type = 'same',
                 nV = False,
                 
                 polarities = ['ON', 'OFF'],
                 filterlength = 1,
                 dt = 0.02):
        

        self.linear_filter = linear_filter 
        self.filtertype =  filtertype 
        self.convolution = convolution
        self.system = system
        self.nonlinearity = nonlinearity
        self.stimfunction = stimfunction
        
        self.params = params

        self.occupancy = occupancy
        self.convolution_type = convolution_type
        self.nV = nV

        self.filterlength = filterlength
        self.polarities = polarities
        self.dt = dt
        
        
        


    def predict(self,
                stim,
                time,
                stimulus_name,
                VB0 = 0,VG0 = 0,n0 = 1,
                print_steps = True):

        
        '''
        function to make a prediction with the full model 
        returns OPL_inputs as functions ,solutions of the dynamical system and nonlinear_response
        '''

        simt = time[-1]
        tau_B = self.params['tau_B']
        tau_A1 = self.params['tau_A1']
        tau_A2 = self.params['tau_A2']
        tau_VR = self.params['tau_VR']
        tau_VR2 = self.params['tau_VR2']

        # calculate scaling factors to keep intermediate voltage responses at similar amplitudes
        SF_B = self.params['SFB']           # [mV/s**2]
        SF_A1 = self.params['SFA1']              # [mV/s**2]
        SF_A2 = self.params['SFA2']             # [mV/s**2]


        #make timeline for filter with the same dt
        filtertime = np.arange(0,self.filterlength,self.dt)

        if self.convolution_type == 'same': 

            if self.polarities[0] is 'ON':
                if self.filtertype == 'monophasic':
                    filter_B = self.linear_filter(filtertime,tau_B)
                if self.filtertype == 'biphasic':
                    filter_B = self.linear_filter(filtertime,tau_B,tau_A2,SF_A2)

            if self.polarities[0] is 'OFF':
                if self.filtertype == 'monophasic':
                    filter_B = -1*self.linear_filter(filtertime,tau_B)
                if self.filtertype == 'biphasic':
                    filter_B = -1*self.linear_filter(filtertime,tau_B,tau_A2,SF_A2)


        #     if self.polarities[1] is 'ON':
        #         filter_A1 = self.linear_filter(filtertime,tau_A1)

        #     if self.polarities[1] is 'OFF':
        #         filter_A1 = -1 * self.linear_filter(filtertime,tau_A1)



        if self.convolution_type == 'VR': 

            if self.polarities[0] is 'ON':
                if self.filtertype == 'monophasic':
                    filter_B = self.linear_filter(filtertime,tau_VR)
                if self.filtertype == 'biphasic':
                    filter_B = self.linear_filter(filtertime,tau_VR,tau_VR2,SF_A2)

        if self.polarities[0] is 'OFF':
                if self.filtertype == 'monophasic':
                    filter_B = -1*self.linear_filter(filtertime,tau_VR)
                if self.filtertype == 'biphasic':
                    filter_B = -1*self.linear_filter(filtertime,tau_VR,tau_VR2,SF_A2)


        #     if self.polarities[1] is 'ON':
        #         filter_A1 = self.linear_filter(filtertime,tau_VR)

        #     if self.polarities[1] is 'OFF':
        #         filter_A1 = -1 * self.linear_filter(filtertime,tau_VR)

            
                
        if print_steps == True:

            print("filter computed")

        


        #convolve
        FB_raw = SF_B * self.convolution(stim,np.flip(filter_B),self.dt)
        FA1_raw = 0 * self.convolution(stim,np.flip(filter_B),self.dt)
        FA2_raw = 0 * self.convolution(stim,np.flip(filter_B),self.dt)

        #rectify
        if self.stimfunction == 'sigmoid_late':
       
            FB_rec = sig(FB_raw,self.params['slope_on'], self.params['threshold_on'], self.params['max_val_on'] )-1#0.5
            FA1_rec= sig(FA1_raw,self.params['slope_on'], self.params['threshold_on'], self.params['max_val_on'] )
            FA2_rec = sig(FA2_raw,self.params['slope_on'], self.params['threshold_on'], self.params['max_val_on'] )


            FB = SF_B * FB_rec
            FA1 = SF_A1 * FA1_rec * -1
            FA2 = SF_A2 * FA2_rec

        else:
            FB = SF_B * FB_raw
            FA1 = SF_A1 * FA1_raw *-1
            FA2 = SF_A2 * FA2_raw

            FB_rec = SF_B * FB_raw
            FA1_rec = SF_A1 * FA1_raw *-1
            FA2_rec = SF_A2 * FA2_raw


        if print_steps == True:

            print("convolution sucessful")

        
        # prepare OPL Inputs 
        print(len(time))
        print(len(FB))
        FB_fun = interp1d(time,FB,fill_value="extrapolate")
        FA1_fun = interp1d(time,FA1,fill_value="extrapolate")
        FA2_fun = interp1d(time,FA2,fill_value="extrapolate")


        OPL_inputs = {'FB': FB_fun,
                    'FA1': FA1_fun,
                    'FA2': FA2_fun}
        
        if print_steps == True:
        
            print("input interpolated")

        
        if self.occupancy == 'fixed':
            sol = solve_ivp(self.system,[0,simt],[VB0,VG0], t_eval = time, args=(self.params,
                                                                                    OPL_inputs))
        if self.occupancy == 'dynamic':
            sol = solve_ivp(self.system,[0,simt],[VB0,n0,VG0], t_eval = time, args=(self.params,
                                                                                    OPL_inputs))

        
        if print_steps == True:

            print('system solved')


        #apply nonlinearity
        nonlinear_response = np.asarray([self.nonlinearity(l,self.params) for l in sol.y[-1]])





        # #some tests 
        # VG_baseline = calculate_VG_baseline(self.params,self.nV)
        # err = 0.01

        # if sol.y[-1][-1] <= VG_baseline-err or sol.y[-1][-1] >= VG_baseline+err:
        #     print("!!!!! VG baseline does not match")

        # if sol.y[-1][-1] <= 0-err or sol.y[-1][-1] >= 0+err:
        #     print(f"!!!!! simulation VG baseline is {sol.y[-1][-1]}")

        # if VG_baseline <= 0-err or VG_baseline >= 0+err:
        #     print(f"!!!!! calculated VG baseline is {VG_baseline}")



        # if self.occupancy == 'dynamic':
        #     n_eq = calculate_n_eq(self.params)

        #     if sol.y[-2][-1] <= n_eq-err or  sol.y[-2][-1] >= n_eq+err:
        #         print(f' !!!!! occupancy equilibrium in calculation and simulation dont match')
        #         print(f'{n_eq} vs {sol.y[-2][-1]}')

        
        out = { 'name': stimulus_name,
                'stimulus': stim,
                'time': time,
                "OPL_inputs":  OPL_inputs,
                "sol" : sol,
                "RG": nonlinear_response }


        return out 


    def  plot_kernels(self):


        if self.convolution_type == 'same' : 
            tau_B = self.params['tau_B']
            tau_A1 = self.params['tau_A1']
            tau_A2 = self.params['tau_A2']
            SF_A2 = self.params['SFA2']

        if self.convolution_type == 'VR':
            tau_B = self.params['tau_VR']
            tau_A1 = self.params['tau_VR']
            tau_A2 = self.params['tau_VR2']
            SF_A2 = self.params['SFA2']


        #make timeline for filter with the same dt
        filtertime = np.arange(0,self.filterlength,self.dt)

        fig = plt.figure()
        if self.filtertype =='monophasic':
            plt.plot(filtertime,self.linear_filter(filtertime,tau_B), color = 'g', label = "kernel B")
        if self.filtertype == 'biphasic': 
            plt.plot(filtertime,self.linear_filter(filtertime,tau_B,tau_A2,SF_A2), color = 'g', label = "kernel B")

        # plt.plot(filtertime,self.linear_filter(filtertime,tau_A1,1,0), color = 'm', label = "kernel A1")
        # print(self.linear_filter(filtertime,tau_A1,0,0))
        plt.legend()
        plt.title( "Filter shapes for OPL input")
        plt.show()
        return fig




    def  plot_sigmoid_late(self):


        fig = plt.figure()
        #make timeline for filter with the same dt
        range = np.arange(-1,1,0.0001)
        si_on  =sig(range,self.params['slope_on'], self.params['threshold_on'], self.params['max_val_on'] )

        plt.plot(range,si_on, color = 'k')
      
        plt.title( " nonlinearity ON")
        plt.show()
        return fig




    def plot_response(self,simulation, xlims =(0.9,2)): 

        name = simulation['name']
        stimulus = simulation['stimulus']
        time = simulation['time']
        sol = simulation['sol']
        OPL_inputs = simulation['OPL_inputs']

        fig = plt.figure(figsize = (10,5))


        ax0 = fig.add_subplot(511)
        ax0.plot(time,stimulus)

        ax1 = fig.add_subplot(512)
        ax1.plot(time,[OPL_inputs['FB'](t) for t in time], color = 'g', linestyle = '--',label = 'FB(t)')
        # ax1.plot(time,[OPL_inputs['FA1'](t) for t in time], color = 'r',linestyle = '--',label = 'FA1(t)')



        ax2 = fig.add_subplot(513)
        ax3 = fig.add_subplot(515)

        ax2.plot(time,sol.y[0],color = 'g', label = 'VB')
        ax2.plot(time,sol.y[0]*sol.y[1],linestyle = ':',color = 'g', label = 'VB dynamic')
        ax3.plot(time,sol.y[2],color = 'r', label = 'VG')
        # ax2.plot(time,sol.y[2],color = 'orange', label = 'VA2')


        ax22 = fig.add_subplot(514)

        if self.occupancy == 'fixed':
            ax22.axhline(self.params['n_A1_star'], color = 'c', label = 'nA1')
            # ax3.plot(time,sol.y[3], color = 'k', label = 'VG')

        if self.occupancy == 'dynamic':
            ax22.plot(time,sol.y[1],color = 'c', label = 'n')
            #ax3.scatter(filtertime,time_rf_smooth, label = 'STA Datapoints')
            # ax3.plot(time,sol.y[4], color = 'k', label = 'VG')





        ax0.set_title('Stimulus')
        ax0.set_xlim(xlims)

        ax1.set_title('OPL Filter')
        ax1.set_xlim(xlims)



        ax2.set_title('Pathway Responses ')
        ax2.set_xlim(xlims)


        ax2.set_title('Occupancy')
        ax22.set_xlim(xlims)




        ax3.set_xlabel('time [s]')
        ax3.set_title('VG response')
        ax3.set_xlim(xlims)


        fig.legend()
        fig.suptitle(f'{name},{self.occupancy}')
        plt.show()

        return fig 