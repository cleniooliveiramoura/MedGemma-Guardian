import os
import json
from typing import List, Dict
import google.generativeai as genai
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    hf_api_key: str = ""
    google_api_key: str = ""
    use_local_model: bool = False

    model_config = {
        "env_file": ".env",
        "extra": "ignore" # Ignore extra env vars to prevent errors
    }

settings = Settings()

class ClinicalEngine:
    """
    Orchestrates clinical extraction and REGULATORY compliance 
    using Gemini 2.5 Flash Lite or MedGemma.
    """
    
    def __init__(self):
        self.model_type = "MedGemma Guardian (Core)"
        if settings.google_api_key:
            genai.configure(api_key=settings.google_api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-09-2025')
        else:
            self.model = None

    async def analyze(self, text: str) -> Dict:
        # Strict Regulatory Rules
        rules_context = """
        REGULATORY RULES:
        - Max Paracetamol/Acetaminophen dose: 4000mg/day. (CRITICAL: 10 tablets of 500mg = 5000mg, which is an OVERDOSE).
        - Pediatric safety: Dose for children (<12y) MUST mention weight.
        - High Fever: >= 39°C is an URGENT CLINICAL RISK.
        """

        prompt = f"""
        You are the 'MedGemma Guardian'. You MUST be paranoid about patient safety.
        
        TASK:
        1. Extract: Symptoms, Medications, Dosage units, Frequency.
        2. MANDATORY CALCULATION: For every medication, multiply (Concentration) x (Quantity per day).
        3. STRICT AUDIT: If total daily dose > 4000mg for Paracetamol, YOU MUST set risk_level to 'Critical'.
        
        INPUT:
        {text}
        
        OUTPUT RULES:
        - compliance_summary: Must be in PORTUGUESE (PT-BR). Explain the math if a limit was exceeded.
        - risk_level: Must be 'Critical' if any rule is violated.
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "entities": [
                {{
                    "name": "term",
                    "category": "SYMPTOM|MEDICATION|DOSAGE|RISK",
                    "value": "standardized value",
                    "status": "success|alert|error"
                }}
            ],
            "compliance_summary": "Resumo profissional em Português, detalhando a auditoria de segurança.",
            "risk_level": "Low|Medium|High|Critical"
        }}
        """
        
        if not self.model:
            return {"entities": [{"name": "Auth Error", "category": "SYSTEM", "value": "Missing API Key", "status": "error"}], "compliance_summary": "Config (.env) required.", "risk_level": "N/A"}

        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except Exception as e:
            return {
                "entities": [{"name": "Inference Error", "category": "IA", "value": str(e), "status": "error"}],
                "compliance_summary": "Ocorreu um erro no processamento neural.",
                "risk_level": "High"
            }

clinical_engine = ClinicalEngine()
