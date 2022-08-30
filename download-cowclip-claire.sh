#!/bin/bash

# Created on Tue Aug 25 11:55:00 2022

# Script to download a bunch of COWCLIP v2.1 data
# See http://thredds.aodn.org.au/thredds/catalog/CSIRO/Climatology/COWCLIP2/hindcasts/Monthly/Dm/catalog.html
# also https://www.nature.com/articles/s41597-022-01459-3
# All 3 outputs
# http://thredds.aodn.org.au/thredds/catalog/CSIRO/Climatology/COWCLIP2/hindcasts/Monthly/catalog.html

# @author: durack1

# PJD 25 Aug 2022   - started
# PJD 29 Aug 2022   - hacked to get 4 additional/replacement files

# Download generically formatted netcdf files
date=`date +%y%m%d`
workDir=/p/user_pub/climate_work/durack1/Shared/
srcPath=${workDir}220809_murialdo1
# standard DAP URL
dapURL="http://thredds.aodn.org.au/thredds/fileServer/CSIRO/Climatology/COWCLIP2/hindcasts/Monthly"
# monthly file - dir_CSIRO-CAWCR_monthly_1980-2014.nc
fileURLPart=dir_${init}_1980-2014.nc
# complete
# http://thredds.aodn.org.au/thredds/fileServer/CSIRO/Climatology/COWCLIP2/hindcasts/Monthly/Dm/dir_CSIRO-CAWCR_monthly_1980-2014.nc

# change working dir and set output path
cd ${srcPath}
rm -rf ${date}-COWCLIP2p1
mkdir ${date}-COWCLIP2p1
cd ${date}-COWCLIP2p1

# Dm dir
# Hs hs
# Tm tm

# Print for testing
wget --no-check-certificate https://hpc.csiro.au/users/326141/PD_COWCLIP/CAWCR_HIST__CFSR.Hs.mlystat_from_6hly.nc
wget --no-check-certificate https://hpc.csiro.au/users/326141/PD_COWCLIP/CAWCR_HIST__CFSR.Tm.mlystat_from_6hly.nc
wget --no-check-certificate https://hpc.csiro.au/users/326141/PD_COWCLIP/ww3.glob_24m.hs.mlystat_from_hly.nc
wget --no-check-certificate https://hpc.csiro.au/users/326141/PD_COWCLIP/ww3.glob_24m.t0m1.mlystat_from_hly.nc