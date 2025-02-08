pip install -e ".[dev]"

# Real Estate Analysis Dubai

This repository contains the code and data for analyzing real estate properties in Dubai.

## Prerequisites

- Python 3.8+
- pip
- MongoDB

## Folder Structure

The folder structure of this project is as follows:

- `src/`: This folder contains the source code for the analysis.
- `tests/`: This folder contains the unit tests for the code.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository: `git clone https://github.com/ggurjar333/real-estate-analysis-dubai.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up your environment variables in the `.env` file. You will need to provide values for `URL`, `MONGO_DATABASE_URI`, and `MONGO_DATABASE_NAME`.

## Usage

To extract data, run the `extract.py` script in the `src/` directory:

```sh
python lib/extract.py
``````

This script, `analysis.py`, performs feature engineering on the extracted real estate data. It adds new features that can be useful for further analysis or machine learning models.
```sh
python lib/analysis.py
```
The script adds the following features to the data:

- `price_range`: This is a categorical feature derived from the `price` feature. It categorizes the price into four ranges: '0-100k', '100k-200k', '200k-300k', and '300k+'.
- `price_per_sqft`: This is a numerical feature calculated by dividing the `price` by the `area_square_feet`.
- `bed_bath_ratio`: This is a numerical feature calculated by dividing the number of `bedrooms` by the number of `bathrooms`.
- `total_rooms`: This is a numerical feature calculated by adding the number of `bedrooms` and `bathrooms`.

To run the script, use the following command:

```sh
python analysis.py