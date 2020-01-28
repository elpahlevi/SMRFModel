import arcpy
import os, math
from arcpy import env as ENV
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

class trainingData():
    workDIR = r"D:/PersonalAssets/PersonalThings/Projects/skripsi-ku"
    outDIR = r"D:/PersonalAssets/PersonalThings/Projects/skripsi-ku/output/trainingData"
    ENV.overwriteOutput = True
    
    def evi(self):
        ENV.workspace = self.workDIR + "/output/clipped-images"
        bandLists = ["*B2*", "*B4*", "*B5*"]
        lists = []
        evi_image = "/evi"
        out = self.outDIR + evi_image
        os.makedirs(out)
        for evi_raster in bandLists:
            raster_src = arcpy.ListRasters(evi_raster, "TIF")
            lists.extend(raster_src)
        blue = arcpy.sa.Raster(lists[0])
        red = arcpy.sa.Raster(lists[1])
        nir = arcpy.sa.Raster(lists[2])
        evi = 2.5 * Float(nir-red)/Float(nir + (6.0*red)-(7.5*blue)+1)
        evi.save(os.path.join(out, "evi.TIF"))
        print("Selesai menghitung EVI")

    def savi(self):
        ENV.workspace = self.outDIR + "/output/clipped-images"
        bandLists = ["*B4*", "*B5*"]
        cons = 0.5
        lists = []
        savi_image = "/savi"
        out = self.outDIR + savi_image
        os.makedirs(out)
        for savi_raster in bandLists:
            raster_src = arcpy.ListRasters(savi_raster, "TIF")
            lists.extend(raster_src)
        red = arcpy.sa.Raster(lists[0])
        nir = arcpy.sa.Raster(lists[1])
        savi = (Float(nir-red)/Float(nir+red+cons))*(1.5)
        savi.save(os.path.join(out, "savi.TIF"))
        print("Selesai menghitung SAVI")

    def msavi(self):
        ENV.workspace = self.outDIR + "/output/clipped-images"
        bandLists = ["*B4*", "*B5*"]
        lists = []
        msavi_image = "/msavi"
        out = self.outDIR + msavi_image
        os.makedirs(out)
        for msavi_raster in bandLists:
            raster_src = arcpy.ListRasters(msavi_raster, "TIF")
            lists.extend(raster_src)
        red = arcpy.sa.Raster(lists[0])
        nir = arcpy.sa.Raster(lists[1])
        msavi = ((2*nir)+1-SquareRoot(((2*nir+1)**2)-(8*(nir-red))))/2
        msavi.save(os.path.join(out, "msavi.TIF"))
        print("Selesai menghitung MSAVI")
# evi = trainingData().evi()
# savi = trainingData().savi()
# msavi = trainingData().msavi()