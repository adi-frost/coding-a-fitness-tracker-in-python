#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 20:22:53 2025

@author: aditya
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display
pd.set_option('display.max_columns', None)

# ---------------------------------------------------------------------------
# Load Data
# ---------------------------------------------------------------------------

df = pd.read_pickle("../../data/interim/01_data_processed.pkl")


# ---------------------------------------------------------------------------
# Plot Single column
# ---------------------------------------------------------------------------

set_df = df[df["set"] == 1]

plt.plot(set_df["acc_y"].reset_index(drop=True))


# ---------------------------------------------------------------------------
# Plot all exercises
# ---------------------------------------------------------------------------

for label in df["label"].unique():
    subset = df[df["label"] == label]
    # display(subset.head(2))
    fig, ax  = plt.subplots()
    plt.plot(subset[:100]["acc_y"].reset_index(drop=True), label=label)
    plt.legend()
    plt.show()
    

# -------------------------------------------------------------------------
# Adjust Plot Settings
# -------------------------------------------------------------------------

mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"] = (20, 5)
mpl.rcParams["figure.dpi"] = 100


# ------------------------------------------------------------------------
# Compare Medium vs Heavy Sets
# ------------------------------------------------------------------------

category_df = df.query("label == 'squat'").query("participant == 'A'").reset_index()

fig, ax = plt.subplots()
category_df.groupby(["category"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()
plt.show()


# -------------------------------------------------------------------------
# Compare participants
# -------------------------------------------------------------------------

participant_df = df.query("label =='bench'").sort_values("participant").reset_index()

fig, ax = plt.subplots()
participant_df.groupby(["participant"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()
plt.show()


# -------------------------------------------------------------------------
# Plot multiple axis
# -------------------------------------------------------------------------

label = "squat"
participant = "A"
all_axis_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()

fig, ax = plt.subplots()
all_axis_df[["acc_y", "acc_x", "acc_z"]].plot(ax=ax)
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()
plt.show()


# ------------------------------------------------------------------------
# Create a loop to plot all combination per sensor
# ------------------------------------------------------------------------

labels = sorted(df["label"].unique())
participants = sorted(df["participant"].unique())

# For accelerometer data
for label in labels:
    for participant in participants:
        all_axis_df = df.query(f"label == '{label}'") \
            .query(f"participant == '{participant}'") \
            .reset_index()
        
        if len(all_axis_df) > 0:
            fig, ax = plt.subplots()
            all_axis_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax)
            ax.set_ylabel("acc_y")
            ax.set_xlabel("samples")
            plt.legend()
            plt.title(f"{label} ({participant})".title())
            plt.show()


# For gyroscope data
for label in labels:
    for participant in participants:
        all_axis_df = df.query(f"label == '{label}'") \
            .query(f"participant == '{participant}'") \
            .reset_index()
        
        if len(all_axis_df) > 0:
            fig, ax = plt.subplots()
            all_axis_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax)
            ax.set_ylabel("gyr_y")
            ax.set_xlabel("samples")
            plt.legend()
            plt.title(f"{label} ({participant})".title())
            plt.show()


# -----------------------------------------------------------------------
# Combine plots in one figure
# -----------------------------------------------------------------------

label = "row"
participant = "A"
combined_plot_df = df.query(f"label == '{label}'") \
                        .query(f"participant == '{participant}'") \
                        .reset_index(drop=True)

fig, ax = plt.subplots(nrows = 2, sharex = True, figsize=(20, 10))
combined_plot_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
combined_plot_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True)
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True)
ax[1].set_xlabel("samples")
plt.show()


# -----------------------------------------------------------------------
# Loop over all combinations and export for both sensors
# -----------------------------------------------------------------------

labels = sorted(df["label"].unique())
participants = sorted(df["participant"].unique())

# For accelerometer data
for label in labels:
    for participant in participants:
        combined_plot_df = df.query(f"label == '{label}'") \
            .query(f"participant == '{participant}'") \
            .reset_index()
        
        if len(combined_plot_df) > 0:
            fig, ax = plt.subplots(nrows = 2, sharex = True, figsize=(20, 10))
            combined_plot_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
            combined_plot_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

            ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True)
            ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True)
            ax[1].set_xlabel("samples")
            plt.savefig(f"../../reports/figures/{label.title()} ({participant}).png")
            plt.show()            








