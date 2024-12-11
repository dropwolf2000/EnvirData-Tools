#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time       : 2023/6/8 19:57
# @Author     : 落狼
# @File       : batch_unpacking.py
# @Environment: Python 3.9.1.2
# @Software   : PyCharm

import gzip
import os


def batch_extract_gz_files(input_dir, output_dir):
    # 检查输出目录是否存在，若不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录下的所有文件
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            # 检查文件扩展名是否为.gz
            if filename.endswith('.gz'):
                input_path = os.path.join(root, filename)
                output_path = os.path.join(output_dir, os.path.splitext(filename)[0])

                # 解压缩gz文件
                with gzip.open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
                    f_out.write(f_in.read())
                    print(f'解压缩文件: {filename}')


if __name__ == '__main__':

    # 使用示例
    input_dir = r'D:\TEMP\gsmap\origin\realtime\v8_daily0.1'  # 输入目录，存放gz文件的目录
    output_dir = r'D:\TEMP\gsmap\output'  # 输出目录，存放解压缩后的文件的目录

    batch_extract_gz_files(input_dir, output_dir)
