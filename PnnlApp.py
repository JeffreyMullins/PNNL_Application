from netCDF4 import *
import numpy as np

def copy_Variable_Metadata(firstFile, varName, copyVariable):
    """
    Copies the metadata from the variable of one file to the variable of another
    This function only works for specific variables with the following for metadata:
        long_name, units, valid_min, valid_max, valid_delta, missing_value
    :param firstFile: The name of the first CDF file that will have a variable's metadata copied.
    :param varName:  The name of the variable in the first file that will have its metadata copied.
    :param copyVariable: The variable that will have the metadata copied into it.
    :return: None
    """
    copyVariable.long_name = firstFile.variables[varName].long_name
    copyVariable.units = firstFile.variables[varName].units
    copyVariable.valid_min = firstFile.variables[varName].valid_min
    copyVariable.valid_max = firstFile.variables[varName].valid_max
    copyVariable.valid_delta = firstFile.variables[varName].valid_delta
    copyVariable.missing_value = firstFile.variables[varName].missing_value

def average_Varable_data(firstFile, copyVarName, aveVariable, numAverage):
    """
    Copies the averaged data from one variaable into another.
    :param firstFile: The name of the first CDF file that will have its variable averaged and copied.
    :param copyVarName: Name of the variable that is getting averaged and copied.
    :param aveVariable: The variable that the averaged data is being copied into
    :param numAverage: The number of data pointed being averaged into one
    :return: None
    """
    avg = 0
    for i in range(firstFile.variables[copyVarName].size):
        avg += firstFile.variables[copyVarName][i]
        if i % numAverage == 0:
            aveVariable[int(i / numAverage)] = avg / numAverage
            avg = 0

def make_Average_Copy(setName, copyName):
    """
    Takes the names of two CDF files, averages the data in the "temp_mean" and "atmos_pressure" variables,
    and copies those averages (as well as the metadata from those variables) into variables in the other specified file
    :param setName: The name of the CDF file that is going to be averaged and copied
    :param copyName: The name of the CDF file that will have the copied data put in it
    :return: None
    """
    set1 = Dataset(setName, "r", format="NETCDF4")
    setCopy = Dataset(copyName, "w", format="NETCDF4")

    time = setCopy.createDimension("time", size=None)
    avgpres = setCopy.createVariable("atmospheric_pressure", "f4", dimensions=("time",), fill_value=False)
    avgtemp = setCopy.createVariable("mean_temperature", "f4", dimensions=("time",), fill_value=False)

    copy_Variable_Metadata(set1, "atmos_pressure", avgpres)
    average_Varable_data(set1, "atmos_pressure", avgpres, 5)

    copy_Variable_Metadata(set1, "temp_mean", avgtemp)
    average_Varable_data(set1, "temp_mean", avgtemp, 5)

    print(set1.variables["atmos_pressure"])
    print(set1.variables["temp_mean"])
    print(setCopy.variables["atmospheric_pressure"])
    print(setCopy.variables["mean_temperature"])

    set1.close()
    setCopy.close()


if __name__ == '__main__':
    f = 1
    setName = "sgpmetE13.b1.2018010" + str(f) + ".000000.cdf"
    copyName = "sgpmetavgE13.b1.2018010" + str(f) + ".000000.cdf"

    make_Average_Copy(setName, copyName)

