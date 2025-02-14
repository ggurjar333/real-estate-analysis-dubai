# define variables
SOURCE_DIR := lib
TEST_DIR := tests
BUILD_DIR := build
TEMP_DIR := output

# default target
all: build etl clean test

clean:
	@echo "Clean ..."
	rm -rf $(BUILD_DIR)/*
	rm -rf $(SOURCE_DIR)/*.egg-info
	rm -rf $(SOURCE_DIR)/__pycache__
	rm -rf $(TEST_DIR)/__pycache__
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete
	rm -rf $(TEMP_DIR)/*.csv
	rm -rf $(TEMP_DIR)/*.parquet


build:
	@echo "Build ..."
	python --version
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install lib/

# extract the data
etl:
	@echo "ETL ..."
	python dubai_land_department.py

test:
	@echo "Test ..."
	pytest .

.PHONY: all