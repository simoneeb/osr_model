import numpy as np
import pickle
import os
from matplotlib import pyplot as plt


        
def slope_fun(x,s,i):
    return s * x + i


#TODO function to fit the slope 


def save_dict(filepath,data):

    #filepath = os.path.join(filepath,filename)

    with open(filepath, 'wb') as handle:
        pickle.dump(data, handle, protocol=4)



def save_fig(filepath,figure):

    #filepath = os.path.join(filepath,filename)

    figure.savefig(filepath)



def load_dict(filepath):

    #filepath_paramset = os.path.join(filepath,filename)

    with open(filepath, "rb") as handle:   #Pickling
        data = pickle.load(handle)

    return data


def make_directory(filepath,paramset):

    filepath_paramset = os.path.join(filepath,paramset)

    if not os.path.isdir(filepath_paramset):
        os.makedirs(filepath_paramset)
    
    return filepath_paramset



def calculate_n_eq(params):

    k_rec = params['k_rec']
    k_rel =  params['k_rel']
    beta =  params['beta']
    theta =  params['theta_A1']
    
    return 1 / (1- (beta *theta* k_rel)/k_rec)



def calculate_theta_B(params,nV = False):

    wB = params['w_B']
    wA1 = params['w_A1']
    wA2 = params['w_A2']
    theta_A1 = params['theta_A1']
    theta_A2 = params['theta_A2']
    nA1 = params['n_A1_star']

    
    if 'w_B2' in params.keys():
        wB2 = params['w_B2']
        theta_B2 = params['theta_B2']

        return -1*((wA1 * nA1*theta_A1) + (wA2 * theta_A2) +(wB2 * theta_B2)) / wB
    
    else: 
        if nV is False : 

            return -1*(wA1 * nA1*theta_A1 + wA2 * theta_A2) / wB

        if nV is True : 

            return -1*(wA1 *theta_A1 + wA2 * theta_A2) / wB




def calculate_VG_baseline(params, nV = False):

    wB = params['w_B']
    wA1 = - params['w_A1']
    wA2 = - params['w_A2']
    theta_A1 = params['theta_A1']
    theta_A2 = params['theta_A2']
    theta_B = params['theta_B']
    nA1 = params['n_A1_star']

    if nV is False : 

        return wB * theta_B -wA1 * nA1 * theta_A1 - wA2 * theta_A2

    if nV is True : 

        return wB * theta_B -wA1 *  theta_A1 - wA2 * theta_A2



def make_param_dict(params, nV = False):

    # calculate scale factors
    params['SFB'] =  (1/params['tau_B'])  * params['scale_mV']              # [mV/s**2]
    params['SFA1'] = (1/params['tau_A1']) * params['scale_mV']              # [mV/s**2]
    params['SFA2']= (1/params['tau_A2']) * params['scale_mV']             # [mV/s**2]
    if 'tau_B2' in params.keys():
        params['SFB2']= (1/params['tau_B2']) * params['scale_mV']             # [mV/s**2]
  

    #calculate n_A1_star
    params['n_A1_star'] = calculate_n_eq(params)

    #calculate theta_B
    params['theta_B'] = calculate_theta_B(params,nV)

    return params


   
