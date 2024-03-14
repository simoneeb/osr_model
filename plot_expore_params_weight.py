from BA1A2_Model import BA1A2_Model
from filter import filter_alpha_norm
from convolutions import convolve_1D
from dynamical_systems import IPL_rectified, IPL_rectified_occupancy, IPL_rectified_occupancy_nV,IPL_occupancy,IPL
from nonlinearities import N
from utils import  make_param_dict, save_dict,save_fig,make_directory
from stimuli import impulse_stimulus, step_stimulus
from load_data import get_euler_stimulus
from simulate import simulate_OSR
from matplotlib.backends import backend_pdf
from matplotlib import pyplot as plt
import os
import numpy as np
import json
import pandas as pd
import seaborn as sns



filepath = "/user/sebert/home/Documents/Simulations/osr_model/explore_weight_params"

df = pd.read_csv(f'{filepath}/DataFrame_weight_params_slope_effect.csv')

df = df.query('slope != 0 and slope <= 2 and slope >= -1')
df_taun_wA1_slope = df.pivot('w_A1','tau_n','slope')


# plot heatmap for beta
df_taun_wA1_num = df.pivot('w_A1','tau_n','n_diff')
df_taun_wA1_slope = df.pivot('w_A1','tau_n','slope')


# print best params
print('params for maximal slope')
print(df.iloc[df['slope'].idxmax()])

tau_n_max = df['tau_n'].iloc[df['slope'].idxmax()]
fig, ax = plt.subplots(1,2)

sns.heatmap(df_taun_wA1_num, ax = ax[0])
sns.heatmap(df_taun_wA1_slope, ax = ax[1])


ax[0].set_title('Difference in n_max from simulations')
ax[1].set_title('Slope')


plt.show()


# plot for different weight when tau chosen to maximize difference in n

# take data fro tau_n = 0.016000 
df_tau_n_opt = df.query(f'tau_n == {tau_n_max}')
df_tau_n_opt = df.query(f'tau_n == 0.006')

fig2, ax = plt.subplots(1,1)

df_tau_n_opt.plot.scatter(x= 'w_A1', y = 'slope', ax = ax)


fig2.suptitle(f'Slope for tau_n set to {0.006}')
plt.show()


# save the plots

save_fig(f'{filepath}/heatmaps_tau_n_w_A1.png',fig)
save_fig(f'{filepath}/w_A1_slope_effect_tau_n_manual.png',fig2)


