#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 15:28:00 2022

This script has been written to pull data values from an opendap sourced
global ocean reanalysis suite - COWCLIP v2.1 (1980-2014)

Atmospheric data, see
/p/user_pub/PCMDIobs/obs4MIPs/ECMWF/ERA-5/mon/tas/gn
http://www.bom.gov.au/climate/averages/maps.shtml
http://www.bom.gov.au/research/projects/reanalysis/ - BARRA reanalysis 12km Australia-wide

COW-CLIP v2.1 data
https://catalogue.aodn.org.au/geonetwork/srv/eng/catalog.search#/metadata/068252d5-773b-4bd5-8980-100ad436ed7b
http://thredds.aodn.org.au/thredds/catalog/CSIRO/Climatology/COWCLIP2/hindcasts/Monthly/catalog.html

Wave in-situ data
https://www.transport.wa.gov.au/imarine/download-tide-wave-data.asp

PJD 29 Aug 2022     - updated AGCDv1 data, missing march
PJD 30 Aug 2022     - add hs/tm_p10 wave data 10th percentile as min
TODO                - rerun COWCLIP data - CSIRO inputs

@author: durack1
"""

# %% imports
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cdms2 as cdm
import cdutil as cdu
import datetime
import glob
#import matplotlib.patches as patches
import MV2 as mv
import numpy as np
import os
import pdb
import shutil as shu
import subprocess as subp
import sys
np.set_printoptions(threshold=sys.maxsize)
os.sys.path.insert(0, "/home/durack1/git/durolib/durolib")
from durolib import globalAttWrite

# %% timestamps
timeNow = datetime.datetime.now()
timeFormat = timeNow.strftime("%y%m%dT%H%M%S")

# %% paths
home = "/home/durack1/p-work/Shared"
sub = "220809_murialdo1"
waveData = "220825-COWCLIP2p1"
os.chdir(os.path.join(home, sub, waveData))

# %% function defs


def readGridAscii(filePath, homePath):
    # https://stackoverflow.com/questions/37855316/reading-grd-file-in-python
    with open(filePath) as fh:
        ncols = int(fh.readline().split()[1])
        nrows = int(fh.readline().split()[1])
        xllcorner = float(fh.readline().split()[1])
        yllcorner = float(fh.readline().split()[1])
        cellsize = float(fh.readline().split()[1])
        nodata_value = int(fh.readline().split()[1])
        # version = float(fh.readline().split()[1])  # optional
    lon = xllcorner + cellsize * np.arange(ncols)
    lat = yllcorner + cellsize * np.arange(nrows)
    arr = np.loadtxt(filePath, skiprows=6)
    arr = np.ma.masked_equal(arr, nodata_value)
    arr = np.flipud(arr)
    # Cleanup after file read
    if os.path.exists(os.path.join(homePath, "tmpPath")):
        shu.rmtree(os.path.join(homePath, "tmpPath"))

    return arr, lat, lon


def extract(inFile, homePath):
    # /p-work/Shared/obs_data/EN4/read_EN4_tsclim.py
    os.chdir(homePath)
    if os.path.exists("tmpPath"):
        print(os.path.join(homePath, "tmpPath"))
        shu.rmtree(os.path.join(homePath, "tmpPath"))
    os.makedirs("tmpPath")
    os.chdir("tmpPath")
    shu.copy(inFile, "tmp.zip")
    a7zzPath = "/home/durack1/bin/redhat7/"
    cmd = "".join([a7zzPath, "7zz x tmp.zip"])
    # cmd = "".join([a7zzPath, "7zz e tmp.zip -so > tmp.txt"])
    print("cmd:", cmd)
    os.environ["LD_LIBRARY_PATH"] = "/home/durack1/mambaforge/lib"
    fnull = open(os.devnull, "w")
    subp.call(cmd.split(" "), stdout=fnull)
    fnull.close()
    os.remove("tmp.zip")
    for f in glob.glob("*.prj"):
        os.remove(f)  # solarjan.prj
    newFile = os.listdir()[0]
    print("newFile:", newFile)
    os.rename(newFile, "tmp.asc")
    os.chdir(homePath)


# %% wave data - read and create climatologies
# Loop through institutions
insts = {
    "CSIRO-CAWCR": {
        "dir": {"dir_avg": 323.30010986328125, "dir_std": -99.},  # direction
        # significant wave height
        "hs": {"hs_avg": -99., "hs_max": [-99., 0.002], "hs_p10": -99.},
        # mean wave period
        "tm": {"tm_avg": -99., "tm_max": [-99., 0.01], "tm_p10": -99.},
    },
    "CSIRO-G1D": {
        # direction
        "dir": {"dir_avg": 80.99996948242188, "dir_std": 8.514225919498131e-05},
        # significant wave height
        "hs": {"hs_avg": -99., "hs_max": -99., "hs_p10": -99.},
        # mean wave period
        "tm": {"tm_avg": -99., "tm_max": -99., "tm_p10": -99.},
    },
    "ERA5H":  {
        "dir": {"dir_avg": -99, "dir_std": -99.},  # direction
        # significant wave height
        "hs": {"hs_avg": -99., "hs_max": -99., "hs_p10": -99.},
        # mean wave period
        "tm": {"tm_avg": -99., "tm_max": -99., "tm_p10": -99.},
    },
    "ERA5":  {
        "dir": {"dir_avg": -99, "dir_std": -99.},  # direction
        # significant wave height
        "hs": {"hs_avg": -99., "hs_max": -99., "hs_p10": -99.},
        # mean wave period
        "tm": {"tm_avg": -99., "tm_max": -99., "tm_p10": -99.},
    },
    "ERAI":  {
        "dir": {"dir_avg": -99, "dir_std": -99.},  # direction
        # significant wave height
        "hs": {"hs_avg": -99., "hs_max": -99., "hs_p10": -99.},
        # mean wave period
        "tm": {"tm_avg": -99., "tm_max": -99., "tm_p10": -99.},
    },
    "GOW1":  {
        "dir": {"dir_avg": -99, "dir_std": -99.},  # direction
        # significant wave height
        "hs": {"hs_avg": -99., "hs_max": -99., "hs_p10": -99.},
        # mean wave period
        "tm": {"tm_avg": -99., "tm_max": -99., "tm_p10": -99.},
    },
    "GOW2":  {
        "dir": {"dir_avg": -99, "dir_std": -99.},  # direction
        # significant wave height
        "hs": {"hs_avg": -99., "hs_max": -99., "hs_p10": -99.},
        # mean wave period
        "tm": {"tm_avg": -99., "tm_max": -99., "tm_p10": -99.},
    },
    "IORAS":  {
        "dir": {"dir_avg": -99, "dir_std": 9.969209968386869e+36},  # direction
        # significant wave height
        "hs": {"hs_avg": 9.969209968386869e+36, "hs_max": 9.969209968386869e+36, "hs_p10": -99.},
        # mean wave period
        "tm": {"tm_avg": -99., "tm_max": -99., "tm_p10": -99.},
    },
    "JRC-ERAI":  {
        "dir": {"dir_avg": -99, "dir_std": -99.},  # direction
        # significant wave height
        "hs": {"hs_avg": -99., "hs_max": -99., "hs_p10": -99.},
        # mean wave period
        "tm": {"tm_avg": -99., "tm_max": 9.969209968386869e+36, "tm_p10": -99.},
    },
}

# Loop through
instCount = 0
for count1, inst in enumerate(list(insts)):  # .keys())[0:1]:
    print("inst:", inst)
    if inst in ["CSIRO-G1D", "ERA5H", "ERA5"]:
        print("no hs data, skipping..")
        continue  # doesn't include hs data
    elif inst == "GOW2":
        print("garbled dir info, skipping..")
        continue
    elif inst == "IORAS":
        print("no tm data, skipping..")
        continue
    elif inst in ["JRA55-ST2", "JRA55-ST4"]:
        print("dir, hs data missing, skipping..")
        continue
    elif inst == "JRC-ERAI":
        print("tm_max data missing, skipping..")
        continue
    varCount = 0
    # preallocate array
    instFile = "_".join(["dir", inst, "monthly_1980-2014.nc"])
    print("instFile:", instFile)
    fh = cdm.open(instFile)
    varName = fh.listvariables()[0]
    varTmp = fh[varName]
    print("varTmp.shape:", varTmp.shape)
    latLonLength = varTmp.shape[1:]
    # Preallocate array
    outvar = np.ma.zeros([8, 12, latLonLength[0], latLonLength[1]])
    del(varName, varTmp, latLonLength)
    # Loop through vars and fill array
    for count2, varId in enumerate(insts[inst].keys()):
        print(count2, varId)
        file = "_".join([varId, inst, "monthly_1980-2014.nc"])
        print(file)
        fh = cdm.open(file)
        varNames = list(insts[inst][varId])
        for varName in varNames:
            varTmp = fh(varName)
            # Deal with missing_data and scaling factor
            if isinstance(insts[inst][varId][varName], list):
                landVal = insts[inst][varId][varName][0]
                scaleFactor = insts[inst][varId][varName][1]
            else:
                landVal = insts[inst][varId][varName]
                scaleFactor = 1.
            print(varId, varName, landVal, scaleFactor)
            # reset landmask
            varTmp2 = mv.masked_where(
                mv.equal(varTmp, landVal), varTmp)
            varTmp3 = mv.masked_where(
                mv.less(varTmp2, -99.5), varTmp2)
            # deal with scale factor
            varTmp4 = varTmp3 * scaleFactor
            del(varTmp, varTmp2, varTmp3)
            # set time bounds
            cdu.setTimeBoundsMonthly(varTmp4)
            # generate climatological annual cycle
            acClim = cdu.ANNUALCYCLE.climatology(varTmp4)
            # Check array sizes
            print("acClim.shape:", acClim.shape)
            print("outvar.shape:", outvar.shape)
            print("varCount:", varCount, "varName:", varName)
            outvar[varCount, ] = acClim
            # Validate
            fig1, ax1 = plt.subplots()  # 1,2,1)  # constrained_layout=True)
            plt.title(
                " ".join([inst, varId, varName, "{:5.2f}".format(landVal)]))
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            origin = "lower"
            # cs1 = ax1.contourf(varTmp3.getLongitude().getValue(), varTmp3.getLatitude().getValue(),
            #                   varTmp3[0,], 20, cmap=plt.cm.coolwarm, origin=origin)
            # cs1 = ax1.contourf(varTmp3.getLongitude().getValue(), varTmp3.getLatitude().getValue(),
            #                   acClim[0,], 20, cmap=plt.cm.coolwarm, origin=origin)
            cs1 = ax1.contourf(varTmp4.getLongitude().getValue(), varTmp4.getLatitude().getValue(),
                               outvar[varCount, 0, ], 20, cmap=plt.cm.coolwarm, origin=origin)
            # get index of 50N, 90E
            lat = varTmp4.getLatitude()._data_
            latTest = lat-50
            latInd = np.where(abs(latTest) == abs(latTest).min())
            lon = varTmp4.getLongitude()._data_
            lonTest = lon-90
            lonInd = np.where(abs(lonTest) == abs(lonTest).min())
            print("check value [lat50 300/45.2N, lon100 250/100E")
            print("check value [lat50:", latInd[0][0], lat[latInd][0], ", lon90:",
                  lonInd[0][0], lon[lonInd][0], outvar[varCount, 0, latInd, lonInd][0][0])
            divider = make_axes_locatable(plt.gca())
            cax = divider.append_axes("right", "5%", pad="3%")
            # cax = plt.axes([0.91, 0.11, 0.03, 0.77])
            plt.colorbar(cs1, cax=cax)
            plt.tight_layout()
            plt.show()
            pdb.set_trace()
            fig1.savefig(os.path.join(home, sub, "_".join(
                [timeFormat, inst, varName, "wave-clim", "1980-2014.png"])), dpi=300)
            # pdb.set_trace()
            varCount = varCount+1
    # close file
    fh.close()

    # reassign coordinates to array
    outarr = cdm.createVariable(outvar, id="wave")
    outarr.setAxis(1, acClim.getAxis(0))
    outarr.setAxis(2, acClim.getAxis(1))
    outarr.setAxis(3, acClim.getAxis(2))

    # create outfile and write
    outName = os.path.join(home, sub, "_".join(
        [timeFormat, inst, "wave-clim", "1980-2014.nc"]))
    print("outName:", outName)
    if os.path.isfile(outName):
        os.remove(outName)
    outhandle = cdm.open(outName, 'w')
    # Global attributes - function to write standard global atts
    globalAttWrite(outhandle, options=None)
    # Master variables
    outhandle.write(outarr.astype('float32'))
    outhandle.close()
    # Reset for new inst
    varCount = 0  # reset
    instCount = instCount+1


# %% WOA18 data - extract 12 month data
wod18 = 'obs_data/WOD18/190312'
# change path to local dir
os.chdir(os.path.join(home, sub))
# preallocate monthly arrays
sst, t500 = [np.ones([12, ]) for _ in range(2)]
# open and read
for count, mon in enumerate(np.arange(1, 13)):
    fileName = "".join(["woa18_decav_t", "{:02d}".format(mon), "_04.nc"])
    print("fileName:", fileName)
    filePath = os.path.join(home, wod18, fileName)
    print("filePath:", filePath)
    fh = cdm.open(filePath)
    t = fh('t_an')
    print("t.shape:", t.shape)

    # get index of -22S, 113E
    lat = t.getLatitude()._data_
    latTest = lat+22
    latInd = np.where(abs(latTest) == abs(latTest).min())
    latInd = latInd[0][0]
    lon = t.getLongitude()._data_
    lonTest = lon-113
    lonInd = np.where(abs(lonTest) == abs(lonTest).min())
    lonInd = lonInd[0][0:1][0]
    # get depth == 500 m (36)
    levs = t.getLevel()._data_
    depthInd = np.where(levs == 500)[0][0]
    if count == 0:
        print("depthInd:", depthInd, levs[depthInd], "latInd:",
              latInd, lat[latInd], "lonInd:", lonInd, lon[lonInd])
    # read SST and 500 m values
    # SST, 500mTemp
    sst[count] = t[0, 0, int(latInd), int(lonInd)]
    t500[count] = t[0, int(depthInd), int(latInd), int(lonInd)]
    fh.close()
# cleanup
del(count, depthInd, fileName, filePath, lat, latInd,
    latTest, levs, lon, lonInd, lonTest, mon, timeNow, wod18)

# %% wave data - extract 12 month data
# wave direction - dir_avg, dir_std
# wave height - hs_avg, hs_max, hsP10
# wave period - tm_avg, tm_max, tmP10
dirAvg, dirStd, hsAvg, hsMax, hsP10, tmAvg, tmMax, tmP10 = [
    np.ones([3, 12, ]) for _ in range(8)]

for mon in np.arange(0, 12):
    for count, src in enumerate(["CSIRO-CAWCR", "ERAI", "GOW1"]):
        # build name
        fileName = os.path.join(home, sub, "_".join(
            ["220830T123246", src, "wave-clim_1980-2014.nc"]))
        print(fileName)
        fh = cdm.open(fileName)
        wave = fh("wave")
        # get index of -22S, 113E
        lat = wave.getLatitude()._data_
        latTest = lat+22
        latInd = np.where(abs(latTest) == abs(latTest).min())
        latInd = latInd[0][0]
        lon = wave.getLongitude()._data_
        lonTest = lon-113
        lonInd = np.where(abs(lonTest) == abs(lonTest).min())
        lonInd = lonInd[0][0:1][0]
        # Check values
        print("check values", "\n",
              "mon:", mon, "\n",
              "lat-22 ind:", latInd, lat[latInd],
              "lon113 ind:", lonInd, lon[lonInd], "\n",
              "dir:", wave[0:2, int(mon), int(latInd), int(lonInd)], "\n",
              "Hs:", wave[2:5, int(mon), int(latInd), int(lonInd)], "\n",
              "Tm:", wave[5:8, int(mon), int(latInd), int(lonInd)])
        fh.close()
        print("-----")
        # write to placeholder array
        dirAvg[count, :] = wave[0, :, int(latInd), int(lonInd)]
        dirStd[count, :] = wave[1, :, int(latInd), int(lonInd)]
        hsAvg[count, :] = wave[2, :, int(latInd), int(lonInd)]
        hsMax[count, :] = wave[3, :, int(latInd), int(lonInd)]
        hsP10[count, :] = wave[4, :, int(latInd), int(lonInd)]
        tmAvg[count, :] = wave[5, :, int(latInd), int(lonInd)]
        tmMax[count, :] = wave[6, :, int(latInd), int(lonInd)]
        tmP10[count, :] = wave[7, :, int(latInd), int(lonInd)]
        # Collect monthly values
        print("dir_avg:", ["{:6.2f},".format(i)
              for i in wave[0, :, int(latInd), int(lonInd)].data])
        print("hs_avg:", ["{:6.2f},".format(i)
              for i in wave[2, :, int(latInd), int(lonInd)].data])
        print("tm_avg:", ["{:6.2f},".format(i)
              for i in wave[4, :, int(latInd), int(lonInd)].data])
        print("*-----*")
# cleanup
del(count, fileName, lat, latInd, latTest, lon, lonInd, lonTest, src)

# %% terrestrial data - read and extract 12 month data
agcdv1Data = '220829-AGCD'
# change path to local dir
os.chdir(os.path.join(home, sub))
varMap = {
    "tmean": "mean",
    "tmax": "mxt",
    "tmin": "mnt",
    "rh09": "rh09",
    "rh15": "rh15",
    "sol": "solar",
}
mons = ["jan", "feb", "mar", "apr", "may", "jun",
        "jul", "aug", "sep", "oct", "nov", "dec"]

# preallocate monthly arrays
tmean, tmax, tmin, solar = [np.ones([12, ]) for _ in range(4)]
# open and read
for cnt2, varKey in enumerate(varMap):
    if "rh" in varKey:
        continue  # skip
    for cnt1, mon in enumerate(mons):
        varName = varMap[varKey]
        fileName = "".join([varName, mon, ".zip"])
        print("fileName:", fileName)
        # copy and unzip
        filePath = os.path.join(home, sub, agcdv1Data, fileName)
        print("filePath:", "tmpPath")
        homePath = os.path.join(home, sub)
        print("homePath:", homePath)
        extract(filePath, homePath)
        extFile = os.path.join(home, sub, "tmpPath", "tmp.asc")
        print("extFile:", extFile)
        mat, lat, lon = readGridAscii(extFile, homePath)
        # get index of -22S, 113E
        latTest = lat+22
        latInd = np.where(abs(latTest) == abs(latTest).min())
        latInd = latInd[0][0]
        lonTest = lon-113
        lonInd = np.where(abs(lonTest) == abs(lonTest).min())
        lonInd = lonInd[0][0:1][0]
        if cnt1 == 0:
            print("latInd:", latInd, lat[latInd],
                  "lonInd:", lonInd, lon[lonInd])
        # plot
        '''
        fig1, ax1 = plt.subplots()  #1,2,1)  # constrained_layout=True)
        plt.title('Something')
        plt.xlabel('Longitude ($^\circ$E)')
        plt.ylabel('Latitude ($^\circ$S)')
        origin = "lower"
        #lats = 760:960; lons = 0:240
        # CS = ax1.contourf(Y, Z, t_an.isel(depth=slice(None, None, -1)),  # example to reverse DataArray see
        #                   15, cmap=plt.cm.coolwarm, origin=origin)  # https://stackoverflow.com/questions/54677161/xarray-reverse-an-array-along-one-coordinate
        if varName == "solar":
            cs1 = ax1.contourf(lon[0:100], lat[300:500], mat[300:500,0:100], 20, cmap=plt.cm.coolwarm, origin=origin)
            # Create a Rectangle patch
            rect = patches.Rectangle((113.675, -22.525), 0.6, 0.8, linewidth=1, edgecolor='r', facecolor='none')
            # Add the patch to the Axes
            ax1.add_patch(rect)
        else:
            cs1 = ax1.contourf(lon[0:240], lat[760:960], mat[760:960, 0:240], 20, cmap=plt.cm.coolwarm, origin=origin)
            # Create a Rectangle patch
            rect = patches.Rectangle((113.65, -22.5), 0.6, 0.8, linewidth=1, edgecolor='r', facecolor='none')
            # Add the patch to the Axes
            ax1.add_patch(rect)
        # deal with axes fitting
        divider = make_axes_locatable(plt.gca())
        cax = divider.append_axes("right", "5%", pad="3%")
        # cax = plt.axes([0.91, 0.11, 0.03, 0.77])
        plt.colorbar(cs1, cax=cax)
        plt.tight_layout()
        plt.show()
        #fig1.savefig(os.path.join(home, sub, "_".join(
        #    [timeFormat, inst, varName, "wave-clim", "1980-2014.png"])), dpi=300)
        '''
        # read SST and 500 m values
        # tmean, tmax, tmin, solar
        if varKey == "tmean":
            # -22.5 -> -21.7, 113.65 -> 114.25
            tmean[cnt1] = mat[860:893, 66:91].mean()
        elif varKey == "tmax":
            tmax[cnt1] = mat[860:893, 66:91].mean()
        elif varKey == "tmin":
            tmin[cnt1] = mat[860:893, 66:91].mean()
        elif varKey == "sol":
            # -22.525 -> -21.725, 113.675 -> 114.275
            solar[cnt1] = mat[429:446, 33:46].mean()
# cleanup
del(cnt1, cnt2, extFile, fileName, filePath, homePath, lat, latInd, latTest,
    lon, lonInd, lonTest, mat, mon, mons, varKey, varMap, varName)
#del(ax1, cax, cs1, divider, fig1, origin, rect)

# %% write to txt
os.chdir(os.path.join(home, sub))
# mean
logHandle = open("_".join([timeFormat, "durack1-mean-NWAustData.txt"]), 'w')
logHandle.write("".join(["# Paul J. Durack (durack1) ", timeFormat, "\n"]))
logHandle.write("".join(
    ["Mean value/quantity,     Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec", "\n"]))
logHandle.write("".join(["Ocean wave dir_avg deg,  ", "".join(
    ["{:6.2f},".format(i) for i in dirAvg.mean(axis=0)]), "\n"]))
logHandle.write("".join(["Ocean wave  hs_avg m,    ", "".join(
    ["{:6.2f},".format(i) for i in hsAvg.mean(axis=0)]), "\n"]))
logHandle.write("".join(["Ocean wave  tm_avg s,    ", "".join(
    ["{:6.2f},".format(i) for i in tmAvg.mean(axis=0)]), "\n"]))
logHandle.write("".join(["Ocean surface temp degC, ", "".join(
    ["{:6.2f},".format(i) for i in sst]), "\n"]))
logHandle.write("".join(["Ocean 500m temp degC,    ", "".join(
    ["{:6.2f},".format(i) for i in t500]), "\n"]))
logHandle.write("".join(["Land screen temp degC,   ", "".join(
    ["{:6.2f},".format(i) for i in tmean]), "\n"]))
logHandle.write("".join(["Land solar energy MJ m^2,", "".join(
    ["{:6.2f},".format(i) for i in solar]), "\n"]))
logHandle.close()
# max
logHandle = open("_".join([timeFormat, "durack1-max-NWAustData.txt"]), 'w')
logHandle.write("".join(["# Paul J. Durack (durack1) ", timeFormat, "\n"]))
logHandle.write("".join(
    ["Max  value/quantity,     Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec", "\n"]))
logHandle.write("".join(["Ocean wave dir_avg deg,  ", "\n"]))
logHandle.write("".join(["Ocean wave  hs_max m,    ", "".join(
    ["{:6.2f},".format(i) for i in hsMax.max(axis=0)]), "\n"]))
logHandle.write("".join(["Ocean wave  tm_max s,    ", "".join(
    ["{:6.2f},".format(i) for i in tmMax.max(axis=0)]), "\n"]))
logHandle.write("".join(["Ocean surface temp degC, ", "\n"]))
logHandle.write("".join(["Ocean 500m temp degC,    ", "\n"]))
logHandle.write("".join(["Land screen temp degC,   ", "".join(
    ["{:6.2f},".format(i) for i in tmax]), "\n"]))
logHandle.write("".join(["Land solar energy MJ m^2,", "\n"]))
logHandle.close()
# min
logHandle = open("_".join([timeFormat, "durack1-min-NWAustData.txt"]), 'w')
logHandle.write("".join(["# Paul J. Durack (durack1) ", timeFormat, "\n"]))
logHandle.write("".join(
    ["Min  value/quantity,     Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec", "\n"]))
logHandle.write("".join(["Ocean wave dir_avg deg,  ", "\n"]))
logHandle.write("".join(["Ocean wave  hs_p10 m,    ", "".join(
    ["{:6.2f},".format(i) for i in hsP10.max(axis=0)]), "\n"]))
logHandle.write("".join(["Ocean wave  tm_p10 s,    ", "".join(
    ["{:6.2f},".format(i) for i in tmP10.max(axis=0)]), "\n"]))
logHandle.write("".join(["Ocean surface temp degC, ", "\n"]))
logHandle.write("".join(["Ocean 500m temp degC,    ", "\n"]))
logHandle.write("".join(["Land screen temp degC,   ", "".join(
    ["{:6.2f},".format(i) for i in tmin]), "\n"]))
logHandle.write("".join(["Land solar energy MJ m^2,", "\n"]))
logHandle.close()

# %% regrid to 1x1
# Preload WOA18 grids
# warnings.simplefilter('error')
woa = cdm.open(os.path.join(
    home, "obs_data/WOD18/190312/woa18_decav_s00_01.nc"))
s = woa("s_oa")
print("Start read wod18")
print("type(s):", type(s))
s = s[(0,)]
print("End read wod18")
woaLvls = s.getLevel()
woaGrid = s.getGrid()
# Get WOA target grid
woaLat = s.getLatitude()
woaLon = s.getLongitude()
woa.close()

# %%
"""

Check values
fig1, ax1 = plt.subplots()  #1,2,1)  # constrained_layout=True)
plt.title('Something')
plt.xlabel('Longitude ($^\circ$E)')
plt.ylabel('Latitude ($^\circ$S)')
origin = "lower"
# CS = ax1.contourf(Y, Z, t_an.isel(depth=slice(None, None, -1)),  # example to reverse DataArray see
#                   15, cmap=plt.cm.coolwarm, origin=origin)  # https://stackoverflow.com/questions/54677161/xarray-reverse-an-array-along-one-coordinate
cs1 = ax1.contourf(varTmp.getLongitude().getValue(), varTmp.getLatitude().getValue(),
                    outvar[0,0,], 20, cmap=plt.cm.coolwarm, origin=origin)
plt.show()
"""
