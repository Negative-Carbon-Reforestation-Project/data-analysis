import numpy as np
import rpy2
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from rpy2.robjects import r

# Using rpy2 instead of pyreadr here as the dataset contains latin1 characters that break pyreadr
readRDS = r['readRDS']

soil_frame_rpy = readRDS('data/soil/sol_chem.pnts_horizons.rds')

type(soil_frame_rpy)

new_df = pd.DataFrame()
for col in soil_frame_rpy:
    new_df[col] = ''
    for row in soil_frame_rpy[col]:
        try:
            new_df[col].append(row)
        except:
            print('hi')
