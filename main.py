import os.path
import time

import numpy as np
import pandas as pd

import config
from utility import plot
from utility import quantize_categorical_columns
from utility import calc_C_AVG
from anonymizer import mondrian


if __name__ == '__main__':
    # performance data
    duration = {}
    C_AVG = {}

    # read the data and drop EIs
    tblData = pd.read_csv(config.inputBaseUrl + config.inputFile).drop(columns=config.ei).copy(deep=True)

    # Make sure non-numeric columns are of type string
    non_numeric_columns = tblData.select_dtypes(exclude=np.number).columns
    tblData[non_numeric_columns] = tblData[non_numeric_columns].astype(str)

    # quantize the categorical columns
    transformedData = quantize_categorical_columns(tblData)

    # create output folder if not exist
    if not os.path.exists(config.outputBaseUrl):
        os.mkdir(config.outputBaseUrl)

    print("\n\n\n********************************")
    print("                START           ")
    print("********************************\n")
    for k in config.k_list:
        print(f"start anonymization with k='{k}' - {config.mode} mode")
        start = time.time()
        # anonymize the data
        anonymizedData = mondrian(transformedData, k, config.mode)
        end = time.time()
        duration[k] = end - start
        print(f"anonymization finished in '{duration[k]}' seconds")

        # write the anonymized data
        anonymizedData.to_csv(f"{config.outputBaseUrl}{config.inputFile}_{config.mode}_K{k}_output.csv", index=False)

        if config.debug:
            print(anonymizedData)

        # check quality
        C_AVG[k] = calc_C_AVG(anonymizedData, k)
        print(f"The C_avg quality metric of this anonymization is: '{C_AVG[k]}'")
        print("\nThe anonymized data is saved successfully in the output folder.")
        print(f"anonymization with k='{k}' - {config.mode} mode has finished!")
        print("\n********************************\n")

    print("\n\n\n********************************")
    print("                FINISHED!           ")
    print("********************************\n\n\n")

    plot(duration, C_AVG, config.mode)
