# 🏥 MedGemma Guardian

> **Privacy-Preserving Clinical Decision Support & Safety Auditing**

[![MedGemma Impact Challenge](https://img.shields.io/badge/Kaggle-MedGemma%20Impact%20Challenge-20BEFF?logo=kaggle)](https://kaggle.com/competitions/med-gemma-impact-challenge)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange)](LICENSE)

## 🎯 Overview

**MedGemma Guardian** is an AI-powered clinical safety agent designed to reduce prescription errors and improve patient safety. Built on Google's **MedGemma** (HAI-DEF) model, it performs automated Medical Document Understanding (MDU) with real-time safety auditing.

### Key Features

- 🔒 **Privacy-First**: Local execution ensures patient data never leaves the hospital
- 🧮 **Mathematical Auditing**: Chain-of-Thought prompting for accurate dosage calculations
- ⚠️ **Risk Detection**: Real-time alerts for overdose risks (e.g., Acetaminophen > 4000mg/day)
- 📋 **FHIR Compatible**: Structured JSON output for healthcare interoperability
- 👨‍⚕️ **Human-in-the-Loop**: Empowers clinicians with transparent safety audits

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- 4GB+ VRAM (for quantized model)
- Google API Key (for MedGemma access)

### Installation

```bash
# Clone the repository
git clone https://github.com/cleniooliveiramoura/MedGemma-Guardian.git
cd MedGemma-Guardian

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY

# Run the application
uvicorn app.main:app --reload
```

### Access the Application

Open your browser at: `http://localhost:8000`

## 📁 Project Structure

```
MedGemma/
├── app/                    # Backend (FastAPI)
│   ├── main.py            # API endpoints
│   ├── engine.py          # MedGemma integration
│   └── __init__.py
├── web/                    # Frontend (Vanilla JS)
│   ├── index.html
│   ├── index.css
│   └── main.js
├── notebook/               # Kaggle submission
│   └── kaggle_submission.py
├── data/                   # Sample clinical data
├── scripts/                # Utility scripts
├── KAGGLE_SUBMISSION_REPORT.md
├── RELATORIO_TECNICO_FINAL_PT.md
└── IMPLEMENTATION_PLAN.md
```

## 🧪 Demo Case: Acetaminophen Toxicity Prevention

The system detects dangerous prescriptions like:

```
Patient: "Take 10 tablets of 500mg Acetaminophen daily"
```

**MedGemma Guardian Response:**
```json
{
  "medication": "Acetaminophen",
  "daily_dose": 5000,
  "max_safe_dose": 4000,
  "risk_level": "CRITICAL",
  "reasoning": "500mg × 10 = 5000mg (exceeds 4000mg/day limit → hepatotoxicity risk)"
}
```

## 🏗️ Technical Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Clinical      │────▶│   FastAPI       │────▶│   MedGemma      │
│   Document      │     │   Backend       │     │   (HAI-DEF)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                                ▼
                 ┌─────────────────────────────┐
                 │   Chain-of-Thought Audit    │
                 │   • Entity Extraction       │
                 │   • Dosage Calculation      │
                 │   • Risk Classification     │
                 └─────────────────────────────┘
                                │
                                ▼
                 ┌─────────────────────────────┐
                 │   Glassmorphism UI          │
                 │   • Safety Alerts           │
                 │   • Protocol Viewer         │
                 │   • Human-in-the-Loop       │
                 └─────────────────────────────┘
```

## 👨‍💻 Team

- **Clenio Afonso de Oliveira Moura** — *Data Scientist & AI Engineer*
  - Lead Developer | Full-stack implementation | MedGemma integration
  - GitHub: [@cleniooliveiramoura](https://github.com/cleniooliveiramoura)

## 📚 References

Fereshteh Mahvar, Yun Liu, Daniel Golden, Fayaz Jamil, Sunny Jansen, Can Kirmizi, Rory Pilgrim, David F. Steiner, Andrew Sellergren, Richa Tiwari, Sunny Virmani, Liron Yatziv, Rebecca Hemenway, Yossi Matias, Ronit Levavi Morad, Avinatan Hassidim, Shravya Shetty, and María Cruz. *MedGemma Impact Challenge*. https://kaggle.com/competitions/med-gemma-impact-challenge, 2026. Kaggle.

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ for the <a href="https://kaggle.com/competitions/med-gemma-impact-challenge">MedGemma Impact Challenge</a>
</p>
