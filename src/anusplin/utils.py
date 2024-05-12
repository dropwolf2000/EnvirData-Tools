#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time       : 2024/5/1 下午4:20
# @Author     : 落狼
# @File       : utils.py
# @Environment: Python 3.9.1.2
# @Software   : PyCharm

# 写一个检查特定后缀名日期序列完整性的方法
import os
from datetime import datetime, timedelta
from typing import List
from collections import defaultdict
from pathlib import Path
import re


def __extract_time_from_string(search_string: str) -> str:
    # 从文件名中提取时间字符串
    pattern = r"\d{8}"  # 时间格式为年份后跟着月份和日期，例如 20230527
    match = re.search(pattern, search_string)
    # print(match)
    if match:
        searched_dt = datetime.strptime(match.group(), '%Y%m%d')

        return searched_dt.strftime('%Y%m%d')
    else:
        raise ValueError("No time string found in the search string")


def check_date_sequence_integrity(file_list: List[str]) -> None:
    """
    检查文件名中的日期序列是否连续
    :param file_list: 文件名列表
    :return:
    """
    # 获取目录下所有文件名
    file_names = list(file_list)

    file_names = list(map(__extract_time_from_string, file_names))

    if not file_names:
        print("目录中没有文件.")
        return

    # 提取日期部分并转换为日期对象
    dates = [datetime.strptime(file_name, "%Y%m%d") for file_name in file_names]

    # 对日期进行排序
    dates.sort()

    # 检查日期序列的连续性
    start_date = dates[0]
    end_date = dates[-1]
    expected_date = start_date
    missing_dates = []

    while expected_date <= end_date:
        if expected_date not in dates:
            missing_dates.append(expected_date)
        expected_date += timedelta(days=1)

    if not missing_dates:
        print("文件日期序列是连续的.")
    else:
        print("文件日期序列不连续. 缺失的日期:")
        for date in missing_dates:
            print(date.strftime("%Y-%m-%d"))

    print("起始日期:", start_date.strftime("%Y-%m-%d"))
    print("结束日期:", end_date.strftime("%Y-%m-%d"))





if __name__ == '__main__':
    # 测试
    # 应该只获取到文件名列表
    filename_list = [f.name for f in
                     Path(r'D:\PROJECTS\hnsw_soil_moisture_surface\auto_anu\run2\data\output').glob('*.flt')]
    result = check_date_sequence_integrity(filename_list)

