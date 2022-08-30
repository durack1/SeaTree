#!/bin/bash

# Created on Tue Aug 25 11:55:00 2022

# Script to download a bunch of COWCLIP v2.1 data
# See http://thredds.aodn.org.au/thredds/catalog/CSIRO/Climatology/COWCLIP2/hindcasts/Monthly/Dm/catalog.html
# also https://www.nature.com/articles/s41597-022-01459-3
# All 3 outputs
# http://thredds.aodn.org.au/thredds/catalog/CSIRO/Climatology/COWCLIP2/hindcasts/Monthly/catalog.html

# @author: durack1

# PJD 25 Aug 2022   - started
# PJD 29 Aug 2022   - fix nar -> mar

# Download generically formatted netcdf files
date=`date +%y%m%d`
workDir=/p/user_pub/climate_work/durack1/Shared/
srcPath=${workDir}220809_murialdo1
# standard URL
URL="http://www.bom.gov.au/web01/ncc/www/climatology"
# example files
: <<"BLANK"
http://www.bom.gov.au/web01/ncc/www/climatology/solar_radiation/solarfeb.zip
http://www.bom.gov.au/web01/ncc/www/climatology/relative-humidity/rh09/rh09jan.zip
http://www.bom.gov.au/web01/ncc/www/climatology/relative-humidity/rh15/rh15jan.zip
http://www.bom.gov.au/web01/ncc/www/climatology/temperature/mean/meanjan.zip
http://www.bom.gov.au/web01/ncc/www/climatology/temperature/mnt/mntjan.zip
http://www.bom.gov.au/web01/ncc/www/climatology/temperature/mxt/mxtjan.zip
BLANK

# change working dir and set output path
src="AGCD"
cd ${srcPath}
rm -rf ${date}-${src}
mkdir ${date}-${src}
cd ${date}-${src}

# Print for testing
for mon in {jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec}; do
    for var in {solar,rh09,rh15,mean,mnt,mxt}; do
        if [ $var == "solar" ]; then
            dirvar="solar_radiation"
        elif [ $var == "rh09" ]; then
            dirvar="relative-humidity/rh09"
        elif [ $var == "rh15" ]; then
            dirvar="relative-humidity/rh15"
        elif [ $var == "mean" ]; then
            dirvar="temperature/mean"
        elif [ $var == "mnt" ]; then
            dirvar="temperature/mnt"
        elif [ $var == "mxt" ]; then
            dirvar="temperature/mxt"
        fi
        filePart="${var}${mon}.zip"
        dapVarUrl="${URL}/${dirvar}/"
        url="${dapVarUrl}${filePart}"
        echo $url
        wget --no-check-certificate -U "Mozilla/5.0 (X11; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0" $url
        #--referer="http://www.bom.gov.au/jsp/ncc/climate_averages/relative-humidity/index.jsp"\
    done
done
