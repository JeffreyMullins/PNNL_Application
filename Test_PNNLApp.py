from unittest import TestCase
from PnnlApp import *

class testPnnlApp(TestCase):

    def test_changes_metadata(self):
        set1 = Dataset("sgpmetE13.b1.20180103.000000.cdf", "r", format="NETCDF4")
        setCopy = Dataset("sgpmetavgE13.b1.20180103.000000.cdf", "w", format="NETCDF4")
        time = setCopy.createDimension("time", size=None)
        avgpres = setCopy.createVariable("atmospheric_pressure", "f4", dimensions=("time",), fill_value=False)
        
        copy_Variable_Metadata(set1, "atmos_pressure", avgpres)

        # test if all metadata in the copy file is correct
        self.assertEqual("Atmospheric pressure", setCopy.variables["atmospheric_pressure"].long_name)
        self.assertEqual("kPa", setCopy.variables["atmospheric_pressure"].units)
        self.assertEqual(80.0, setCopy.variables["atmospheric_pressure"].valid_min)
        self.assertEqual(110.0, setCopy.variables["atmospheric_pressure"].valid_max)
        self.assertEqual(1.0, setCopy.variables["atmospheric_pressure"].valid_delta)
        self.assertEqual(-9999.0, setCopy.variables["atmospheric_pressure"].missing_value)

        setCopy.close()
        set1.close()

    def test_Average_Variable_Data(self):
        set1 = Dataset("sgpmetE13.b1.20180103.000000.cdf", "r", format="NETCDF4")
        setCopy = Dataset("sgpmetavgE13.b1.20180103.000000.cdf", "w", format="NETCDF4")
        time = setCopy.createDimension("time", size=None)
        avgpres = setCopy.createVariable("atmospheric_pressure", "f4", dimensions=("time",), fill_value=False)
        
        average_Varable_data(set1, "atmos_pressure", avgpres, 5)

        second_average_result = 0
        for i in range(5):
            second_average_result += set1.variables["atmos_pressure"][i+5]

        second_average_result /= 5


        self.assertEqual((288,), setCopy.variables["atmospheric_pressure"].shape)
        # test if the second calculated average is within the first decimal of the variable's calculation
        # (rounding from CDF files makes doing an assertAlmostEqual needed)
        self.assertAlmostEqual(second_average_result, setCopy.variables["atmospheric_pressure"][1], 1)

        setCopy.close()
        set1.close()