import arcpy
import os, math
from arcpy import env as ENV
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

class gis():
    workDIR = r"D:/arcpy"
    ENV.overwriteOutput = True
    outDIR = r"D:/arcpy/results"
    satellite_image = "/satellite_image"
    corrected_image = "/correctedImage"
    clipped_image = "/clippedImage"
    shapeFile = "/shapeFile"
    count = 0

    def rad_correction(self):
        ENV.workspace = self.workDIR+self.satellite_image
        raster_src = arcpy.ListRasters("","TIF")
        ref_mult_band = 0.00002
        ref_add_band = -0.1
        sun_elevation = 54.19672095
        pi = math.pi
        sin = math.sin
        for raster_process in raster_src:
            self.count +=1
            raster_assign = arcpy.sa.Raster(raster_process)
            toa_corrected = (ref_mult_band * raster_assign) + (ref_add_band)
            su_corrected = toa_corrected/(sin((sun_elevation*pi)/180))
            su_corrected.save(os.path.join(self.outDIR+self.corrected_image, raster_process))
            print ("Terkoreksi Band "+str(self.count))
        print ("Selesai koreksi")
        print ("Mulai memotong citra")

    def clip_image(self):
        ENV.workspace = self.outDIR+self.corrected_image
        kulonprogo_shape = self.outDIR+self.shapeFile+"/kulonprogo.shp"
        raster_src = arcpy.ListRasters("","TIF")
        for raster_clip in raster_src:
            self.count +=1
            raster_assign_image = arcpy.sa.Raster(raster_clip)
            arcpy.Clip_management(raster_assign_image, "#", os.path.join(self.outDIR+self.clipped_image, raster_clip), kulonprogo_shape, "0", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
            print("Band "+str(self.count)+" Terpotong")
        print("Selesai Memotong")    
        
    def comp_image(self):
        ENV.workspace = self.outDIR+self.clipped_image
        band_list = ["*B2*", "*B3*", "*B4*", "*B5*", "*B6*", "*B7*"]
        band_comps = []
        for ras in band_list:
            raster_src = arcpy.ListRasters(ras, "TIF")
            band_comps.extend(raster_src)
        output_name = "D:/arcpy/results/compositeImage/kulonprogo_composite.TIF"
        semicolon = ";"
        b2 = band_comps[0]
        b3 = band_comps[1]
        b4 = band_comps[2]
        b5 = band_comps[3]
        b6 = band_comps[4]
        b7 = band_comps[5]
        str_composite = b2+semicolon+b3+semicolon+b4+semicolon+b5+semicolon+b6+semicolon+b7
        arcpy.CompositeBands_management(str_composite, output_name)
        print("Selesai membuat citra komposit")
#run the function
# run_correction = gis().rad_correction()
# run_clip = gis().clip_image()
#composite_clip = gis().comp_image()


    
