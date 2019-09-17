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
    ndvi_image = "/ndvi"
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

    def ndvi(self):
        ENV.workspace = self.outDIR+self.clipped_image
        band_ndvi_list = ["*B4*", "*B5*"]
        ndvi_list = []
        for ndvi_calc in band_ndvi_list:
            raster_src = arcpy.ListRasters(ndvi_calc, "TIF")
            ndvi_list.extend(raster_src)
        ndvi_output = "D:/arcpy/results/ndvi/NDVI_kulonprogo.TIF"
        red = arcpy.sa.Raster(ndvi_list[0])
        nir = arcpy.sa.Raster(ndvi_list[1])
        ndvi_calculate = Float(nir-red)/Float(nir+red)
        ndvi_calculate.save(ndvi_output)
        print("Selesai memroses NDVI")

    def prop_ems_veg(self):
        ENV.workspace = self.outDIR+self.ndvi_image
        raster_ndvi = arcpy.ListRasters("","TIF")
        for ras_ndvi in raster_ndvi:
            ndvi_raster = arcpy.sa.Raster(ras_ndvi)
        ndvi_min = -0.6998
        ndvi_max = 0.870175
        ems_output = "D:/arcpy/results/ems/ems_kulonprogo.TIF"
        proportion_vegetation = Square((ndvi_raster-ndvi_min)/(ndvi_max-ndvi_min))
        ems = 0.004*proportion_vegetation + 0.986
        ems.save(ems_output)
        print("Selesai menghitung Emisivitas")

    def t_brightness(self):
        ENV.workspace = self.workDIR+self.satellite_image
        kulonprogo_shape = self.outDIR+self.shapeFile+"/kulonprogo.shp"
        raster_sr_list = ["*B10*", "*B11*"]
        image_list = []
        rad_mult = 0.0003342
        rad_add = 0.1
        b10_clip = "D:/arcpy/results/sr/b10_kulonprogo.TIF"
        b11_clip = "D:/arcpy/results/sr/b11_kulonprogo.TIF"
        tb_output = "D:/arcpy/results/sr/tb_kulonprogo.TIF"
        for ras_sr in raster_sr_list:
            raster_src = arcpy.ListRasters(ras_sr, "TIF")
            image_list.extend(raster_src)
        #clip image
        b10 = arcpy.sa.Raster(image_list[0])
        arcpy.Clip_management(b10, "#", b10_clip , kulonprogo_shape, "0", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
        b11 = arcpy.sa.Raster(image_list[1])
        arcpy.Clip_management(b11, "#", b11_clip , kulonprogo_shape, "0", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
        #calculate spectral radiance
        b10_raster = arcpy.sa.Raster(b10_clip)
        b11_raster = arcpy.sa.Raster(b11_clip)
        sr_10 = (rad_mult * b10_raster) + rad_add
        sr_11 = (rad_mult * b11_raster) + rad_add
        #calculate brightness temperature
        K1_CONSTANT_BAND_10 = 774.8853
        K2_CONSTANT_BAND_10 = 1321.0789
        K1_CONSTANT_BAND_11 = 480.8883
        K2_CONSTANT_BAND_11 = 1201.1442

        tb_10 = K2_CONSTANT_BAND_10/Ln((K1_CONSTANT_BAND_10/sr_10)+1)
        tb_11 = K2_CONSTANT_BAND_11/Ln((K1_CONSTANT_BAND_11/sr_11)+1)
        #calculate average brightness temperature
        tb_ave = (tb_10+tb_11)/2
        tb_ave.save(tb_output)

#run the function
# run_correction = gis().rad_correction()
# run_clip = gis().clip_image()
#composite_clip = gis().comp_image()
#ndvi_run = gis().ndvi()
#ems_run = gis().prop_ems_veg()
sr_run = gis().t_brightness()


    
