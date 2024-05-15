# environment-convert-tools

---

用于实现各种水文学环境数据格式之间的工具, 顺便重构之前的各种转换工具
之前的flux2nc和flt2nc已经整合进来

## Features Implemented

### GSMaP
- [x] DAT to NetCDF
- [ ] DAT to GeoTIFF

### ERA5
- [ ] Hourly ERA5 NetCDF to Daily GeoTIFF
- [ ] Hourly ERA5 NetCDF to Daily NetCDF

### ANUSPLIN
- [x] FLT to NetCDF
- [ ] FLT to Compressed GeoTIFF
    - **PLOT**
      - [x] NC PLOT


### VIC Model
- [x] OUTPUT Fluxes to NetCDF ()
  - 基于servir-vic-training项目中的flux2nc工具改进而来 修改如下 
    - 1. 选项将作为方法的参数输入
      2. 修复了读取fluxes和snows文件在同一目录时的读取错误问题
      3. 修复了fluxes读取串行的问题(前三列为年月日 而不进行小时模拟的情况)



### Others
- [ ] NetCDF to GeoTIFF
- [ ] GeoTIFF to NetCDF
