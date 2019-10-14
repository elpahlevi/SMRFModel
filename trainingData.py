import arcpy
import os, math
from arcpy import env as ENV
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

class trainingData():
    workDIR = r"D:/arcpy"
    ENV.overwriteOutput = True
    outDIR = r"D:/arcpy/results"
    clipped_image = "/clippedImage"

    def evi(self):
        ENV.workspace = self.outDIR+self.clipped_image
        evi_band_list = ["*B2*", "*B4*", "*B5*"]
        evi_list = []
        for evi_calc in evi_band_list:
            raster_src = arcpy.ListRasters(evi_calc, "TIF")
            evi_list.extend(raster_src)
        blue = arcpy.sa.Raster(evi_list[0])
        red = arcpy.sa.Raster(evi_list[1])
        nir = arcpy.sa.Raster(evi_list[2])
        evi_output = "D:/arcpy/results/trainingData/evi/EVI_kulonporogo.TIF"
        evi_calculate = 2.5 * Float(nir-red)/Float(nir + (6.0*red)-(7.5*blue)+1)
        evi_calculate.save(evi_output)
        print("Selesai Menghitung EVI")

    def savi(self):
        ENV.workspace = self.outDIR+self.clipped_image
        savi_band_list = ["*B4*", "*B5*"]
        constant = 0.5
        savi_list = []
        for savi_calc in savi_band_list:
            raster_src = arcpy.ListRasters(savi_calc, "TIF")
            savi_list.extend(raster_src)
        red = arcpy.sa.Raster(savi_list[0])
        nir = arcpy.sa.Raster(savi_list[1])
        savi_output = "D:/arcpy/results/trainingData/savi/SAVI_kulonprogo.TIF"
        savi_calculate = (Float(nir-red)/Float(nir+red+constant))*(1.5)
        savi_calculate.save(savi_output)
        print("Selesai menghitung SAVI")
    
    def msavi(self):
        ENV.workspace = self.outDIR+self.clipped_image
        msavi_band_list = ["*B4*", "*B5*"]
        msavi_list = []
        for msavi_calc in msavi_band_list:
            raster_src = arcpy.ListRasters(msavi_calc, "TIF")
            msavi_list.extend(raster_src)
        red = arcpy.sa.Raster(msavi_list[0])
        nir = arcpy.sa.Raster(msavi_list[1])
        msavi_output = "D:/arcpy/results/trainingData/msavi/MSAVI_kulonprogo.TIF"
        msavi_calculate = ((2*nir)+1-SquareRoot(((2*nir+1)**2)-(8*(nir-red))))/2
        msavi_calculate.save(msavi_output)
        print("Selesai menghitung MSAVI")
    
    # def twi(self):
        