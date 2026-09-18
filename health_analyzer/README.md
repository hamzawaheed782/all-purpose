# Health Issue Analyzer

A Python-based health symptom analysis tool powered by the Gemini API.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
export GEMINI_API_KEY="your_key_here"
python app.py
```

Then open http://localhost:7860 in your browser.

## Features

- Enter symptoms (one per line) with optional age and duration
- Get structured analysis from Gemini 3.6 Flash
- JSON-formatted response with severity, possible causes, recommendations
- Built-in disclaimer reminding users to consult a professional

## Disclaimer

This tool is for informational purposes only and is NOT a substitute for professional medical advice.
