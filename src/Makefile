# ---------------------------------------------------------
# 🧭 Makefile for Electric Vehicles Data Project
# ---------------------------------------------------------
# Automates environment setup, data fetching, ML pipeline, Docker, and cleanup
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
# 🐳 Docker
# ---------------------------------------------------------
docker_build:
	@echo "🐳 Building Docker image..."
	docker compose build

docker_up:
	@echo "🚀 Starting Docker containers..."
	docker compose up -d

docker_down:
	@echo "🛑 Stopping Docker containers..."
	docker compose down

# ---------------------------------------------------------
# 🤖 Machine Learning
# ---------------------------------------------------------
train_ml:
	@echo "🤖 Training ML models..."
	python3 -m src.pipelines.train_all

# ---------------------------------------------------------
# 🧹 Cleanup
# ---------------------------------------------------------
clean:
	@echo "🧹 Cleaning up raw data files..."
	rm -f data/raw/*.csv
	@echo "✅ Cleanup completed."
