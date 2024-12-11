#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time       : 2023/6/8 18:12
# @Author     : 落狼
# @File       : dat2tiff.py
# @Environment: Python 3.9.1.2
# @Software   : PyCharm

import datetime
import os
import sys
import numpy as np
from osgeo import gdal
import netCDF4
from utils import file_tools, gdal_tools, time_tools

from tqdm import tqdm

from joblib import Parallel, delayed



def read_dat(dat_file, data_shape=None):
    with open(dat_file, 'rb') as f:
        dat_data = np.fromfile(dat_file, dtype='<f', count=-1)

    # reshape
    if data_shape:
        dat_data = dat_data.reshape(data_shape)

    return dat_data


def save_tiff(output_path, data, projection, geotransform):
    """
    save array data to tiff
    :param output_path: full tif output path
    :param data: 2d data array
    :param projection:
    :param geotransform:
    :return:
    """
    driver = gdal.GetDriverByName('GTiff')
    # default single band
    bands = 1
    # set geotrans and proj
    rows, cols = data.shape

    dataset = driver.Create(output_path, cols, rows, bands, gdal.GDT_Float32, options=['COMPRESS=LZW'])
    dataset.SetGeoTransform(geotransform)
    dataset.SetProjection(projection)

    # write data to tiff
    band = dataset.GetRasterBand(1)
    band.WriteArray(data)
    band.FlushCache()

    # release ds
    dataset = None


def dat_to_tiff_batch(dat_path, save_path):
    dat_s = file_tools.get_all_files(dat_path)
    geotrans = (0, 0.1, 0, 60, 0, -0.1)
    proj = gdal_tools.wkt_proj(4326)


    def datToTiff(dat, save_path):
        # read dat
        # GSMaP dat *24 for one day
        dat_matrix = read_dat(dat, (1200, 3600)) * 24

        # dat_date = os.path.basename(dat)[:-5]
        dat_date = time_tools.extract_time_from_string(dat)
        # print(f'[INFO] dat: {dat} ReadIn')
        # dats_bar.set_description(os.path.basename(dat))

        # create dir
        file_tools.create_directory(save_path)
        # geotrans and proj
        output_file = os.path.join(save_path, dat_date + '.tif')
        # save tiff
        save_tiff(output_file, dat_matrix, proj, geotrans)


    dats_bar = tqdm(dat_s)

    # for dat in dats_bar:
    #     dats_bar.set_description(os.path.basename(dat))

    Parallel(n_jobs=8)(delayed(datToTiff)(dat, save_path) for dat in dats_bar)



def output_zero_tif(tif_path):
    geotrans = (0, 0.1, 0, 60, 0, -0.1)
    proj = gdal_tools.wkt_proj(4326)

    dat_matrix = np.zeros((1200, 3600))

    save_tiff(tif_path, dat_matrix, proj, geotrans)
    print('OK')







if __name__ == '__main__':
    # files = file_tools.get_all_files(r'E:\DATA\a1_DATA_COLLECTION\a1_Hydrology\PRE\TRMM_Daily3B42RT')
    # output_path = r'E:\DATA\a1_DATA_COLLECTION\a2_HydroData_AfterConvertion\PRE\TRMM_Daily3B42RT'
    # for file in files:
    #     nc_to_tiff(file, output_path)


    input_dir = r'D:\TEMP\gsmap\output'
    output_dir = r'E:\DATA\a1_DATA_COLLECTION\a1_Hydrology\PRE\GSMaP\_realtime_ver_v8_daily0.1\tif'
    # output_dir = r'D:\TEMP\GSMaP_download_temp\realtime_collection\tif'
    #
    dat_to_tiff_batch(input_dir, output_dir)


    # output_zero_tif('20170225.tif')


