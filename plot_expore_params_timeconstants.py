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



filepath = "/user/sebert/home/Documents/Simulations/osr_model/explore_timeconstants_params"

df = pd.read_csv(f'{filepath}/DataFrame_timeconstants_params_slope_effect.csv')

# plot heatmap  time constants
# fix a walue for  weight ratio

df_wfix = df.loc[df['w_ratio'] == 1]

# constrain slope 
df_hms = df_wfix.query(' slope <= 1 and slope >= -0.5')
#df_hms = df_wfix
mi = df_hms['slope'].min()
print(df_hms.query(f'slope == {mi}'))


df_tau_B_tau_A2_slope = df_hms.pivot('tau_B','tau_A2','slope')
df_tau_B_tau_A2_delay = df_hms.pivot('tau_B','tau_A2','delay_16Hz')


# print best params
print('params for maximal slope')
print(df.iloc[df['slope'].idxmax()])

print('params for minimal slope')
print(df.iloc[df['slope'].idxmin()])



fig, ax = plt.subplots(1,2)

sns.heatmap(df_tau_B_tau_A2_slope, ax = ax[0])
sns.heatmap(df_tau_B_tau_A2_delay, ax = ax[1])


ax[0].set_title('Slope')
ax[1].set_title(' Peak Latency for 16 Hz')


fig.suptitle('Weights ratio fixed to 1')
plt.show()




#plot heatmap for weighs ratio



# save the plots
df_tbfix = df.loc[df['tau_B'] == 0.01]
# df_tbfix = df_tbfix.query('slope <= 1 and slope >= -1')
df_tbfix = df_tbfix

df_wr_tau_A2_slope = df_tbfix.pivot('w_ratio','tau_A2','slope')
df_wr_tau_A2_delay = df_tbfix.pivot('w_ratio','tau_A2','delay_16Hz')


fig2, ax = plt.subplots(1,2)

sns.heatmap(df_wr_tau_A2_slope, ax = ax[0])
sns.heatmap(df_wr_tau_A2_delay, ax = ax[1])


ax[0].set_title('Slope')
ax[1].set_title(' Peak Latency for 16 Hz')


fig2.suptitle('tau_b fixed to 0.01')


plt.show()

save_fig(f'{filepath}/heatmaps_tau_B_tau_A2.png',fig)
save_fig(f'{filepath}/heatmaps_w_ratio_tau_A2.png',fig2)


