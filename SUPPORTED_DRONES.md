# Supported Drones

`dm_extract` supports **7 manufacturer-specific extractors** plus a generic fallback for any other drone.

---

## Manufacturer Extractors

Each extractor handles GPS, orientation, calibrated focal length, and timestamp for its specific brand.

### DJI

*Detection: XMP `drone-dji:` · Make = `DJI` or `Hasselblad`*

| Model / series            | Notes                                    | Features                                         |
| ------------------------- | ---------------------------------------- | ------------------------------------------------ |
| Matrice 300 RTK / 350 RTK | Zenmuse H20T · H20 — WideCamera          | RTK · LRF · calibration · orientation · full GPS |
| Matrice 30T / 30          | WideCamera 4.4mm · ZoomCamera 21mm       | RTK · LRF · calibration · orientation · full GPS |
| Phantom 4 RTK / Pro       | FC6310R · P4R — 1" sensor                | RTK · calibration · orientation · full GPS       |
| Mavic 3 / 3 Pro           | Hasselblad L2D-20c — 4/3" sensor         | calibration · orientation · full GPS             |
| Mavic 2 Pro               | FC2204 · Hasselblad L1D-20c — 1"         | calibration · orientation · full GPS             |
| Mavic Air 2               | FC3411 — 1/2" sensor                     | calibration · orientation · full GPS             |
| Mini 3 Pro                | FC7303 — 1/1.3" sensor                   | calibration · orientation · full GPS             |
| Zenmuse P1                | FC8482 — full-frame 45 MP, f35mm         | RTK · calibration · orientation · full GPS       |
| Zenmuse X5 / X5S / X5R    | MFT sensor, focal length from EXIF       | calibration · orientation · full GPS             |
| Zenmuse X7                | Super 35, interchangeable DL lens        | calibration · orientation · full GPS             |
| DJI XT2 / FC3682          | Sexagesimal GPS format (exif: namespace) | orientation · full GPS                           |
| Other DJI models          | Any Make=DJI or XMP drone-dji:           | orientation · full GPS · identification          |

>  Models without a registry entry fall back to 35mm_approx calibration (score 0.40). Registry entries yield score 0.80. XMP `CalibratedFocalLength` always takes priority (score 0.95).

------

### Parrot

*Detection: XMP `drone-parrot:` · Make = `PARROT`*

| Model / series      | Notes                                    | Features                                |
| ------------------- | ---------------------------------------- | --------------------------------------- |
| ANAFI               | 1/2.4" sensor, single-axis gimbal (tilt) | orientation · full GPS · identification |
| ANAFI Ai            | 4G, omnidirectional obstacle avoidance   | orientation · full GPS · identification |
| ANAFI USA / Thermal | Government / thermal variants            | orientation · full GPS · identification |

>  No calibration registry, no RTK. Single-axis gimbal: `camera_pitch` → `gimbal_pitch` when `gimbal_pitch` is absent.

------

### senseFly

*Detection: XMP `sensefly:` · Make = `SENSEFLY` · `Description:` namespace (Pix4D)*

| Model / series     | Notes                           | Features                                      |
| ------------------ | ------------------------------- | --------------------------------------------- |
| eBee X / eBee Plus | Fixed-wing, PPK/RTK, Pix4D tags | RTK · orientation · full GPS · identification |
| eBee Classic / SQ  | Fixed-wing, standard GPS        | orientation · full GPS · identification       |
| Aeria X            | Multi-sensor platform           | orientation · full GPS · identification       |

>  XMP tags under `Description:` namespace (Pix4D style). `FlightUUID` extracted. No calibration registry.

------

### Skydio

*Detection: XMP `skydio:` · `vehiclepositionned` (detected without EXIF Make)*

| Model / series | Notes                                     | Features                             |
| -------------- | ----------------------------------------- | ------------------------------------ |
| Skydio 2       | Model=`"2"` · Sony IMX577, 1/3.8", f3.7mm | calibration · orientation · full GPS |
| Skydio 2+      | Model=`"2+"` or `"[2+]"` · same sensor    | calibration · orientation · full GPS |
| Skydio X10     | VT300-Z 13mm · VT300-Z 50mm               | calibration · orientation · full GPS |

>  Built-in focal length sanity check (pre-2021 firmware stores normalized `CalibratedFocalLengthX`). Auto-corrected against actual `image_width`.

------

### Autel Robotics

*Detection: XMP `drone-autel:` · Make = `AUTEL`*

| Model / series          | Notes                          | Features                                |
| ----------------------- | ------------------------------ | --------------------------------------- |
| EVO II / EVO II Pro     | 8K, 1" sensor                  | orientation · full GPS · identification |
| EVO II Dual / Rugged    | Binocular, ruggedized variants | orientation · full GPS · identification |
| X-Star / X-Star Premium | Legacy lineup                  | full GPS · identification               |

>  XMP `drone-autel:` present only on some firmware versions. No calibration registry, no RTK.

------

### Yuneec

*Detection: Make = `YUNEEC` · Make = `XIRO` · model contains `CGO` / `TYPHOON` / `H520`*

| Model / series     | Notes                                 | Features       |
| ------------------ | ------------------------------------- | -------------- |
| Typhoon H / H Plus | CGO3+, hexacopter                     | identification |
| H520 / H520E       | Professional, interchangeable payload | identification |
| Q500 / Q500+       | CGO2 / CGO3                           | identification |
| Xiro Xplorer       | Make=`XIRO` or `XPLORER` in model     | identification |

>  Minimal extractor: camera family identification + basic calibration. No known proprietary XMP namespace, no RTK, no structured orientation.

------

### Xiaomi / FIMI

*Detection: Make = `XIAOMI` · Make = `BJ_XIAOMI` · model contains `YTXJ` / `FIMI` / `MJX`*

| Model / series          | Notes                       | Features                  |
| ----------------------- | --------------------------- | ------------------------- |
| FIMI X8 SE / X8 SE 2022 | `YTXJ` in EXIF model tag    | full GPS · identification |
| FIMI X8 Mini            | 250g class, `FIMI` in model | full GPS · identification |
| MJX Bugs series         | `MJX` in model              | identification            |

>  Minimal extractor: identification + basic calibration. No proprietary XMP namespace, no RTK, no structured orientation.

