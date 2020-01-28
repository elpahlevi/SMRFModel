import arcpy
import os, math
from arcpy import env as ENV
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

class preprocessing():
    workDIR = r"D:/PersonalAssets/PersonalThings/Projects/skripsi-ku"
    outDIR = r"D:/PersonalAssets/PersonalThings/Projects/skripsi-ku/output"
    ENV.overwriteOutput = True
    count = 0

    def correction(self):
        ENV.workspace = self.workDIR + "/src-data"
        correctedImages = "/corrected-images"
        rs_source = arcpy.ListRasters("","TIF")
        ref_mult_band = 0.00002
        ref_add_band = -0.1
        sun_elev = 50.32421680
        pi = math.pi
        sin = math.sin
        out = self.outDIR+correctedImages
        os.makedirs(out)
        for raster_correction in rs_source:
            self.count +=1
            raster_lists = arcpy.sa.Raster(raster_correction)
            toa_correction = (ref_mult_band * raster_lists) + (ref_add_band) 
            sunElev_correction = toa_correction/(sin((sun_elev*pi)/180))
            sunElev_correction.save(os.path.join(out, "corrected_"+raster_correction))
            print ("Terkoreksi Band "+str(self.count))
        print ("Selesai koreksi")

    def clip(self):
        ENV.workspace = self.outDIR + "/corrected-images"
        shapefile = self.workDIR + "/src-data/shp-training/shp-training.shp"
        clipped = "/clipped-images"
        out = self.outDIR+clipped
        os.makedirs(out)
        rs_source = arcpy.ListRasters("", "TIF")
        for raster_clip in rs_source:
            self.count +=1
            raster_lists = arcpy.sa.Raster(raster_clip)
            arcpy.Clip_management(raster_lists, "#", os.path.join(out, "clipped_"+raster_clip), shapefile, "0", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
            print("Band "+str(self.count)+" Terpotong")
        print("Selesai memotong")

    def ndvi(self):
        ENV.workspace = self.outDIR + "/clipped-images"
        bandList = ["*B4*", "*B5*"]
        lists = []
        ndvi_image = "/ndvi"
        out = self.outDIR+ndvi_image
        os.makedirs(out)
        for ndvi in bandList:
            src = arcpy.ListRasters(ndvi, "TIF")
            lists.extend(src)
        red = arcpy.sa.Raster(lists[0])
        nir = arcpy.sa.Raster(lists[1])
        ndvi_calculate = Float(nir-red)/Float(nir+red)
        ndvi_calculate.save(os.path.join(out, "ndvi.TIF"))
        print("Selesai memroses NDVI")
    
    def ems(self):
        ENV.workspace = self.outDIR + "/ndvi"
        ras_ndvi = arcpy.ListRasters("", "TIF")
        ems_image = "/ems"
        out = self.outDIR+ems_image
        os.makedirs(out)
        for raster in ras_ndvi:
            ndvi = arcpy.sa.Raster(raster)
        ndvi_min =  -0.0099316 
        ndvi_max =  0.826289
        propveg = Square((ndvi-ndvi_min)/(ndvi_max-ndvi_min))
        emissivity = 0.004*propveg + 0.986
        emissivity.save(os.path.join(out, "ems.TIF"))
        print("Selesai memroses emisivitas")
    
    def tbrightness(self):
        ENV.workspace = self.workDIR + "/src-data"
        shp = self.workDIR + "/src-data/shp-training/shp-training.shp"
        sr_list = ["*B10*", "*B11*"]
        tirs_list = []
        rad_mult = 0.0003342
        rad_add = 0.1
        tb_image = "/tb"
        out = self.outDIR+tb_image
        os.makedirs(out)
        for raster in sr_list:
            tirs = arcpy.ListRasters(raster, "TIF")
            tirs_list.extend(tirs)
        b10 = arcpy.sa.Raster(tirs_list[0])
        b11 = arcpy.sa.Raster(tirs_list[1])
        arcpy.Clip_management(b10, "#", os.path.join(out, "b10_clip.TIF") , shp, "0", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
        arcpy.Clip_management(b11, "#", os.path.join(out, "b11_clip.TIF") , shp, "0", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
        
        #calculate spectral radiance
        b10_clip = self.outDIR + "/tb/b10_clip.TIF"
        b11_clip = self.outDIR + "/tb/b11_clip.TIF"
        b10_raster = arcpy.sa.Raster(b10_clip)
        b11_raster = arcpy.sa.Raster(b11_clip)
        sr10 = (rad_mult * b10_raster) + rad_add
        sr11 = (rad_mult * b11_raster) + rad_add
        print("Selesai menghitung spectral radiance")
        
        #calculate brightness temperature
        K1_CONSTANT_BAND_10 = 774.8853
        K2_CONSTANT_BAND_10 = 1321.0789
        K1_CONSTANT_BAND_11 = 480.8883
        K2_CONSTANT_BAND_11 = 1201.1442
        tb10 = K2_CONSTANT_BAND_10/Ln((K1_CONSTANT_BAND_10/sr10)+1)
        tb11 = K2_CONSTANT_BAND_11/Ln((K1_CONSTANT_BAND_11/sr11)+1)
        tb_ave = (tb10+tb11)/2
        tb_ave.save(os.path.join(out, "tb.TIF"))
        print("Selesai menghitung suhu kecerahan")
    
    def ts(self):
        ENV.workspace = self.outDIR + "/tb"
        ems = arcpy.sa.Raster(self.outDIR + "/ems/ems.TIF")
        tb = arcpy.sa.Raster("tb.TIF")
        ts_image = "/ts"
        out = self.outDIR + ts_image
        os.makedirs(out)
        w = 11.5
        p = 14380
        ts = tb / (1 + (w*(tb/p)*Ln(ems)))
        ts.save(os.path.join(out, "ts.TIF"))
        print("Selesai menghitung suhu permukaan")

# correction = preprocessing().correction();
# clip = preprocessing().clip()
# ndvi = preprocessing().ndvi()
# ems = preprocessing().ems()
# tb = preprocessing().tbrightness()
#ts = preprocessing().ts()