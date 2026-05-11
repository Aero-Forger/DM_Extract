# dm_extract ( *drone metadata extract* ) ![English](https://flagcdn.com/w40/gb.png)
![Langage](https://img.shields.io/badge/langage-C-blue.svg)

**English** | [Français](docs/README.fr.md)

> Extract drone image metadata from the command line.

`dm_extract` is a CLI tool for extracting EXIF, XMP and GPS metadata from drone JPG images.  
It produces structured, ready-to-use output in multiple formats — designed for integration into geomatics and photogrammetry workflows.

---

## Features

* 📷 Parses EXIF / XMP metadata from drone JPEG images (single file or batch)
* 📍 Extracts GPS coordinates, altitude, gimbal angles and calibrated focal length
* 📤 Exports to CSV and GeoJSON
* ⚡ Fast, scriptable, pipeline-friendly
* 100% written in C
* Runs on Windows, Linux and macOS
* Bonus: Python GUI tool 

---

## Usage

##### Syntaxe

```bash
dm_extract [options] FILE [FILE ...]
```

At least one file must be provided. Wildcards are accepted.

##### Options

| Option    | Forme longue    | Description                                               |
| --------- | --------------- | --------------------------------------------------------- |
| `-o FILE` | `--output FILE` | Output file. Default: stdout                              |
| `-g`      | `--geojson`     | GeoJSON output format. Default : CSV                      |
| `-n`      | `--no-header`   | Omit the header line CSV                                  |
| `-r`      | `--raw`         | Diagnostic mode: raw EXIF/XMP dump + structured summary   |
| `-q`      | `--quiet`       | Delete progress messages on stderr                        |
| `-V`      | `--version`     | Show version and exit                                     |
| `-h`      | `--help`        | Show help and exit                                        |

#####  Exit codes

| Code |                             Meaning                          |
| ---- | ------------------------------------------------------------ |
|  `0` | Success — all files have been processed                      |
|  `1` | At least one file in error (read, format not recognized)     |
|  `2` | Arguments error (unknown option, inaccessible output file)   |

##### Single file

```bash
# Linux / macOS
./dm_extract DJI_0001.JPG

# Windows
dm_extract.exe DJI_0001.JPG
```
See [binaries](https://github.com/Aero-Forger/DM_Extract/blob/main/binaries.md) for more details

---

### Test Python GUI

[GUI](https://github.com/Aero-Forger/DM_Extract/blob/main/dm_extract_gui_en.py)

Quick python tool to graphically test dm_extract.  
The static binary use is <mark>preferred</mark> to be able to make scripts or to be integrate into an exernal workflow.   
The GUI does not allow it.

:warning: the Python GUI is a simple test tool that **is not part of the code** of `dm_extract`

---
### Output:

[output CSV](https://github.com/Aero-Forger/DM_Extract/blob/main/CSV_sample.md)

---
### Limitations

- Only **JPEG** files (`.jpg`, `.JPG`) are supported. RAW formats (DNG, CR2, NEF) are not yet supported.
- The maximum scan size per file is **512 KB** (the EXIF + XMP blocks of a drone fit in the first 128 KB).
- The processing is **sequential** (one file at a time) only with **-- raw**
- In GeoJSON mode, images without valid GPS are excluded without warning message (use '--raw` to diagnose).
  
---

## Use cases

- Build flight logs from a set of drone images
- Feed coordinates directly into QGIS, GDAL, or any GIS tool
- Pre-process image sets before photogrammetry pipelines (Metashape, ODM...)
- Quality-check GPS coverage before processing

## Supported drones:

7 brands detected automatically: **DJI**, **Parrot**, **senseFly**, **Skydio**, **Autel Robotics**, **Yuneec**, **Xiaomi**.

[Drones](https://github.com/Aero-Forger/DM_Extract/blob/main/SUPPORTED_DRONES.md)

---

## Part of the Aeroforger ecosystem

`dm_extract` is an open-source tool maintained under the [Aeroforger](https://github.com/Aero-Forger) project — a collection of tools for drone data processing, photogrammetry and geomatics.

Support the project on [Patreon](https://www.patreon.com/Aeroforger).

---

## License
**LGPL v3**
