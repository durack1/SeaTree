#!/bin/bash

# Created on Tue Aug 23 14:37:00 2022

# Script to download a bunch of AustBOM ACCESS-S1 data
# See https://dapds00.nci.org.au/thredds/catalog/ub7/access-s1/hc/calibrated_5km_v3/atmos/catalog.html
# Some descriptive info
# http://poama.bom.gov.au/general/dataserver/calibrated.html
# Gridded obs datasets
# http://www.bom.gov.au/climate/averages/climatology/gridded-data-info/gridded_datasets_summary.shtml
# AGCD v2
# https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f6087_5319_9836_7368 - only pr opendap
# http://www.bom.gov.au/metadata/catalogue/19115/ANZCW0503900567
# AGCD v1 / AWAP
# https://dapds00.nci.org.au/thredds/catalog/zv2/agcd/v1/catalog.html - 5 vars

# @author: durack1

# PJD 23 Aug 2022   - started
# PJD 23 Aug 2022   - switched from clim_1990-2012 to emn (ensemble mean)
# PJD 23 Aug 2022   - drop to single e1 ensemble member

# Download generically formatted netcdf files
date=`date +%y%m%d`
workDir=/p/user_pub/climate_work/durack1/Shared/
srcPath=${workDir}220809_murialdo
# standard DAP URL
DapURL="https://dapds00.nci.org.au/thredds/fileServer/ub7/access-s1/hc/calibrated_5km_v3/atmos/"
# climatology path - ?
fileURLPart="${var}/monthly/clim_1990-2012/maq5_${var}_clim${mon}${init}.nc"
# emn path - m3aq5_rsds_19900101_emn.nc
fileURLPart=${var}/monthly/emn/m3aq5_${var}_${year}${mon}${init}_emn.nc

# change working dir and set output path
cd ${srcPath}
rm -rf ${date}
mkdir ${date}
cd ${date}

# Print for testing
for var in {evap,pr,rsds,tasmax,tasmin,vprp_09,vprp_15,wind_speed}; do
    for yr in {1990..2012}; do
        for mon in {01..12}; do
            #for init in {01,09,17,25}; do
                filePart="${var}/monthly/emn/m3aq5_${var}_${yr}${mon}01_emn.nc"
                url=${DapURL}${filePart}
                echo $url
                wget --no-check-certificate $url
            #done
        done
    done
done
