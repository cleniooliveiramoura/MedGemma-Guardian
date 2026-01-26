import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

def load_med_model(model_name="google/gemma-2-2b-it"):
    print(f"--- Iniciando carregamento do modelo: {model_name} ---")
    
    # Configuração para 4-bits (Economiza VRAM para seus 4GB)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto"
        )
        print("✅ Modelo carregado com sucesso na GPU!")
        
        # Teste rápido
        input_text = "Clinical note: Patient with 102F fever and cough. Suggest extraction."
        inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=50)
        
        print("\n--- Resultado do Teste ---")
        print(tokenizer.decode(outputs[0], skip_special_tokens=True))
        
    except Exception as e:
        print(f"❌ Erro ao carregar o modelo: {e}")
        print("Dica: Verifique se você está logado no Hugging Face e se aceitou os termos do modelo.")

if __name__ == "__main__":
    # Usando Gemma 2 2B como base (que é o motor do MedGemma)
    load_med_model()
