# Supported Drones

`dm_extract` supports **7 manufacturer-specific extractors** plus a generic fallback for any other drone.

---

## Manufacturer Extractors

Each extractor handles GPS, orientation, calibrated focal length, and timestamp for its specific brand.

### DJI

Detected via `Make = DJI` or `Make = Hasselblad` with `drone-dji:` XMP namespace.

| Model | Sensor | Notes |
|---|---|---|
| Mavic 2 Pro | 1" (Hasselblad L1D-20c) | FC2204 |
| Mavic 3 / 3 Pro | 4/3" (Hasselblad L2D-20c) | |
| Mavic Air 2 | 1/2" | FC3411 |
| Mini 3 Pro | 1/1.3" | FC7303 |
| Phantom 4 RTK / Pro v2 | 1" | FC6310R, P4R |
| Matrice M30 | 1/2" wide | |
| Matrice M30T | 1/2" wide + zoom | |
| Matrice M600 + Zenmuse X5 | MFT 17.3 mm | |
| Matrice M600 + Zenmuse X5S | MFT 17.4 mm | |
| Zenmuse X5R | MFT 17.3 mm | |
| Zenmuse X7 | Super35 23.5 mm | |
| Zenmuse P1 | Full-frame 35 mm | FC8482 |
| Inspire / XT2 / FC3682 | — | GPS parsed from `exif:` XMP namespace |

RTK solution quality, GPS accuracy (RtkStdLat/Lon/Hgt), and relative/absolute altitude are all extracted.

---

### Autel Robotics

Detected via `Make = AUTEL` or model IDs `XL709`, `XT705`, `XB004`.

| Model | Notes |
|---|---|
| Evo II | |
| X-Star | |
| Evo II Pro / Enterprise | XL709, XT705, XB004 |

> **Note:** Autel uses the Pix4D pitch convention (0° = nadir, 90° = horizontal), which differs from DJI. This is flagged in the output metadata.

---

### Parrot

Detected via `Make = Parrot`.

| Model | Notes |
|---|---|
| ANAFI | Single-axis gimbal — camera angles copied to gimbal fields |
| ANAFI Ai | |

---

### senseFly (Parrot Professional)

Detected via Pix4D-style `Description:` XMP namespace.

| Model | Notes |
|---|---|
| eBee | Fixed-wing mapping drone |
| Aeria X | Fixed-wing — camera angles propagated to flight angles |

---

### Skydio

Detected via `skydio:` XMP prefix, or tags `CaptureUtime`, `VehiclePositionNED`, `CameraPositionNED`.

| Model | Sensor | Notes |
|---|---|---|
| Skydio 2 | 1/3.8" IMX577, 3.7 mm | Firmware quirk: `ExifImageWidth` may contain normalisation base (320 px) instead of actual resolution (4056 px) — corrected automatically |
| Skydio 2+ | 1/3.8" IMX577, 3.7 mm | Includes `[bracketed]` model tag variant |
| X10 VT300-Z 13 mm | 8000 × 6000 | 35 mm equiv., sq. pixels |
| X10 VT300-Z 50 mm | 9250 × 6878 | 9.8 mm focal length |

UTC timestamp is read from `xmp:CreateDate` (always written with `Z` suffix by Skydio firmware). `CaptureUtime` is a flight-relative counter (µs since boot) and is **not** used as a Unix timestamp.

---

### Yuneec / Xiro

Detected via `Make = Yuneec` or model prefixes `CGO2`, `CGO3`, `CGO4`, `XPLORER`, `UG3300`, `TYPHOON`, `H520`, `H850`.

| Model | Notes |
|---|---|
| Typhoon H | |
| Q500 | |
| H520 | |
| H850 | |
| Xiro Explorer | Xiro brand, same extractor |

---

### Xiaomi / FIMI

Detected via `Make = FIMI` or model prefixes `YTXJ`, `FIMI`, `MJX`.

| Model | Notes |
|---|---|
| FIMI X8 SE | |
| FIMI X8 Mini | |

---

## Fallback Extractor

Any drone not matched by the extractors above falls back to a generic extractor that reads:

- Standard EXIF GPS (latitude, longitude, altitude)
- `DateTimeOriginal` / `DateTime` timestamp
- Make, Model, focal length

No manufacturer-specific fields (relative altitude, gimbal angles, RTK) are extracted in fallback mode.

---

## Calibration Registry

The following models have a built-in calibration entry used to validate or compute the calibrated focal length in pixels when XMP data is absent or inconsistent.

| Model key | Image source | Focal (mm) | Sensor width (mm) | Resolution |
|---|---|---|---|---|
| M30T | WideCamera | 4.5 | 6.297 | 3840 × 2160 |
| M30 | WideCamera | 4.5 | 6.297 | 3840 × 2160 |
| M30T | ZoomCamera | — | — | median zoom |
| Mavic 3 | WideCamera | 12.3 | 17.3 | — |
| FC6310R (Phantom 4 RTK) | * | 8.8 | 13.2 | — |
| P4R | * | alias for FC6310R | | |
| FC2204 (Mavic 2 Pro) | * | 10.3 | 13.2 | — |
| FC3411 (Mavic Air 2) | * | 4.5 | 6.3 | — |
| FC8482 (Zenmuse P1) | * | 35.0 | 35.9 | — |
| M600 + X5 | * | — | 17.3 | 4608 × 3456 |
| M600 + X5S | * | — | 17.4 | 5280 × 3956 |
| X5S | * | — | 17.4 | 5280 × 3956 |
| X5R | * | — | 17.3 | 4608 × 3456 |
| X7 | * | — | 23.5 | 6016 × 4008 |
| FC7303 (Mini 3 Pro) | * | 6.7 | 9.4 | — |
| Skydio 2 | * | 3.7 | 4.78 | 4056 × 3040 |
| Skydio 2+ | * | 3.7 | 4.78 | 4056 × 3040 |
| Skydio 2+ `[…]` variant | * | 3.7 | 4.78 | 4056 × 3040 |
| X10 VT300-Z 13 mm | * | 35.0 eq. | 6.3683 | 8000 × 6000 |
| X10 VT300-Z 50 mm | * | 9.8 | 7.175 | 9250 × 6878 |

> `*` matches any `ImageSource` value. Entries with focal length = 0 rely on the EXIF `FocalLength` tag (variable-focal-length or interchangeable-lens systems).
