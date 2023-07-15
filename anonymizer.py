import numpy as np
import pandas as pd

import config


def choose_dimension(data):
    return max(config.qi, key=lambda column: data[column].max() - data[column].min())


def generalization(data):
    for column in config.qi:
        col_min = data[column].min()
        col_max = data[column].max()

        if column in config.userDefinedCat:
            # decode quantized columns based on user-defined generalization hierarchies for categorical attributes
            value = config.userDefinedCat[column][str(col_min) + "-" + str(col_max)] \
                if col_min != col_max else config.userDefinedCat[column][str(col_min)]
        else:
            value = str(col_min) + "-" + str(col_max) if col_min != col_max else str(col_min)

        data.loc[:, column] = value

    return data


def mondrian(data, k, mode=config.mode):
    # termination condition
    if len(data) < 2 * k:
        return generalization(data)

    # choose dimension (return the highest range of unique values)
    dim = choose_dimension(data)

    # get the set of the dimension chosen
    fs = data[dim]
    # find the median to split the partition based on that
    split_val = np.median(fs)

    # split the data based on median
    # changes based on mode
    if mode == 'strict':
        lhs = data[data[dim] <= split_val]
        rhs = data[data[dim] > split_val]
        # if rhs is empty, we will hit infinite recursion
        # if rhs is less than k, we fail the k-anonymity
        if len(rhs) < k:
            return generalization(data)
    elif mode == 'relaxed':
        # rows where t.dim = splitVal are divided such that:
        # |lhs child| = |rhs child| (+1 when |partition| is odd)
        lhs = data[data[dim] < split_val]
        rhs = data[data[dim] > split_val]
        median_rows = data[data[dim] == split_val]
        midIdx = (len(median_rows) // 2)
        lhs = pd.concat([lhs, median_rows[:midIdx]], ignore_index=True)
        rhs = pd.concat([rhs, median_rows[midIdx:]], ignore_index=True)

    else:
        print('the available modes are: \'strict\' and \'relaxed\'')
        exit()

    return pd.concat([mondrian(lhs, k, mode), mondrian(rhs, k, mode)], ignore_index=True)
