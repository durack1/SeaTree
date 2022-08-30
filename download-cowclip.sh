#!/bin/bash

# Created on Tue Aug 25 11:55:00 2022

# Script to download a bunch of COWCLIP v2.1 data
# See http://thredds.aodn.org.au/thredds/catalog/CSIRO/Climatology/COWCLIP2/hindcasts/Monthly/Dm/catalog.html
# also https://www.nature.com/articles/s41597-022-01459-3
# All 3 outputs
# http://thredds.aodn.org.au/thredds/catalog/CSIRO/Climatology/COWCLIP2/hindcasts/Monthly/catalog.html

# @author: durack1

# PJD 25 Aug 2022   - started

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
for inst in {CSIRO-CAWCR,CSIRO-G1D,ERA5H,ERA5,ERAI,GOW1,GOW2,IORAS,JRA55-ST2,JRA55-ST4,JRC-CFDR,JRC-ERAI}; do
    for var in {Dm,Hs,Tm}; do
        if [ $var == "Dm" ]; then
            filevar="dir"  # direction
        elif [ $var == "Hs" ]; then
            filevar="hs"  # significant wave height
        elif [ $var == "Tm" ]; then
            filevar="tm"  # mean wave period
        fi
        filePart="${filevar}_${inst}_monthly_1980-2014.nc"
        dapVarUrl="${dapURL}/${var}/"
        url="${dapVarUrl}${filePart}"
        echo $url
        wget --no-check-certificate $url
    done
done
