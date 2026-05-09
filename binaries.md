# dm_extract — Drone Metadata Extractor

### Platform : 
          - Linux x86-64 (static binary, no dependencies)
            Tested on: Ubuntu 22.04 / 24.04, Debian 12 and Fedora 43/44
          - Windows 10 and 11
          - Mac: on-going bug corrections - pending

### USAGE

```bash
chmod +x dm_extract
 ./dm_extract photo.jpg
 ./dm_extract -o report.csv flight/*.JPG
 ./dm_extract --geojson flight/*.JPG > flight.geojson
 ./dm_extract --raw DJI_0001.JPG
 ./dm_extract --help
```

### OUTPUTS

CSV (default) : 33 columns — GPS, orientation, calibration, LRF, RTK
 GeoJSON : FeatureCollection, one Feature per GPS‑valid image

### SUPPORTED BRANDS

DJI · Parrot · senseFly · Skydio · Autel · Yuneec · Xiaomi/FIMI

### EXIT CODES

0 Success  
1 At least one file in error  
2 Argument error  
