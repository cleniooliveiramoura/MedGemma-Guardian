# MedGemma Guardian: Privacy-Preserving Clinical Decision Support & Safety Auditing
**Submission for MedGemma Impact Challenge - Google Health AI**

## 1. Executive Summary
MedGemma Guardian is a specialized medical agent designed to address the critical gap in hospital documentation safety. By leveraging the **MedGemma** (HAI-DEF) model, the system performs automated **Medical Document Understanding (MDU)**, extracting structured clinical entities and auditing them against safety protocols in real-time. Our solution focuses on three pillars: **Patient Safety (overdose prevention), Transparency (interpretable clinical rules), and Privacy (local execution).**

## 1.1. Team
- **Clenio Afonso de Oliveira Moura** — *Data Scientist & AI Engineer*
  - Lead Developer responsible for full-stack implementation, MedGemma integration, and Chain-of-Thought prompting strategy.
  - Specializations: Python, Machine Learning, Deep Learning, Data Processing.
  - GitHub: [clenio77](https://github.com/clenio77)

## 2. Problem Statement
Diagnostic and prescription errors often stem from incomplete or misinterpreted clinical documentation. Manual audit of thousands of patient notes is impossible. MedGemma Guardian automates this process, acting as a "second pair of eyes" for the clinical team, specifically catching mathematical dosage errors that standard NLP models often miss.

## 3. Technical Architecture
The system is built as a hybrid edge-AI application:
- **Core Engine:** Powered by MedGemma 2b (highly quantized for 4GB VRAM environments).
- **Inference Strategy:** We implemented **Chain-of-Thought (CoT)** prompting. Instead of just identifying medications, the model is forced to perform internal calculations (e.g., *Dosage x Frequency*) before assigning a risk level.
- **Data Pipeline:** Uses a FastAPI backend to ingest clinical notes and PDFs, converting them into a structured **FHIR-compatible** internal format.
- **Frontend:** A modern "Glassmorphism" interface designed for low cognitive load in high-stress clinical environments.

## 4. Safety & Responsible AI
In compliance with Health AI Developer Foundations:
- **Privacy By Design:** The model is optimized for local execution via 4-bit quantization, ensuring patient data never leaves the hospital's premises.
- **Explicability:** The "Safety Protocols" module allows clinicians to see exactly which rules the IA is enforcing.
- **Human-in-the-Loop:** The system provides alerts but does not perform actions; it empowers the physician with "Safety Audits" to support final decision-making.

## 5. Impact & Scalability
Our anchor case—Acetaminophen (Paracetamol) toxicity prevention—demonstrates immediate impact. By catching doses over 4000mg/day, the system prevents potential liver failure. The architecture is horizontally scalable to any medical specialty by simply updating the "Safety Protocols" repository.

## 6. Conclusion
MedGemma Guardian proves that specialized, small medical models like Gemma 2b can provide life-saving clinical intelligence without the costs and privacy risks of large-scale cloud LLMs.

---

## References
Fereshteh Mahvar, Yun Liu, Daniel Golden, Fayaz Jamil, Sunny Jansen, Can Kirmizi, Rory Pilgrim, David F. Steiner, Andrew Sellergren, Richa Tiwari, Sunny Virmani, Liron Yatziv, Rebecca Hemenway, Yossi Matias, Ronit Levavi Morad, Avinatan Hassidim, Shravya Shetty, and María Cruz. *MedGemma Impact Challenge*. https://kaggle.com/competitions/med-gemma-impact-challenge, 2026. Kaggle.
