# dm_extract ( *drone metadata extract* ) ![Français](https://flagcdn.com/w40/fr.png)

![Langage](https://img.shields.io/badge/langage-C-blue.svg)

>  Extraction de métadonnées d'images de drone en ligne de commande.

`dm_extract` est un outil CLI pour extraire les métadonnées EXIF, XMP et GPS des images JPG de drones.  
Il produit une sortie structurée et prête à l'emploi dans plusieurs formats — conçu pour l'intégration dans les flux de travail de géomatique et de photogrammétrie.

---

## Fonctionnalités

* 📷 Analyse les métadonnées EXIF / XMP des images JPEG de drones  (fichier unique ou par lot)

* 📍 Extrait les coordonnées GPS, altitude, angles de nacelle et focale calibrée

* 📤 Exporte format CSV et GeoJSON

* ⚡ Rapide, scriptable, adapté aux pipelines

* 100 % écrit en C

* Fonctionne sous Windows, Linux et macOS

* **Bonus :** Interface Python

---

## Utilisation

##### Syntaxe

```bash
dm_extract [options] FICHIER [FICHIER ...]
```

Au moins un fichier doit être fourni. Les jokers sont acceptés.

##### Options

| Option    | Forme longue    | Description                                             |
| --------- | --------------- | ------------------------------------------------------- |
| `-o FILE` | `--output FILE` | Fichier de sortie. Par défaut : stdout                  |
| `-g`      | `--geojson`     | Format de sortie GeoJSON. Par défaut : CSV              |
| `-n`      | `--no-header`   | Omet la ligne d'en-tête CSV                             |
| `-r`      | `--raw`         | Mode diagnostic : dump EXIF/XMP brut + résumé structuré |
| `-q`      | `--quiet`       | Supprime les messages de progression sur stderr         |
| `-j N`    | `--jobs N`      | Nombre de threads (2, 4, 6 or 8).                       |
| `-V`      | `--version`     | Affiche la version et quitte                            |
| `-h`      | `--help`        | Affiche l'aide et quitte                                |

***Options Multithread:***
  - Par défaut : sélection automatique en fonction de la RAM disponible.
  - Utilisez -j 1 pour forcer le mode séquentiel.
  - Ignoré avec l'option --raw (toujours séquentiel).

##### Codes de sortie

| Code | Signification                                                        |
| ---- | -------------------------------------------------------------------- |
| `0`  | Succès — tous les fichiers ont été traités                           |
| `1`  | Au moins un fichier en erreur (lecture, format non reconnu)          |
| `2`  | Erreur d'arguments (option inconnue, fichier de sortie inaccessible) |

##### Fichier unique

```bash
# Linux / macOS
./dm_extract DJI_0001.JPG

# Windows
dm_extract.exe DJI_0001.JPG
```

Voir [binaires](https://github.com/Aero-Forger/DM_Extract/blob/main/binaries.md) pour plus de détails

---

### Interface graphique Python de test

https://github.com/Aero-Forger/DM_Extract/blob/main/dm_extract_gui_en.py

Outil Python rapide pour tester `dm_extract` graphiquement.  
L'utilisation du binaire statique est <mark>préférée </mark>pour pouvoir faire des scripts ou s'intégrer dans un flux de precessus externe.  
L'interface graphique ne le permet pas.

:warning: la GUI Python est un simpe outil de test qui **ne fait pas partie du code** de `dm_extract` 

---

### Sortie :

[CSV_sample](https://github.com/Aero-Forger/DM_Extract/blob/main/CSV_sample.md)

---

### Limitations

- Seuls les fichiers **JPEG** (`.jpg`, `.JPG`) sont pris en charge. Les formats RAW (DNG, CR2, NEF) ne le sont pas encore.

- La taille maximale de scan par fichier est de **512 Ko** (les blocs EXIF + XMP d'un drone tiennent dans les 128 premiers Ko).

- Le traitement est **séquentiel** (un fichier à la fois) avec **-- raw**

- En mode GeoJSON, les images sans GPS valide sont exclues sans message d'avertissement (utilisez `--raw` pour diagnostiquer).

---

## Cas d'utilisation

- Construire des journaux de vol à partir d'un ensemble d'images drone

- Alimenter directement des coordonnées dans QGIS, GDAL ou tout outil SIG

- Pré-traiter des ensembles d'images avant pipelines de photogrammétrie (Metashape, ODM...)

- Vérifier la couverture GPS avant traitement

## Drones pris en charge :

7 marques détectées automatiquement : **DJI**, **Parrot**, **senseFly**, **Skydio**, **Autel Robotics**, **Yuneec**, **Xiaomi**.

[Drones](https://github.com/Aero-Forger/DM_Extract/blob/main/SUPPORTED_DRONES.md)

---

## Fait partie de l'écosystème Aeroforger

`dm_extract` est un outil open-source maintenu dans le cadre du projet [Aeroforger](https://github.com/Aero-Forger) — une collection d'outils pour le traitement de données drone, la photogrammétrie et la géomatique.

Soutenez le projet sur [Patreon](https://www.patreon.com/Aeroforger).

---

## Licence

**LGPL v3**
