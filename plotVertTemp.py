#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 15:49:51 2022

@author: durack1
"""

# %% imports
import numpy as np
import xcdat as xc
#import datetime
import os
import matplotlib.pyplot as plt

# %% data
homeDir = '/p/user_pub/climate_work/durack1'
sharedObsDir = 'Shared/obs_data'
wod18 = 'WOD18/190312'
tan = 'woa18_decav_t00_04.nc'

# %% change path to local dir
os.chdir(os.path.join(homeDir, 'Shared/220809_murialdo1'))

# %% preprocess kludge
'''
time = "1986-06-15"  #4326
newTime = datetime.datetime(1986, 6, 15)

def fixTime(var):
    return
'''

# %% open and read
wH = xc.open_dataset(os.path.join(homeDir, sharedObsDir,
                     wod18, tan), decode_times=False, add_bounds=False)

# xarray preprocess notes https://github.com/pydata/xarray/issues/2313
# https://github.com/xCDAT/xcdat/issues/304 - test example below
wH = xc.open_dataset(os.path.join(homeDir, sharedObsDir,
                     wod18, tan))

# %% pull out longitude line
lonX = 112.875  # 113.125  #112.875  # 113 E
latY = np.array([-35.125, -15.125])
t_an = wH.t_an.sel(lat=slice(-35.125, -15.125), lon=lonX, depth=slice(0, 1000))
t_an.isel(depth=slice(None, None, -1))
Y = abs(wH.lat.values[219:300])  # wash sign
#X = wH.lon.values[1171]
Z = wH.depth.values[0:47]  # 0 -> 1000 m
# t_an.shape
#Out[35]: (1, 102, 80)
t_an = t_an.squeeze(axis=0)
# t_an.shape
#Out[39]: (102, 81)

# %% now plot
fig1, ax1 = plt.subplots()  # constrained_layout=True)
plt.title('North->South Indian Ocean temperature cross-section (113E, $^\circ$C)')
plt.xlabel('Latitude ($^\circ$S)')
plt.ylabel('Depth (m)')
origin = "lower"
# CS = ax1.contourf(Y, Z, t_an.isel(depth=slice(None, None, -1)),  # example to reverse DataArray see
#                   15, cmap=plt.cm.coolwarm, origin=origin)  # https://stackoverflow.com/questions/54677161/xarray-reverse-an-array-along-one-coordinate
CS = ax1.contourf(Y, Z, t_an,
                  20, cmap=plt.cm.coolwarm, origin=origin)
ax1.invert_yaxis()  # flip so 0 at top
# ax1.invert_xaxis()  # flip so north is left - not required with Y = abs() above
#ax1.set_position([[0.08, 0.07], [0.90, 0.97]])
cax = plt.axes([0.92, 0.125, 0.035, 0.755])
plt.colorbar(CS, cax=cax)
ax1.text(16, 700, "NOAA World Ocean Atlas 2018\nannual mean ocean temperature", fontsize=7)
plt.show()
fig1.savefig('220809_durack1_WOD18-t_an-IndianOcean-113E-0to1000m.png', dpi=300)
