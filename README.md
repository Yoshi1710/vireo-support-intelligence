# Vireo Support Intelligence Platform

Deterministic, low-latency customer ticket classification, automated routing, and operational intelligence engine.

---

## Executive Overview
This repository provides an engineering-first decision support system designed to resolve frontline support bottlenecks and eliminate capital misallocation.

* Inference Engine: Scikit-Learn TF-IDF (1,3 n-grams) + Multinomial Logistic Regression.
* Performance Benchmark: 86.38% overall accuracy on 2,356 unseen tickets (0.94 F1 on Delivery, 0.91 F1 on Audio Quality).
* Cost & Latency: Fully local CPU execution (<15ms per inference) at $0 recurring API cost.
* Core Business Impact: Prevents misallocating Rs 9,00,000/year to an artificially inflated Billing queue and identifies Logistics as the true operational bottleneck (39.75h resolution time).

---

## Repository Structure
* app.py: Streamlit-powered triage workstation for live ticket routing.
* memo.md: 1-page executive memorandum detailing audit findings and headcount strategy.
* submission-form.md: Comprehensive technical and business evaluation record.
* requirements.txt: Minimal runtime dependencies.
* src/analyze.py: Exploratory analysis discovering the 42.3% Billing misrouting pattern.
* src/classifier.py: End-to-end model training, evaluation, and serialization pipeline.
* src/ticket_classifier.pkl: Serialized production model artifact.

---

## Quickstart Guide

1. Setup Environment:
   git clone <https://github.com/Yoshi1710/vireo-support-intelligence>
   cd vireo-support-intelligence
   python -m venv venv

2. Activate Virtual Environment:
   Windows: .\venv\Scripts\Activate.ps1
   Linux/macOS: source venv/bin/activate

3. Install Dependencies:
   pip install -r requirements.txt

4. Launch Triage Workstation:
   streamlit run app.py

5. Re-evaluate / Retrain (Optional):
   python src/analyze.py
   python src/classifier.py