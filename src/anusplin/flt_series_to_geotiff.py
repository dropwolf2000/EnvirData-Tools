#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time       : 2024/6/21 下午4:10
# @Author     : 落狼
# @File       : flt_series_to_geotiff.py
# @Environment: Python 3.9.1.2
# @Software   : PyCharm
# attr set
import glob
import os.path
from osgeo import gdal, gdalconst, osr
from tqdm import tqdm
from joblib import Parallel, delayed
import datetime
from pathlib import Path


# default_band = 1
# nodata_value = -9999
# geotransform = (73.446647817425, 0.01, 0.0, 53.56, 0.0, -0.01)
# projection_code = 4326



temp_geotrans = None

def flt_to_compressedTif(flt_file, output_tif):
    dst = gdal.Open(flt_file)

    global temp_geotrans
    if temp_geotrans is None:
        temp_geotrans = dst.GetGeoTransform()


    band1 = dst.GetRasterBand(1)
    data_arr = band1.ReadAsArray()

    x_pixs, y_pixs = dst.RasterXSize, dst.RasterYSize

    # OUTPUT
    driver = gdal.GetDriverByName("GTiff")

    options = [f"COMPRESS=LZW", "TILED=YES"]
    output_dst = driver.Create(output_tif, x_pixs, y_pixs, 1, gdalconst.GDT_Float32, options)

    if output_dst is None:
        raise Exception("tiff create false")

    # write data
    output_dst.GetRasterBand(1).WriteArray(data_arr)
    # set nodata value(mask
    output_dst.GetRasterBand(1).SetNoDataValue(-9999)
    # set geotransform
    # output_dst.SetGeoTransform((73.446647817425, 0.01, 0.0, 53.56, 0.0, -0.01))
    # output_dst.SetGeoTransform((73.446647817425, 0.05, 0.0, 53.55, 0.0, -0.05))
    output_dst.SetGeoTransform(temp_geotrans)
    # set projection
    wgs84_srs = osr.SpatialReference()
    wgs84_srs.ImportFromEPSG(4326)
    output_dst.SetProjection(wgs84_srs.ExportToWkt())

    # clear memories
    output_dst.FlushCache()
    output_dst = None
    dst = None

    return True






if __name__ == '__main__':

    input = Path(r'D:\PROJECTS\PRECIPITATION_CLASSIFY\PrecipitaionQueryResult_V3_yearly\anu\r3\data\output')
    output = Path(r'D:\PROJECTS\PRECIPITATION_CLASSIFY\PrecipitaionQueryResult_V3_yearly\anu\r3\data\tif')

    for f in input.glob('*.flt'):
        output_tif = str(output.joinpath(f.stem + '.tif'))

        if flt_to_compressedTif(str(f), output_tif):
            print(f'[ INFO ] {os.path.basename(f)}')