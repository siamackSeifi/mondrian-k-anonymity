# Mondrian k-anonymity
Mondrian is a multidimensional k-anonymity model which benefits from a Top-down greedy data anonymization algorithm. 
It uses a median-partitioning technique to split the attributes' dimensions recursively and anonymize data.
This repository contains the code for a Mondrian k-anonymity algorithm based on the paper proposed by Kristen LeFevre. 
The algorithm is implemented in Python and can be run from the command line.
This repository contains the code for a Mondrian k-anonymity algorithm. 
The algorithm is implemented in Python and can be run from the command line.

## Usage
To run the algorithm, you will need to have Python 3 installed. Once you have Python installed, 
you can run the algorithm by executing the following command:

`python main.py`

This will run the algorithm based on the parameters specified in config.py file.\
The output of the algorithm will be saved in the ``output`` directory.

### Parameters
The algorithm can be configured using the config.py file. The following parameters can be configured:

* ``debug:`` Set this to ``True`` to print debugging information.
* ``inputBaseUrl``: The base URL of the input dataset.
* ``inputFile``: The name of the input dataset.
* ``ei``: The list of EIs (Explicit-identifiers).
* ``qi``: The list of QIs (Quasi-identifiers).
* ``k_list``: The list of k values to use.
* ``mode``: The mode of the algorithm (either strict or relaxed).
* ``outputBaseUrl``: The base URL of the output directory.
* ``userDefinedCatAvailable``: Set this to True if you have provided user-defined generalization hierarchies for the categorical attributes.
* ``userDefinedCat``: A dictionary that maps categorical attributes to their user-defined generalization hierarchies.\
It is used for quantizing categorical fields and generalizing them in the end.\
  (In order to preserve the semantics of the categorical data after quantizing them)

## Output
The output of the algorithm will be saved in the output directory. The output will consist of 
a set of anonymized datasets, one for each value of k. Each anonymized dataset will be a CSV file.\
Also, there will be a set of charts to visualize the performance statistics.
