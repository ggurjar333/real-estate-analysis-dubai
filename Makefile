# define variables
SOURCE_DIR := lib
TEST_DIR := tests
BUILD_DIR := build

# default target
all: build extract

#clean:
#	@echo "Clean ..."
#	rm -rf $(BUILD_DIR)/*
#	rm -rf $(SOURCE_DIR)/*.egg-info
#	rm -rf $(SOURCE_DIR)/__pycache__
#	rm -rf $(TEST_DIR)/__pycache__
#	find . -type f -name '*.pyc' -delete
#	find . -type f -name '*.pyo' -delete
#	find . -type f -name '*~' -delete


build:
	@echo "Build ..."
	python --version
	pip install -r requirements.txt
	cd lib
	pip install .
	cd ..

# extract the data
extract:
	@echo "Extract ..."
	python dubai_land_department.py

test:
	@echo "Test ..."
	pytest .

.PHONY: all extract