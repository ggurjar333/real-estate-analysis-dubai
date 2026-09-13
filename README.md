# Rental Market Dynamics - Dubai

![Build Status](https://img.shields.io/github/actions/workflow/status/ggurjar333/rental-market-dynamics-dubai/build_and_deploy.yml?branch=main)
![License](https://img.shields.io/github/license/ggurjar333/rental-market-dynamics-dubai)
![Coverage](https://img.shields.io/codecov/c/github/ggurjar333/rental-market-dynamics-dubai)

Ejari rent transactions only — sourced from the configured `EJARI_URL` endpoint
(Rent Transaction Details). No sales, no carea, no legacy Pulse code.

## Features

- **Automated Data Extraction:** Paginated gateway rents fetch (`EjariRentsDownloader`).
- **Data Transformation:** Rents CSV → Parquet with canonical aliases (`RentsTransformer`).
- **Property Usage Analysis:** Generate detailed property usage reports.
- **Scrapy spider:** `rents` spider in `rents_scraper/` (same gateway endpoint).
- **Automated Releases:** Publish processed data via GitHub releases.
- **CI/CD Integration:** Built-in workflows to test and deploy changes.

## Prerequisites

- **Python:** 3.9 or higher
- **Make:** To execute build commands
- **pip:** Python package installer

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ggurjar333/rental-market-dynamics-dubai
    cd rental-market-dynamics-dubai
    ```

2. **Install dependencies**
    ```bash
    uv sync
    ```

3. **Create a ``.env`` file**

    Copy the provided example and update the values:
    ```bash
    cp .env.example .env
    ```
    `.env` needs only:
    ```bash
    EJARI_URL=your_ejari_endpoint_here
    ```

## Folder Structure
```bash
.
├── lib
│   ├── extract
│   │   └── ejari_rents_downloader.py   # POST EJARI_URL
│   ├── transform
│   │   └── rents_transformer.py        # rents CSV -> Parquet
│   ├── classes
│   ├── workspace
│   ├── config.py                       # rents config (EJARI_URL)
│   └── logging_helpers.py
├── rents_scraper
│   └── rents_scraper/spiders/rents.py  # Scrapy rents spider
├── output                              # rents_*.csv, rents_*.parquet
├── tests
├── run_etl_pipeline.py                 # EJARI_URL pipeline
├── .env.example
├── Makefile
├── README.md
└── requirements.txt
```

## Getting Started
- **ETL Pipeline:** 
    
    Run the complete pipeline (build, ETL, tests, and release publishing) with:
    ```bash
    make all
    ```
- **Testing:** 
    
    Run tests using:
    ```bash
    make test
    ```

## Usage Examples
- **Downloading & Transforming Data**:

    The ETL process downloads Ejari rents, transforms the data into Parquet format, and generates a property usage report. Logs are saved in ``etl.log``.
    ```bash
    make etl
    # or
    python run_etl_pipeline.py
    ```

- **Scrapy rents spider**:
    ```bash
    make scrapy-rents
    # or
    cd rents_scraper && uv run scrapy crawl rents -a from_date=09/12/2026 -a to_date=09/13/2026 -O ../output/rents.jsonl
    ```

- **Publishing Releases**:

    On successful processing, the data files are automatically published to a GitHub release.


## Historical Data
   Download the historical data from [releases](https://github.com/dataengineergaurav/rental-market-dynamics-dubai/releases

## Contributing
Contributions are welcome! Please review the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Licenses
This project is licensed under the terms of the [MIT License](https://mit-license.org/).

## Changelog
Refer to [CHANGELOG.md](changelog.md) for a complete history of changes.

## Contact
For questions or feedback, please open an issue on GitHub.




