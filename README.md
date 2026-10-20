# TerraSignal AI 🌍🔥

**A machine learning project for geospatial wildfire risk analysis and satellite-based fire detection forecasting.**

TerraSignal AI explores how satellite observations and environmental data can be combined to estimate the likelihood of fire detections in specific geographic areas over a future time window.

The project starts with **Tunisia** as its initial study region, with the long-term goal of expanding to North Africa and the Mediterranean.

> **Project status:** Early development. Data collection, validation, and baseline experiments are the initial priorities. Predictive performance and operational usefulness have not yet been established.

---

## 🎯 Objectives

- Collect and validate satellite-based fire detection data.
- Build a reproducible geospatial data processing pipeline.
- Engineer spatial, temporal, and environmental features.
- Establish a historical-frequency baseline before introducing more complex models.
- Train and evaluate an XGBoost model using leakage-aware temporal validation.
- Investigate class imbalance, observation bias, and probability calibration.
- Visualize fire detections and model-estimated risk across geographic regions.
- Develop a maintainable ML pipeline that can eventually be deployed as an API.

---

## 🗺️ Initial Scope

| Component                  | Initial approach                                            |
| -------------------------- | ----------------------------------------------------------- |
| Study region               | Tunisia                                                     |
| Historical data            | Start with one complete year; expand to multiple years      |
| Satellite observations     | NASA FIRMS VIIRS 375 m active fire data                     |
| Initial spatial resolution | 0.25° geographic grid                                       |
| Prediction target          | Satellite-detected fire during the next 24 hours            |
| Baseline                   | Historical detection frequency                              |
| Machine learning model     | XGBoost                                                     |
| Evaluation                 | Temporal validation, PR-AUC, precision, recall, calibration |
| Visualization              | Geographic maps and temporal analysis                       |

The spatial and temporal resolutions are starting hypotheses. They may change based on data quality, observation coverage, and experimental results.

---

## 📡 Data Sources

### 1. NASA FIRMS — Active Fire Detections

[Fire Information for Resource Management System (FIRMS)](https://firms.modaps.eosdis.nasa.gov/)

FIRMS provides satellite-derived active fire observations from the VIIRS instrument at 375 m resolution.

Planned uses:
- Explore the spatial and temporal distribution of fire detections.
- Aggregate observations into geographic grid cells and daily time windows.
- Investigate detection confidence, duplicate observations, and data quality.

### 2. ERA5-Land — Environmental Weather Data

[ERA5-Land dataset](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land)

Potential features include temperature, precipitation, wind-related variables, and soil moisture.

**Important:** ERA5-Land is a reanalysis dataset, not a future weather forecast. Features must respect the prediction cutoff to avoid leakage. An operational system would require actual weather forecasts.

### 3. MODIS Land Cover

[MODIS MCD12Q1](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD12Q1)

Used to characterize vegetation and land-cover types: forests, shrublands, croplands, and other categories.

---

## 🧠 Methodology

### Step 1 — Data Collection and Validation
Download a manageable FIRMS sample, inspect the schema, validate coordinates and dates, and investigate duplicate records and detection confidence. Original files are preserved; processed data is stored separately.

### Step 2 — Exploratory Data Analysis
Analyze detection counts over time, seasonal patterns, geographic hotspots, and relationships between detection characteristics and environmental variables.

### Step 3 — Geospatial Aggregation
Map individual detections to a 0.25° geographic grid. The initial target is whether a grid cell contains at least one qualifying satellite fire detection during the following 24 hours — representing **observed satellite fire activity**, not necessarily a new wildfire ignition.

### Step 4 — Label Quality
A key challenge is that **no detection does not always mean no fire**. Cloud cover, satellite sampling, and detection limits can all affect observation. The project will distinguish:
- Positive observations with qualifying fire detections.
- Credible negatives with sufficient observation evidence.
- Unknown/unreliable cases that should be excluded from training.

### Step 5 — Feature Engineering
Candidate features include recent fire detection history, seasonal/calendar variables, historical environmental conditions (pre-cutoff), land-cover characteristics, and terrain features. All features are checked for missingness, temporal alignment, and leakage.

### Step 6 — Baseline and Machine Learning
A historical-frequency baseline is built first. XGBoost is then evaluated to determine whether environmental and temporal features provide meaningful predictive improvement. More complex architectures are considered only if experiments provide a clear reason.

### Step 7 — Evaluation
- **PR-AUC** for performance under class imbalance.
- **Precision and recall** for the false-alarm / missed-detection trade-off.
- **Probability calibration** to verify predicted probabilities match observed frequencies.
- **Temporal generalization** on periods not used for training.
- **Regional and seasonal analysis** for performance variation.

---

## 🛠️ Technology Stack

| Area                | Technologies                             |
| ------------------- | ---------------------------------------- |
| Language            | Python 3.11                              |
| Data processing     | pandas, NumPy                            |
| Data storage        | Parquet                                  |
| Analytical queries  | DuckDB                                   |
| Machine learning    | scikit-learn, XGBoost                    |
| Visualization       | Matplotlib, geospatial mapping libraries |
| Testing             | pytest                                   |
| Experiment tracking | MLflow — planned                         |
| API                 | FastAPI — planned                        |
| Containerization    | Docker — planned                         |
| Version control     | Git and GitHub                           |

---

## 🏗️ Architecture

```text
NASA FIRMS + Environmental Data
              │
              ▼
     Data Ingestion Layer
              │
              ▼
   Validation and Quality Checks
              │
              ▼
   Geospatial and Temporal ETL
              │
              ▼
     Parquet + DuckDB Storage
              │
              ▼
       Feature Engineering
              │
              ▼
  Frequency Baseline / XGBoost
              │
              ▼
 Leakage-Aware Model Evaluation
              │
              ▼
     Maps, Reports and API
```

---

## 📁 Repository Structure

```text
terrasignal-ai/
├── configs/
│   └── baseline.yaml          # Experiment configuration
├── data/
│   ├── raw/                   # Original, unmodified source files
│   ├── interim/               # Cleaned, pre-aggregation data
│   └── processed/             # Model-ready features and labels
├── notebooks/
│   └── 01_explore_firms.ipynb # Initial EDA notebook
├── reports/
│   └── figures/               # Generated maps and charts
├── scripts/
│   └── inspect_firms.py       # CLI: validate a raw FIRMS CSV
├── src/
│   └── terrasignal/
│       ├── data/
│       │   ├── firms.py       # FIRMS loader and aggregation
│       │   └── validation.py  # Data quality checks
│       ├── features/
│       │   └── build.py       # Feature engineering pipeline
│       ├── models/
│       │   ├── baseline.py    # Historical-frequency baseline
│       │   └── train.py       # XGBoost training pipeline
│       ├── evaluation/
│       │   └── metrics.py     # PR-AUC, calibration, temporal eval
│       └── api/
│           └── main.py        # FastAPI application (planned)
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11
- Git
- A NASA FIRMS data download or API key ([register here](https://firms.modaps.eosdis.nasa.gov/api/area/))

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/terrasignal-ai.git
cd terrasignal-ai
```

**Windows PowerShell:**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Set the Python source path (Windows PowerShell):
```powershell
$env:PYTHONPATH = "src"
```

Run the initial data inspection script after placing a FIRMS CSV in `data/raw/`:
```bash
python scripts/inspect_firms.py --file data/raw/your_firms_file.csv
```

Run tests:
```bash
pytest -q
```

---

## 📈 Development Roadmap

- [ ] Create the repository and development environment.
- [ ] Download a small, documented FIRMS sample for Tunisia.
- [ ] Implement and test the satellite data loader.
- [ ] Produce a data-quality report and exploratory visualizations.
- [ ] Define the spatial grid and daily aggregation logic.
- [ ] Investigate observation coverage and negative-label reliability.
- [ ] Build a reproducible historical-frequency baseline.
- [ ] Implement leakage-aware temporal evaluation.
- [ ] Integrate environmental data and engineer features.
- [ ] Train and evaluate XGBoost against the baseline.
- [ ] Analyze calibration and geographic/seasonal performance.
- [ ] Add MLflow experiment tracking.
- [ ] Package the pipeline and expose predictions through FastAPI.
- [ ] Containerize the application with Docker.
- [ ] Explore population exposure and expand the study region.

---

## ⚠️ Limitations and Responsible Use

TerraSignal AI is a research and engineering project, **not an operational wildfire warning system**.

- Satellite detections are imperfect observations of fire activity.
- Historical associations do not guarantee future predictive performance.
- Reanalysis data must not be mistaken for information available in a real-time forecast.
- Model probabilities require calibration and independent evaluation before any operational use.
- Both false negatives and false positives can have serious consequences.

Any future public-facing risk map must communicate uncertainty and should not replace official warnings or emergency-management decisions.

---

## 📚 References

- [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/)
- [ERA5-Land](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land)
- [MODIS MCD12Q1 Land Cover](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD12Q1)

---

*Built as a learning and research project in machine learning, geospatial data engineering, and environmental risk analysis.*
