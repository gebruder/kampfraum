#!/usr/bin/env python3
"""normalize.py — Convert fetched datasets into normalized Parquet format.

Output schema:
    timestamp       int64       unix ms, null if unavailable
    drone_model     string
    flight_mode     string      hovering / flying / on / off / recording
    sensor_type     string      rf / acoustic / visual
    signal_data     binary      serialized numpy array
    snr_db          float32     null if unavailable
    environment     string      lab / field / contested
    source_dataset  string      catalog id
"""

import json
import logging
import os
import sys
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("normalize")

SCHEMA = pa.schema([
    ("timestamp", pa.int64()),
    ("drone_model", pa.string()),
    ("flight_mode", pa.string()),
    ("sensor_type", pa.string()),
    ("signal_data", pa.binary()),
    ("snr_db", pa.float32()),
    ("environment", pa.string()),
    ("source_dataset", pa.string()),
])

ROOT = Path(__file__).resolve().parent.parent
DATASETS = ROOT / "datasets"
CATALOG = ROOT / "catalog.json"


def load_catalog():
    with open(CATALOG) as f:
        return json.load(f)["datasets"]


def serialize_array(arr: np.ndarray) -> bytes:
    """Serialize a numpy array to bytes."""
    buf = pa.allocate_buffer(arr.nbytes)
    pa.py_buffer(arr.tobytes())
    return arr.tobytes()


def null_reason(field: str, reason: str, dataset_id: str):
    log.warning("NULL %s in %s: %s", field, dataset_id, reason)


# --- DroneRF ---

def normalize_dronerf(max_rows: int = 0):
    """Normalize DroneRF CSV files.

    DroneRF file naming convention encodes metadata:
    Files contain RF power measurements across frequency bins.
    """
    dataset_id = "dronerf"
    src = DATASETS / "rf" / "dronerf"
    if not src.exists():
        log.info("DroneRF not fetched, skipping")
        return

    csv_files = sorted(src.glob("*.csv"))
    if not csv_files:
        log.warning("No CSV files found in %s", src)
        return

    rows = []
    # DroneRF filenames encode: drone type + flight mode
    mode_map = {
        "00000": "off",
        "00001": "on",
        "00010": "hovering",
        "00100": "flying",
        "01000": "recording",
        "10000": "on",
    }
    drone_map = {
        "bebop": "Parrot Bebop",
        "ar": "Parrot AR",
        "phantom": "DJI Phantom",
    }

    for csv_path in csv_files:
        fname = csv_path.stem.lower()

        # Determine drone model from filename
        drone_model = None
        for key, model in drone_map.items():
            if key in fname:
                drone_model = model
                break
        if drone_model is None:
            drone_model = "Unknown"
            null_reason("drone_model", f"could not parse from {csv_path.name}", dataset_id)

        # Determine flight mode
        flight_mode = None
        for key, mode in mode_map.items():
            if key in fname:
                flight_mode = mode
                break
        if flight_mode is None:
            flight_mode = "unknown"
            null_reason("flight_mode", f"could not parse from {csv_path.name}", dataset_id)

        try:
            import csv as csvmod
            with open(csv_path, "r") as f:
                reader = csvmod.reader(f)
                row_count = 0
                for line in reader:
                    if max_rows and row_count >= max_rows:
                        break
                    try:
                        signal = np.array([float(x) for x in line], dtype=np.float32)
                    except ValueError:
                        continue  # skip header or malformed rows
                    rows.append({
                        "timestamp": None,
                        "drone_model": drone_model,
                        "flight_mode": flight_mode,
                        "sensor_type": "rf",
                        "signal_data": serialize_array(signal),
                        "snr_db": None,
                        "environment": "lab",
                        "source_dataset": dataset_id,
                    })
                    row_count += 1
        except Exception as e:
            log.error("Error reading %s: %s", csv_path, e)

        if max_rows and len(rows) >= max_rows:
            break

    if not rows:
        log.warning("DroneRF: no rows produced")
        return

    null_reason("timestamp", "not available in DroneRF format", dataset_id)
    null_reason("snr_db", "not available in DroneRF format", dataset_id)
    _write_parquet(rows, "rf", dataset_id)


# --- RFUAV ---

def normalize_rfuav(max_rows: int = 0):
    """Normalize RFUAV dataset. Raw I/Q data."""
    dataset_id = "rfuav"
    src = DATASETS / "rf" / "rfuav"
    if not src.exists():
        log.info("RFUAV not fetched, skipping")
        return

    rows = []
    # Look for data files (may be .bin, .dat, .npy, .mat)
    data_files = sorted(
        f for f in src.rglob("*")
        if f.suffix in (".bin", ".dat", ".npy", ".mat", ".csv") and f.is_file()
    )

    if not data_files:
        log.warning("RFUAV: No data files found in %s — repo may contain only pointers", src)
        return

    for data_path in data_files:
        if max_rows and len(rows) >= max_rows:
            break

        # Extract drone model from directory name
        drone_model = data_path.parent.name if data_path.parent != src else "Unknown"

        try:
            if data_path.suffix == ".npy":
                arr = np.load(data_path, allow_pickle=False)
                if max_rows:
                    arr = arr[:max_rows]
                for i in range(len(arr)):
                    signal = arr[i].astype(np.float32) if arr[i].dtype != np.float32 else arr[i]
                    rows.append({
                        "timestamp": None,
                        "drone_model": drone_model,
                        "flight_mode": "unknown",
                        "sensor_type": "rf",
                        "signal_data": serialize_array(signal.flatten()),
                        "snr_db": None,
                        "environment": "lab",
                        "source_dataset": dataset_id,
                    })
                    if max_rows and len(rows) >= max_rows:
                        break
            else:
                # Binary / CSV — read raw and store
                raw = np.fromfile(data_path, dtype=np.float32, count=max_rows * 1024 if max_rows else -1)
                chunk_size = min(1024, len(raw))
                for i in range(0, len(raw), chunk_size):
                    if max_rows and len(rows) >= max_rows:
                        break
                    chunk = raw[i:i + chunk_size]
                    rows.append({
                        "timestamp": None,
                        "drone_model": drone_model,
                        "flight_mode": "unknown",
                        "sensor_type": "rf",
                        "signal_data": serialize_array(chunk),
                        "snr_db": None,
                        "environment": "lab",
                        "source_dataset": dataset_id,
                    })
        except Exception as e:
            log.error("Error reading %s: %s", data_path, e)

    if not rows:
        log.warning("RFUAV: no rows produced")
        return

    null_reason("timestamp", "not available in RFUAV format", dataset_id)
    null_reason("snr_db", "variable SNR — per-sample value not embedded in data files", dataset_id)
    null_reason("flight_mode", "not labeled in RFUAV data files", dataset_id)
    _write_parquet(rows, "rf", dataset_id)


# --- DroneDetect ---

def normalize_dronedetect(max_rows: int = 0):
    """Normalize DroneDetect .mat files."""
    dataset_id = "dronedetect"
    src = DATASETS / "rf" / "dronedetect"
    if not src.exists():
        log.info("DroneDetect not fetched, skipping")
        return

    try:
        from scipy.io import loadmat
    except ImportError:
        log.error("scipy required for DroneDetect .mat files: pip install scipy")
        return

    mat_files = sorted(src.glob("*.mat"))
    if not mat_files:
        log.warning("DroneDetect: No .mat files found in %s", src)
        return

    rows = []
    drone_map = {
        "mavicpro": "DJI Mavic Pro",
        "mavicair": "DJI Mavic Air",
        "phantom4": "DJI Phantom 4",
        "inspire1": "DJI Inspire 1",
        "matrice100": "DJI Matrice 100",
        "disco": "Parrot Disco",
        "bebop2": "Parrot Bebop 2",
    }

    for mat_path in mat_files:
        if max_rows and len(rows) >= max_rows:
            break

        fname = mat_path.stem.lower().replace(" ", "").replace("_", "").replace("-", "")
        drone_model = "Unknown"
        for key, model in drone_map.items():
            if key in fname:
                drone_model = model
                break

        try:
            data = loadmat(mat_path)
            # Find the main data variable (skip metadata keys)
            data_keys = [k for k in data.keys() if not k.startswith("__")]
            for key in data_keys:
                arr = data[key]
                if not isinstance(arr, np.ndarray):
                    continue
                n = min(len(arr), max_rows) if max_rows else len(arr)
                for i in range(n):
                    if max_rows and len(rows) >= max_rows:
                        break
                    signal = arr[i].astype(np.float32).flatten()
                    rows.append({
                        "timestamp": None,
                        "drone_model": drone_model,
                        "flight_mode": "unknown",
                        "sensor_type": "rf",
                        "signal_data": serialize_array(signal),
                        "snr_db": None,
                        "environment": "lab",
                        "source_dataset": dataset_id,
                    })
        except Exception as e:
            log.error("Error reading %s: %s", mat_path, e)

    if not rows:
        log.warning("DroneDetect: no rows produced")
        return

    null_reason("timestamp", "not available in DroneDetect format", dataset_id)
    null_reason("snr_db", "not embedded per-sample in DroneDetect .mat files", dataset_id)
    null_reason("flight_mode", "not labeled per-sample in DroneDetect", dataset_id)
    _write_parquet(rows, "rf", dataset_id)


# --- Zenodo RF/Video ---

def normalize_zenodo(max_rows: int = 0):
    """Normalize Zenodo RF/Video dataset."""
    dataset_id = "zenodo_rf_video"
    src = DATASETS / "multimodal" / "zenodo"
    if not src.exists():
        log.info("Zenodo RF/Video not fetched, skipping")
        return

    csv_files = sorted(src.glob("*.csv"))
    if not csv_files:
        log.warning("Zenodo: No CSV files found in %s", src)
        return

    rows = []
    for csv_path in csv_files:
        if max_rows and len(rows) >= max_rows:
            break
        try:
            import csv as csvmod
            with open(csv_path, "r") as f:
                reader = csvmod.DictReader(f)
                for i, line in enumerate(reader):
                    if max_rows and len(rows) >= max_rows:
                        break
                    # Try to extract signal data from available columns
                    signal_cols = [k for k in line.keys()
                                   if k not in ("timestamp", "label", "class", "drone", "mode")]
                    signal_vals = []
                    for col in signal_cols:
                        try:
                            signal_vals.append(float(line[col]))
                        except (ValueError, TypeError):
                            pass
                    signal = np.array(signal_vals, dtype=np.float32) if signal_vals else np.array([], dtype=np.float32)

                    ts = None
                    if "timestamp" in line:
                        try:
                            ts = int(float(line["timestamp"]) * 1000)
                        except (ValueError, TypeError):
                            null_reason("timestamp", f"unparseable value in {csv_path.name}", dataset_id)

                    rows.append({
                        "timestamp": ts,
                        "drone_model": line.get("drone", line.get("label", "DJI Phantom 4")),
                        "flight_mode": line.get("mode", "unknown"),
                        "sensor_type": "rf",
                        "signal_data": serialize_array(signal),
                        "snr_db": None,
                        "environment": "field",
                        "source_dataset": dataset_id,
                    })
        except Exception as e:
            log.error("Error reading %s: %s", csv_path, e)

    if not rows:
        log.warning("Zenodo: no rows produced")
        return

    null_reason("snr_db", "not available in Zenodo RF/Video dataset", dataset_id)
    _write_parquet(rows, "multimodal", dataset_id)


# --- Acoustic Multiclass ---

def normalize_acoustic(max_rows: int = 0):
    """Normalize acoustic multiclass dataset."""
    dataset_id = "acoustic_multiclass"
    src = DATASETS / "acoustic"
    if not src.exists():
        log.info("Acoustic multiclass not fetched, skipping")
        return

    # Look for .npy, .csv, or .wav files
    data_files = sorted(
        f for f in src.rglob("*")
        if f.suffix in (".npy", ".csv", ".wav", ".npz") and f.is_file()
        and ".fetched" not in f.name
    )

    if not data_files:
        log.warning("Acoustic multiclass: No data files found — dataset not yet available")
        return

    rows = []
    for data_path in data_files:
        if max_rows and len(rows) >= max_rows:
            break
        drone_model = data_path.parent.name if data_path.parent != src else "Unknown"
        try:
            if data_path.suffix == ".npy":
                arr = np.load(data_path, allow_pickle=False)
                n = min(len(arr), max_rows) if max_rows else len(arr)
                for i in range(n):
                    if max_rows and len(rows) >= max_rows:
                        break
                    signal = arr[i].astype(np.float32).flatten()
                    rows.append({
                        "timestamp": None,
                        "drone_model": drone_model,
                        "flight_mode": "unknown",
                        "sensor_type": "acoustic",
                        "signal_data": serialize_array(signal),
                        "snr_db": None,
                        "environment": "lab",
                        "source_dataset": dataset_id,
                    })
        except Exception as e:
            log.error("Error reading %s: %s", data_path, e)

    if not rows:
        log.warning("Acoustic multiclass: no rows produced")
        return

    null_reason("timestamp", "not available in acoustic dataset", dataset_id)
    null_reason("snr_db", "not available in acoustic dataset", dataset_id)
    null_reason("flight_mode", "not labeled in acoustic dataset", dataset_id)
    _write_parquet(rows, "acoustic", dataset_id)


def _write_parquet(rows: list[dict], sensor_type: str, dataset_id: str):
    """Write rows to a Parquet file with the normalized schema."""
    outdir = DATASETS / sensor_type
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f"{dataset_id}.parquet"

    table = pa.table({
        "timestamp": pa.array([r["timestamp"] for r in rows], type=pa.int64()),
        "drone_model": pa.array([r["drone_model"] for r in rows], type=pa.string()),
        "flight_mode": pa.array([r["flight_mode"] for r in rows], type=pa.string()),
        "sensor_type": pa.array([r["sensor_type"] for r in rows], type=pa.string()),
        "signal_data": pa.array([r["signal_data"] for r in rows], type=pa.binary()),
        "snr_db": pa.array([r["snr_db"] for r in rows], type=pa.float32()),
        "environment": pa.array([r["environment"] for r in rows], type=pa.string()),
        "source_dataset": pa.array([r["source_dataset"] for r in rows], type=pa.string()),
    }, schema=SCHEMA)

    pq.write_table(table, outpath)
    log.info("Wrote %d rows to %s", len(rows), outpath)


def main():
    max_rows = int(os.environ.get("NORMALIZE_MAX_ROWS", "0"))
    if max_rows:
        log.info("Limiting to %d rows per dataset (sample mode)", max_rows)

    normalize_dronerf(max_rows)
    normalize_rfuav(max_rows)
    normalize_dronedetect(max_rows)
    normalize_zenodo(max_rows)
    normalize_acoustic(max_rows)

    log.info("Normalization complete.")


if __name__ == "__main__":
    main()
