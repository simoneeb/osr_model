   
from nonlinearities import p,sig

def IPL_rectified_occupancy(t,X,params,OPL_inputs):

    """
    dynamical system with rectified synapses and dynamic occupancy
    """

    VB,VA1,VA2,nA1,VG = X
    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  OPL_inputs['FA2'](t),
            (1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1,params['theta_A1']) * nA1,
            -VG/params['tau_G'] + params['w_B'] * p(VB,params['theta_B']) + nA1* params['w_A1'] *  p(VA1,params['theta_A1']) + params['w_A2'] *  p(VA2,params['theta_A2'])]



def IPL_rectified_occupancy_sig(t,X,params,OPL_inputs):

    """
    dynamical system with rectified synapses and dynamic occupancy
    """

    VB,VA1,VA2,nA1,VG = X
    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  OPL_inputs['FA2'](t),
            (1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1,params['theta_A1']) * nA1,
            -VG/params['tau_G'] + params['w_B'] * sig(VB,params) + nA1* params['w_A1'] *  sig(VA1,params) + params['w_A2'] *  sig(VA2,params)]



def IPL_rectified_occupancy_B(t,X,params,OPL_inputs):

    """
    dynamical system with rectified synapses and dynamic occupancy
    """

    VB,VA1,VA2,nA1,VG = X
    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  OPL_inputs['FA2'](t),
            (1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1,params['theta_A1']) * nA1,
            -VG/params['tau_G'] +nA1* params['w_B'] * p(VB,params['theta_B']) + params['w_A1'] *  p(VA1,params['theta_A1']) + params['w_A2'] *  p(VA2,params['theta_A2'])]




def IPL_rectified_occupancy_recip(t,X,params,OPL_inputs):

    """
    dynamical system with rectified synapses and dynamic occupancy
    """

    VB,VA1,VA2,nA1,VG = X
    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t) - params['w_A2']*VA2,
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  params['w_A2']*VB,
            (1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1,params['theta_A1']) * nA1,
            -VG/params['tau_G'] + params['w_B'] * p(VB,params['theta_B']) + nA1* params['w_A1'] *  p(VA1,params['theta_A1']) + 0 *  p(VA2,params['theta_A2'])]



def IPL_occupancy(t,X,params,OPL_inputs):

    """
    dynamical system dynamic occupancy, only A! is rectified
    """

    VB,VA1,VA2,nA1,VG = X
    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  OPL_inputs['FA2'](t),
            (1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1,params['theta_A1']) * nA1,
            -VG/params['tau_G'] + params['w_B'] * VB + nA1* params['w_A1'] *  p(VA1,params['theta_A1']) + params['w_A2'] *  VA2]



def IPL_occupancy_shunting(t,X,params,OPL_inputs):

    """
    dynamical system dynamic occupancy, only A! is rectified
    """

    VB,VA1,VA2,nA1,VG = X
    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  OPL_inputs['FA2'](t),
            (1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1,params['theta_A1']) * nA1,
            -VG*((1/params['tau_G']) + nA1* params['g_A1']* p(VA1,params['theta_A1'])+ params['g_A2'] *  VA2 + params['g_B'] * VB)+ params['g_A2'] *  VA2 + params['w_B'] * VB + + nA1* params['w_A1']* p(VA1,params['theta_A1']) ]




def IPL_occupancy_secondON(t,X,params,OPL_inputs):

    """
    dynamical system dynamic occupancy, only A! is rectified
    """

    VB,VA1,VA2,nA1,VB2,VG = X
    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  OPL_inputs['FA2'](t),
            (1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1,params['theta_A1']) * nA1,
            -VB2/params['tau_B2'] +  OPL_inputs['FB2'](t),
            -VG/params['tau_G'] + params['w_B'] * p(VB,params['theta_B']) + nA1* params['w_A1'] *  p(VA1,params['theta_A1']) + params['w_A2'] *  p(VA2,params['theta_A2']) + params['w_B2'] * p(VB2,params['theta_B2'])]



def IPL_occupancy_bipolar(t,X,params,OPL_inputs):

    """
    dynamical system dynamic occupancy, only bipolar 
    """

    VB,n,VG = X
    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),   
            (1-n) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VB,params['theta_A1']) * n,
            -VG/params['tau_G'] + params['w_B'] * n*p(VB,params['theta_A1'])]


def IPL_occupancy_newconnection(t,X,params,OPL_inputs):

    """
    dynamical system dynamic occupancy, only A1 is rectified and connects to A2 as well 
    """

    VB,VA1,VA2,nA1,VG = X
    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  params['w_A1A2'] * VA1 + OPL_inputs['FA2'](t),
            (1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1,params['theta_A1']) * nA1,
            -VG/params['tau_G'] + params['w_B'] * VB + nA1* params['w_A1'] *  p(VA1,params['theta_A1']) + params['w_A2'] *  VA2]



def IPL_occupancy_A1B(t,X,params,OPL_inputs):

    """
    dynamical system dynamic occupancy, only A1 is rectified and connects to B instead of G
    """

    VB,VA1,VA2,nA1,VG = X
    
    return [-VB/params['tau_B']  + params['w_A1B'] * VA1 + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] + OPL_inputs['FA2'](t),
            (1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1,params['theta_A1']) * nA1,
            -VG/params['tau_G'] + params['w_B'] * VB + nA1* params['w_A1'] *  p(VA1,params['theta_A1'])  + params['w_A2'] *  VA2]




def IPL_rectified_occupancy_nV(t,X,params,OPL_inputs):

    """
    dynamical system with rectified synapses and dynamic occupancy
    """

    VB,VA1,VA2,nA1,VG = X
    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  OPL_inputs['FA2'](t),
            (1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1,params['theta_A1']) * nA1,
            -VG/params['tau_G'] + params['w_B'] * p(VB,params['theta_B']) +  params['w_A1'] *  p(nA1*VA1,params['theta_A1']) + params['w_A2'] *  p(VA2,params['theta_A2'])]

def IPL_rectified(t,X,params,OPL_inputs):

    """
    dynamical system with rectified synapses and fixed  occupancy
    """
    VB,VA1,VA2,VG = X

    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  OPL_inputs['FA2'](t),
            -VG/params['tau_G'] + params['w_B'] * p(VB,params['theta_B']) + params['n_A1_star']* params['w_A1'] *  p(VA1,params['theta_A1']) + params['w_A2'] *  p(VA2,params['theta_A2'])]


def IPL(t,X,params,OPL_inputs):

    """
    dynamical system without rectified synapses and fixed  occupancy
    """
    VB,VA1,VA2,VG = X

    
    return [-VB/params['tau_B'] + OPL_inputs['FB'](t),
            -VA1/params['tau_A1'] +  OPL_inputs['FA1'](t),
            -VA2/params['tau_A2'] +  OPL_inputs['FA2'](t),
            -VG/params['tau_G'] + params['w_B'] * VB + params['n_A1_star']* params['w_A1'] *  p(VA1,params['theta_A1']) + params['w_A2'] *  VA2]




def occupancy(t,nA1,params,VA1):

    """
    dynamical equation for vesicle occupancy
    """
    return [(1-nA1) * params['k_rec'] - params['k_rel'] * params['beta'] * p(VA1(t),params['theta_A1']) * nA1]
