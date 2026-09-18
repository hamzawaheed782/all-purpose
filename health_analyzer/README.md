# Health Issue Analyzer

A comprehensive Python-based health symptom analysis tool powered by the Gemini API.

## Features

- **Multi-symptom analysis** with category classification and weighted severity scoring
- **Emergency red-flag detection** with immediate alerts for critical symptoms
- **Persistent session history** with JSON-based storage
- **Longitudinal symptom tracking** with interactive Plotly charts
- **Export functionality** (PDF and Markdown reports)
- **Tabbed Gradio UI** (Assessment, History & Trends, Emergency Guidelines, Export)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
export GEMINI_API_KEY=*** GEMINI_API_KEY /home/ubuntu/.hermes/.env | grep -v "^#" | cut -d= -f2)
python app.py
```

Then open http://localhost:7860 in your browser.

## Architecture

- `app.py` — Gradio web UI with 4 tabs
- `gemini_client.py` — Gemini 3.6 Flash API integration
- `config.py` — Configuration
- `symptom_data.py` — Health categories, symptoms, red-flag definitions
- `emergency_detector.py` — Red-flag detection engine
- `storage_manager.py` — JSON-based session persistence
- `analytics.py` — Plotly chart generation
- `report_generator.py` — PDF and Markdown report generation

## Disclaimer

This tool is for informational purposes only and is NOT a substitute for professional medical advice.
