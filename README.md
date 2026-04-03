# Kampfraum

Open drone detection dataset aggregator. Kampfraum indexes every publicly available drone detection dataset (RF, acoustic, multimodal), normalizes them into a common schema, and serves a dashboard that makes the data explorable without downloading anything. The repo name is the German military doctrine term for battlespace. The project is open. The gap it documents is the business.

## Datasets

### RF

| Dataset | Drone Models | Environment | Size | License | Source |
|---------|-------------|-------------|------|---------|--------|
| DroneRF | Parrot Bebop, Parrot AR, DJI Phantom | Lab | 40 GB | CC BY 4.0 | [Mendeley](https://dx.doi.org/10.17632/f4c2b4n755.1) |
| RFUAV | 37 UAV types | Lab | 1.3 TB | Unknown | [GitHub](https://github.com/kitoweeknd/RFUAV) |
| DroneDetect | 7 DJI/Parrot models | Lab | 3.5 GB | CC BY 4.0 | [IEEE](https://ieee-dataport.org/open-access/dronedetect-dataset-radio-frequency-dataset-unmanned-aerial-system-uas-signals-machine) |
| CardRF | 5 DJI + Beebeerun | Field | 65 GB | CC BY 4.0 | [IEEE](https://ieee-dataport.org/documents/cardinal-rf-cardrf-outdoor-uavuasdrone-rf-signals-bluetooth-and-wifi-signals-dataset) |
| Drone RC RF Signals | 17 RCs, 8 manufacturers | Lab | 124 GB | CC BY 4.0 | [IEEE](https://ieee-dataport.org/open-access/drone-remote-controller-rf-signal-dataset) |
| DroneRFb-Spectra | 7 brands (DJI, FrSky, Futaba...) | Field | 5.5 GB | CC BY 4.0 | [IEEE](https://ieee-dataport.org/documents/dronerfb-spectra-rf-spectrogram-dataset-drone-recognition) |
| CageDroneRF | 23 models, 39 classes | Lab | 500 GB | Unknown | [arXiv](https://arxiv.org/abs/2601.03302) |
| DRFF-R2 | 26 units, 8 models | Field | TBD | CC BY 4.0 | [arXiv](https://arxiv.org/abs/2603.00106) |
| Noisy Drone RF | 6 consumer drones | Lab | TBD | Unknown | [Kaggle](https://www.kaggle.com/datasets/sgluege/noisy-drone-rf-signal-classification-v2) |
| KU Leuven Drone RF | Multiple | Lab | TBD | Unknown | [KU Leuven](https://rdr.kuleuven.be/dataset.xhtml?persistentId=doi:10.48804/HZRVNZ) |
| AirID | DJI Matrice M100 | Lab | TBD | Research | [GENESYS](https://genesys-lab.org/airid) |
| Hovering UAVs RF | 7x DJI M100 | Lab | 4.5 GB | Research | [GENESYS](https://genesys-lab.org/hovering-uavs) |

### Acoustic

| Dataset | Drone Models | Environment | Size | License | Source |
|---------|-------------|-------------|------|---------|--------|
| Acoustic Multiclass | 32 categories | Lab | TBD | Unknown | [arXiv](https://arxiv.org/abs/2509.04715) |
| Drone Audio Detection Samples | Multiple | Field | TBD | Unknown | [HuggingFace](https://huggingface.co/datasets/geronimobasso/drone-audio-detection-samples) |
| DroneAudioset | Multiple types/throttles | Field | TBD | MIT | [HuggingFace](https://huggingface.co/datasets/ahlab-drone-project/DroneAudioSet) |
| DREGON | Quadrotor | Field | TBD | Research | [Inria](https://dregon.inria.fr/datasets/dregon/) |
| SPCup19 Egonoise | Quadrotor | Field | TBD | Research | [Inria](https://dregon.inria.fr/datasets/signal-processing-cup-2019/) |
| UaVirBASE | Multiple UAVs | Lab | TBD | Unknown | [Zenodo](https://zenodo.org/records/15391924) |
| DroneAudioDataset | Propellers (indoor) | Lab | TBD | Unknown | [GitHub](https://github.com/saraalemadi/DroneAudioDataset) |

### Visual

| Dataset | Drone Models | Environment | Size | License | Source |
|---------|-------------|-------------|------|---------|--------|
| Anti-UAV | Multiple | Field | TBD | Research | [GitHub](https://github.com/ZhaoJ9014/Anti-UAV) |
| Anti-UAV410 | Multiple | Field | TBD | Research | [GitHub](https://github.com/HwangBo94/Anti-UAV410) |
| CST Anti-UAV | Tiny UAVs | Field | TBD | Unknown | [arXiv](https://arxiv.org/abs/2507.23473) |
| HIT-UAV | Thermal IR (persons/vehicles) | Field | TBD | CC BY 4.0 | [Kaggle](https://www.kaggle.com/datasets/pandrii000/hituav-a-highaltitude-infrared-thermal-dataset) |
| VisioDECT | 6 UAV models | Field | TBD | Unknown | [IEEE](https://ieee-dataport.org/documents/visiodect-dataset-aerial-dataset-scenario-based-multi-drone-detection-and-identification) |
| SynDroneVision | Synthetic models | Lab | 900 GB | Unknown | [Zenodo](https://zenodo.org/records/13360116) |
| Seraphim | 23 merged source datasets | Field | TBD | CC BY 4.0 | [HuggingFace](https://huggingface.co/datasets/lgrzybowski/seraphim-drone-detection-dataset) |
| Drone vs Bird (YOLO) | Drones + birds | Field | TBD | CC BY 4.0 | [Mendeley](https://data.mendeley.com/datasets/6ghdz52pd7/3) |
| Drone vs Bird Challenge | Drones + birds | Field | TBD | Research | [GitHub](https://github.com/wosdetc/challenge) |
| VisDrone | Aerial (pedestrians, vehicles) | Field | TBD | Research | [GitHub](https://github.com/VisDrone/VisDrone-Dataset) |
| UAVSwarm | 19+ types in swarms | Field | TBD | Unknown | [MDPI](https://www.mdpi.com/2072-4292/14/11/2601) |
| Det-Fly | UAV targets from DJI Mavic 2 | Field | TBD | Unknown | [GitHub](https://github.com/Jake-WU/Det-Fly) |
| DUT Anti-UAV | 35 UAV types | Field | TBD | MIT | [GitHub](https://github.com/wangdongdut/DUT-Anti-UAV) |
| Drone Dataset (UAV) | Mixed consumer drones | Field | TBD | Unknown | [Kaggle](https://www.kaggle.com/datasets/dasmehdixtr/drone-dataset-uav) |

### Multimodal

| Dataset | Sensor Types | Environment | Size | License | Source |
|---------|-------------|-------------|------|---------|--------|
| Zenodo RF/Video | RF + video | Field | 2.1 GB | CC BY 4.0 | [Zenodo](https://zenodo.org/record/4264467) |
| Multi-Sensor IR/Visible/Audio | IR + visible + audio | Field | TBD | CC0 1.0 | [GitHub](https://github.com/DroneDetectionThesis/Drone-detection-dataset) |
| Multi-Sensor Radar/RF | FMCW + CW radar + RF | Lab | TBD | Unknown | [Nature](https://www.nature.com/articles/s41597-026-06802-6) |
| TMRGBT-D2D | RGB + thermal | Field | TBD | Unknown | [MDPI](https://www.mdpi.com/2504-446X/9/10/694) |
| M3OT | RGB + IR | Field | TBD | Unknown | [Nature](https://www.nature.com/articles/s41597-025-06204-0) |
| Cyber-Physical Swarm | Network + telemetry | Field | TBD | Unknown | [IEEE](https://ieee-dataport.org/documents/cyber-physical-dataset-drone-swarms-coordinated-formations) |
| UAVScenes | LiDAR + camera | Field | TBD | Unknown | [GitHub](https://github.com/sijieaaa/UAVScenes) |

## Normalized Schema

All datasets are converted to Parquet with the following schema:

| Field | Type | Notes |
|-------|------|-------|
| `timestamp` | int64 | Unix ms, null if unavailable |
| `drone_model` | string | |
| `flight_mode` | string | hovering / flying / on / off / recording |
| `sensor_type` | string | rf / acoustic / visual |
| `signal_data` | binary | Serialized numpy array (RF: I/Q or amplitude; acoustic: MFCC) |
| `snr_db` | float32 | Null if unavailable |
| `environment` | string | lab / field / contested |
| `source_dataset` | string | Catalog ID |

## Public Data / Öffentliche Daten

Kampfraum collects publicly available data into an easier interface. It does not have private battlespace: EW-contested environments, fiber-optic FPV drones, Shahed/Geran acoustic signatures, and operationally labeled flight data.

Kampfraum sammelt offen verfügbare Daten in einer einfacheren Oberfläche. Es enthält keinen privaten Kampfraum: EW-belastete Umgebungen, Glasfaser-FPV-Drohnen, akustische Signaturen von Shahed/Geran und operativ gekennzeichnete Flugdaten.

## Contributing

To add a dataset:

1. Add an entry to `catalog.json` with all required fields
2. Write a fetch script in `scripts/` following the pattern of existing scripts
3. If the dataset has a known format, add a normalizer function in `scripts/normalize.py`
4. Open a PR

## Dashboard

Live at [gebruder.ottenheimer.app/kampfraum](https://gebruder.ottenheimer.app/kampfraum)

---

[Gebrüder Ottenheimer](https://gebruder.ottenheimer.app)
