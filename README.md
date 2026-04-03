# Kampfraum

Open drone detection dataset aggregator. Kampfraum indexes every publicly available drone detection dataset (RF, acoustic, multimodal), normalizes them into a common schema, and serves a dashboard that makes the data explorable without downloading anything. The repo name is the German military doctrine term for battlespace. The project is open. The gap it documents is the business.

## Datasets

| Dataset | Sensor | Drone Models | Environment | Size | License | Source |
|---------|--------|-------------|-------------|------|---------|--------|
| DroneRF | RF | Parrot Bebop, Parrot AR, DJI Phantom | Lab | 40 GB | CC BY 4.0 | [Mendeley](https://dx.doi.org/10.17632/f4c2b4n755.1) |
| RFUAV | RF | 37 UAV types | Lab | 1.3 TB | Unknown | [GitHub](https://github.com/kitoweeknd/RFUAV) |
| DroneDetect | RF | 7 DJI/Parrot models | Lab | 3.5 GB | CC BY 4.0 | [IEEE](https://ieee-dataport.org/open-access/dronedetect-dataset-radio-frequency-dataset-unmanned-aerial-system-uas-signals-machine) |
| Zenodo RF/Video | Multimodal | DJI Phantom 4 | Field | 2.1 GB | CC BY 4.0 | [Zenodo](https://zenodo.org/record/4264467) |
| Acoustic Multiclass | Acoustic | 32 categories | Lab | TBD | Unknown | [arXiv](https://arxiv.org/abs/2509.04715) |

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
