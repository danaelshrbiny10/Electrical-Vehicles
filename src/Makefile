# ---------------------------------------------------------
# Makefile for Electric Vehicles Data Project
# ---------------------------------------------------------

# Environment variables
export PYTHONPATH := $(shell pwd)

# Targets
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

fetch-data:
	@echo "⚡ Fetching EV charging station data from OpenChargeMap API..."
	python3 src/api/fetch_data.py

clean:
	@echo "🧹 Cleaning up raw data..."
	rm -f data/raw/*.csv
