"""
================================================================================
                    MedGemma Guardian: Clinical Decision Support & Safety Audit
                    Final Submission for MedGemma Impact Challenge 2026
================================================================================

### Project Name
MedGemma Guardian - Privacy-Preserving Clinical Decision Support & Safety Auditing

### Team
- Clenio Afonso de Oliveira Moura (@clenio77)
  - Role: Lead Developer & AI Engineer
  - Specializations: Python, Machine Learning, Deep Learning, Data Processing
  - GitHub: https://github.com/clenio77

### Problem Statement
Diagnostic and prescription errors often stem from incomplete or misinterpreted 
clinical documentation. Manual audit of thousands of patient notes is impossible. 
MedGemma Guardian automates this process, acting as a "second pair of eyes" for 
the clinical team, specifically catching mathematical dosage errors that standard 
NLP models often miss.

### Overall Solution
An AI-powered clinical safety agent using MedGemma (HAI-DEF) for:
- Automated Medical Document Understanding (MDU)
- Chain-of-Thought dosage calculations
- Real-time safety auditing (e.g., Acetaminophen > 4000mg/day detection)
- Privacy-first local execution (4-bit quantization)

### Technical Details
- Core Engine: MedGemma 2b with 4-bit quantization (runs on 4GB VRAM)
- Inference: Chain-of-Thought prompting for accurate mathematical reasoning
- Output: FHIR-compatible JSON with risk classification

### Repository
https://github.com/clenio77/MedGemma-Guardian

### Citation
Fereshteh Mahvar, Yun Liu, Daniel Golden, Fayaz Jamil, Sunny Jansen, Can Kirmizi, 
Rory Pilgrim, David F. Steiner, Andrew Sellergren, Richa Tiwari, Sunny Virmani, 
Liron Yatziv, Rebecca Hemenway, Yossi Matias, Ronit Levavi Morad, Avinatan Hassidim, 
Shravya Shetty, and María Cruz. MedGemma Impact Challenge. 
https://kaggle.com/competitions/med-gemma-impact-challenge, 2026. Kaggle.
================================================================================
"""

# 1. INSTALLATION & SETUP
# !pip install -q -U transformers accelerate bitsandbytes

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import json

# 2. MODEL LOADING (MedGemma HAI-DEF)
model_id = "google/medgemma-2b-it" # Replace with specific HAI-DEF weight path if needed

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

print("Loading MedGemma Guardian Engine...")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)

# 3. CORE INFERENCE ENGINE
def analyze_clinical_note(text):
    rules_context = """
    REGULATORY RULES:
    - Max Paracetamol/Acetaminophen dose: 4000mg/day. (CRITICAL: 10 tablets of 500mg = 5000mg, which is an OVERDOSE).
    - Pediatric safety: Dose for children (<12y) MUST mention weight.
    - High Fever: >= 39°C is an URGENT CLINICAL RISK.
    """

    prompt = f"""<start_of_turn>user
    You are the 'MedGemma Guardian'. You MUST be paranoid about patient safety.
    
    TASK:
    1. Extract: Symptoms, Medications, Dosage units, Frequency.
    2. MANDATORY CALCULATION: For every medication, multiply (Concentration) x (Quantity per day).
    3. STRICT AUDIT: If total daily dose > 4000mg for Paracetamol, YOU MUST set risk_level to 'Critical'.
    
    INPUT:
    {text}
    
    OUTPUT RULES:
    - compliance_summary: Must be in PORTUGUESE (PT-BR). Explain the math clearly.
    - risk_level: Must be 'Critical' if any rule is violated.
    
    Return ONLY a JSON object:
    {{
        "entities": [{{ "name": "...", "category": "...", "value": "...", "status": "success|alert|error" }}],
        "compliance_summary": "Resumo em Português com auditoria matemática.",
        "risk_level": "Low|Medium|High|Critical"
    }}<end_of_turn>
    <start_of_turn>model
    """

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=512, do_sample=False)
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    raw_output = response.split("model")[-1].strip()
    
    # Simple JSON cleaning for local model output
    if "```json" in raw_output:
        raw_output = raw_output.split("```json")[1].split("```")[0].strip()
    elif "{" in raw_output:
        raw_output = raw_output[raw_output.find("{"):raw_output.rfind("}")+1]
        
    return raw_output

# 4. TEST CASE
sample_note = "Patient prescribed 10 tablets of Paracetamol 500mg today for severe pain."
result = analyze_clinical_note(sample_note)
print(result)
