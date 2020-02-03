import arcpy
import os, math, shutil
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
        ENV.workspace = self.workDIR + "/output/clipped-images"
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
        ENV.workspace = self.workDIR + "/output/clipped-images"
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
    
    def twi(self):
        ENV.workspace = self.workDIR + "/output/dem"
        ras_dem = arcpy.ListRasters("","TIF")
        twi_image = "/twi"
        slope_image = "/slope"
        aspect_image = "/aspect"
        
        out_twi = self.outDIR + twi_image
        out_slope = self.outDIR + slope_image
        out_aspect = self.outDIR + aspect_image
        outMeasurement = "DEGREE"
        zFactor = ""
        method = "PLANAR"
        zUnit = "METER"
        forceFlow = "FORCE"
        inWeightRaster = ""
        dataType = "INTEGER"
        os.makedirs(out_twi)
        os.makedirs(out_slope)
        os.makedirs(out_aspect)
        for raster in ras_dem:
            dem = arcpy.sa.Raster(raster)
        # menghitung slope
        slope = Slope(dem, outMeasurement, zFactor, method, zUnit)
        slope.save(os.path.join(out_slope, "slope.TIF"))
        print("Berhasil menghitung slope")
        print("Menghitung aspect")
        # menghitung aspect
        aspect = Aspect(dem, method, zUnit)
        aspect.save(os.path.join(out_aspect, "aspect.TIF"))
        # menghitung flow direction dan flow accumumlation
        flowdir = FlowDirection(dem, forceFlow, "")
        flowAcc = FlowAccumulation(flowdir, inWeightRaster, dataType) + 1
        # konversi slope dari degree ke radian
        slope_radian = slope * math.pi/180.0
        # menghitung TWI
        twi = Ln(flowAcc / (Tan(slope_radian)+.01))
        twi.save(os.path.join(out_twi, "twi.TIF"))
        print("Berhasil menghitung TWI")
    
    def ndmi(self):
        ENV.workspace = self.workDIR  + "/output/clipped-images"
        bandLists = ["*B5*", "*B6*"]
        lists = []
        ndmi_image = "/ndmi"
        out = self.outDIR + ndmi_image
        os.makedirs(out)
        for ndmi_raster in bandLists:
            raster_src = arcpy.ListRasters(ndmi_raster, "TIF")
            lists.extend(raster_src)
        nir = arcpy.sa.Raster(lists[0])
        swir1 = arcpy.sa.Raster(lists[1])
        ndmi = nir - swir1 / nir + swir1
        ndmi.save(os.path.join(out, "ndmi.TIF"))
        print("Selesai menghitung NDMI")
    
    def mndwi(self):
        ENV.workspace = self.workDIR + "/output/clipped-images"
        bandLists = ["*B3*", "*B6*"]
        lists = []
        mndwi_image = "/mndwi"
        out = self.outDIR + mndwi_image
        os.makedirs(out)
        for mndwi_raster in bandLists:
            raster_src = arcpy.ListRasters(mndwi_raster, "TIF")
            lists.extend(raster_src)
        green = arcpy.sa.Raster(lists[0])
        swir1 = arcpy.sa.Raster(lists[1])
        mndwi = green - swir1 / green + swir1
        mndwi.save(os.path.join(out, "mndwi.TIF"))
        print("Selesai menghitung MNDWI")

    def msi(self):
        ENV.workspace = self.workDIR + "/output/clipped-images"
        bandLists = ["*B5*", "*B6*"]
        lists = []
        msi_image = "/msi"
        out = self.outDIR + msi_image
        os.makedirs(out)
        for msi_raster in bandLists:
            raster_src = arcpy.ListRasters(msi_raster, "TIF")
            lists.extend(raster_src)
        nir = arcpy.sa.Raster(lists[0])
        swir1 = arcpy.sa.Raster(lists[1])
        msi = swir1/nir
        msi.save(os.path.join(out, "msi.TIF"))
        print("Selesai menghitung MSI")

    def thermal(self):
        ENV.workspace = self.workDIR + "/output/clipped-images"
        dirFolder = ENV.workspace + "/"
        bandLists = ["*B5*", "*B6*", "*B7*", "*B10*", "*B11*" ]
        lists = []
        thermal_images = "/thermal"
        out = self.outDIR + thermal_images
        os.makedirs(out)
        for thermal_raster in bandLists:
            raster_src = arcpy.ListRasters(thermal_raster, "TIF")
            lists.extend(raster_src)
        nir = lists[0]
        swir1 = lists[1]
        swir2 = lists[2]
        tirs1 = lists[3]
        tirs2 = lists[4]
        shutil.copyfile(dirFolder+ nir, os.path.join(out, "nir.TIF"))
        shutil.copyfile(dirFolder + swir1, os.path.join(out, "swir1.TIF"))
        shutil.copyfile(dirFolder + swir2, os.path.join(out, "swir2.TIF"))
        shutil.copyfile(dirFolder + tirs1, os.path.join(out, "tirs1.TIF"))
        shutil.copyfile(dirFolder + tirs2, os.path.join(out, "tirs2.TIF"))
        print("Selesai memroses citra thermal")

evi = trainingData().evi()
savi = trainingData().savi()
msavi = trainingData().msavi()
twi = trainingData().twi()
ndmi = trainingData().ndmi()
mndwi = trainingData().mndwi()
msi = trainingData().msi()
thermal = trainingData().thermal()