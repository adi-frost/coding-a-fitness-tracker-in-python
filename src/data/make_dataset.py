#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 23:11:22 2025
@author: aditya
"""

import pandas as pd
pd.set_option('display.max_columns', None)
from glob import glob

#---------------------------------------------------------------------------
# Read single CSV file
#---------------------------------------------------------------------------

single_file_acc = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv")

single_file_gyr = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv")


# -------------------------------------------------------------------------
# List all data in data/raw/MetaMotion
# -------------------------------------------------------------------------

files = glob("../../data/raw/MetaMotion/*.csv")

len(files)


# -------------------------------------------------------------------------
# Extract features from filename
# -------------------------------------------------------------------------

data_path = "../../data/raw/MetaMotion/"

f = files[0]

participant = f.split("-")[0].replace(data_path, '')
label = f.split("-")[1]
category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

df = pd.read_csv(f)

df["participant"] = participant
df["label"] = label
df["category"] = category


# -----------------------------------------------------------------------
# Read all files
# -----------------------------------------------------------------------

acc_df = pd.DataFrame()
gyr_df = pd.DataFrame()

acc_set = 1
gyr_set = 1

for f in files:
    participant = f.split("-")[0].replace(data_path, '')
    label = f.split("-")[1]
    category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

    df = pd.read_csv(f)
    
    df["participant"] = participant
    df["label"] = label
    df["category"] = category
    
    if "Accelerometer" in f:
        df["set"] = acc_set
        acc_set += 1
        acc_df = pd.concat([acc_df, df], axis=0)
    
    if "Gyroscope" in f:
        df["set"] = gyr_set
        gyr_set += 1
        gyr_df = pd.concat([gyr_df, df], axis=0)


# acc_df[acc_df["set"] == 10]


# ------------------------------------------------------------------------
# Working with datetimes
# ------------------------------------------------------------------------

acc_df.info()

# pd.to_datetime(acc_df["epoch (ms)"], unit="ms")

# pd.to_datetime(acc_df["time (01:00)"], format='mixed').dt.year

acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

del acc_df["epoch (ms)"]
del acc_df["time (01:00)"]
del acc_df["elapsed (s)"]

del gyr_df["epoch (ms)"]
del gyr_df["time (01:00)"]
del gyr_df["elapsed (s)"]


# ----------------------------------------------------------------------
# Turn into function
# ----------------------------------------------------------------------

files = glob("../../data/raw/MetaMotion/*.csv")

def read_data_from_files(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    data_path = "../../data/raw/MetaMotion/"

    for f in files:
        participant = f.split("-")[0].replace(data_path, '')
        label = f.split("-")[1]
        category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

        df = pd.read_csv(f)
        
        df["participant"] = participant
        df["label"] = label
        df["category"] = category
        
        if "Accelerometer" in f:
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df], axis=0)
        
        if "Gyroscope" in f:
            df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df, df], axis=0)
            
    
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]

    del gyr_df["epoch (ms)"]
    del gyr_df["time (01:00)"]
    del gyr_df["elapsed (s)"]
    
    return acc_df, gyr_df


acc_df, gyr_df = read_data_from_files(files)


# -----------------------------------------------------------------------
# Merging Datasets
# -----------------------------------------------------------------------

data_merged = pd.concat([acc_df.iloc[:,:3], gyr_df], axis=1)


# Rename columns
data_merged.columns = [
        "acc_x",
        "acc_y",
        "acc_z",
        "gyr_x",
        "gyr_y",
        "gyr_z",
        "participant",
        "label",
        "category",
        "set"
    ]


# -----------------------------------------------------------------------
# Resample Data (Frequency Conversion)
# -----------------------------------------------------------------------

# Accelerometer: 12.5 Hz
# Gyroscope: 25 Hz

# data_merged[:100].resample(rule="S").mean(numeric_only=True)
# data_merged[:100].resample(rule="200ms").mean(numeric_only=True)

sampling = {
        "acc_x": "mean", 
        "acc_y": "mean", 
        "acc_z": "mean", 
        "gyr_x": "mean", 
        "gyr_y": "mean", 
        "gyr_z": "mean",
        "participant": "last",
        "category": "last", 
        "label": "last", 
        "set": "last"
    }

# data_merged[:1000].resample(rule="200ms").apply(sampling)

# Split by day
days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]

data_resampled = pd.concat([df.resample(rule="200ms")\
                            .apply(sampling).dropna() \
                                for df in days])

data_resampled.info()

data_resampled["set"] = data_resampled["set"].astype("int")


# -----------------------------------------------------------------------
# Export Dataset
# -----------------------------------------------------------------------

data_resampled.to_pickle("../../data/interim/01_data_processed.pkl")








