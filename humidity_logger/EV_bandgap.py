'''
This file contains a function to calculate the eV bandgap from a given peak wavelength of a perovskite solar cell
In the future, it will also create and edit a CSV file to contain the eV bandgap information of each sample and 
chemical formula tested using pandas
'''


# Input peak wavelength in nanometers to calculate bandgap using Planck Energy Relation
def calcEV(peak):
    if peak < 300:
        return 0
    return 1240 / peak


#CSV file format

# MAPI, MAPI w/ DAO, MAPI w/ PEG
# 30-40% RH, 30-50% RH, 30-60% RH,

# MAPI
# 30-40% RH: SAMPLE 1 SAMPLE 2 SAMPLE 3 SAMPLE 4 SAMPLE 5
# 30-50% RH: SAMPLE 1 SAMPLE 2 SAMPLE 3 SAMPLE 4 SAMPLE 5
# 30-60% RH: SAMPLE 1 SAMPLE 2 SAMPLE 3 SAMPLE 4 SAMPLE 5

# MAPI w/ DAO
# 30-40% RH: SAMPLE 1 SAMPLE 2 SAMPLE 3 SAMPLE 4 SAMPLE 5
# 30-50% RH: SAMPLE 1 SAMPLE 2 SAMPLE 3 SAMPLE 4 SAMPLE 5
# 30-60% RH: SAMPLE 1 SAMPLE 2 SAMPLE 3 SAMPLE 4 SAMPLE 5

# MAPI w/ PEG
# 30-40% RH: SAMPLE 1 SAMPLE 2 SAMPLE 3 SAMPLE 4 SAMPLE 5
# 30-50% RH: SAMPLE 1 SAMPLE 2 SAMPLE 3 SAMPLE 4 SAMPLE 5
# 30-60% RH: SAMPLE 1 SAMPLE 2 SAMPLE 3 SAMPLE 4 SAMPLE 5








