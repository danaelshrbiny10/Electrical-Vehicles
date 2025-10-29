# ---------------------------------------------------------
# 🧭 Makefile for Electric Vehicles Data Project
# ---------------------------------------------------------
# Automates environment setup, data fetching, and cleanup
# ---------------------------------------------------------

# Environment variables
export PYTHONPATH := $(shell pwd)

# ---------------------------------------------------------
# 📦 Installation
# ---------------------------------------------------------
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# ---------------------------------------------------------
# ⚡ Fetch Data (default mode)
# ---------------------------------------------------------
fetch_data:
	@echo "⚡ Fetching EV charging station data from OpenChargeMap API..."
	python3 -m src.api.fetch_data

# ---------------------------------------------------------
# 🔁 Fetch Paginated Data (extended mode)
# ---------------------------------------------------------
fetch_paged_data:
	@echo "🌍 Fetching paginated EV data in multiple batches..."
	python3 -m src.api.fetch_data --paged

# ---------------------------------------------------------
# 🧹 Cleanup
# ---------------------------------------------------------
clean:
	@echo "🧹 Cleaning up raw data files..."
	rm -f data/raw/*.csv
	@echo "✅ Cleanup completed."
