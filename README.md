# dm_extract

> Extract drone image metadata from the command line.

`dm_extract` is a CLI tool for extracting EXIF, XMP and GPS metadata from drone JPG images. It produces structured, ready-to-use output in multiple formats — designed for integration into geomatics and photogrammetry workflows.

---

## Features

- 📷 Parses EXIF / XMP metadata from drone JPG images (single file or batch)
- 📍 Extracts GPS coordinates and altitude
- 📤 Exports to multiple formats: **JSON**, **CSV**, **GeoJSON**
- ⚡ Fast, scriptable, pipeline-friendly
- 100% written in C
- Ported for Windows, Linux and Mac OsX

---

## Usage

### Single file

```bash
dm_extract image.jpg
```
See binaries documents for more details

---

## Use cases

- Build flight logs from a set of drone images
- Feed coordinates directly into QGIS, GDAL, or any GIS tool
- Pre-process image sets before photogrammetry pipelines (Metashape, ODM...)
- Quality-check GPS coverage before processing

## Supported drones:

[Drones](https://github.com/Aero-Forger/DM_Extract/blob/main/SUPPORTED_DRONES.md)

---

## Part of the Aeroforger ecosystem

`dm_extract` is an open-source tool maintained under the [Aeroforger](https://github.com/Aeroforger) project — a collection of tools for drone data processing, photogrammetry and geomatics.

Support the project on [Patreon](https://www.patreon.com/Aeroforger).

---

## License
**LGPL v3**
