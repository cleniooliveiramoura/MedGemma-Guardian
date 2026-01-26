# MedGemma Guardian: Agente de Auditoria Clínica e Segurança do Paciente

*Submissão para MedGemma Impact Challenge – Google Health AI*

## 1. Introdução e Motivação
O **MedGemma Guardian** foi concebido para demonstrar impacto prático e uso responsável de IA em ambientes clínicos de alta pressão. O foco central é o **Medical Document Understanding (MDU)** aplicado à segurança do paciente, prevenindo erros de prescrição e falhas de documentação que, embora evitáveis, continuam sendo causas principais de riscos assistenciais e passivos jurídicos.

### 1.1. Equipe
- **Clenio Afonso de Oliveira Moura** — *Cientista de Dados & Engenheiro de IA*
  - Desenvolvedor líder responsável pela implementação full-stack, integração com MedGemma e estratégia de prompting Chain-of-Thought.
  - Especializações: Python, Machine Learning, Deep Learning, Processamento de Dados.
  - GitHub: [clenio77](https://github.com/clenio77)

## 2. Objetivo do Projeto
Demonstrar uma aplicação prática do MedGemma que:
* Realize extração semântica de entidades clínicas (Sintomas, Medicações, Dosagens).
* Execute **auditoria matemática rigorosa** sobre prescrições em tempo real.
* Gere saídas estruturadas em formato compatível com **FHIR JSON** para interoperabilidade.
* Garanta a privacidade total via execução local (Edge AI), permitindo que dados sensíveis nunca saiam da infraestrutura hospitalar.

## 3. Arquitetura "Safety-First"
A solução utiliza uma arquitetura baseada em agentes lógicos, onde o MedGemma (configurado via HAI-DEF) atua como o núcleo de processamento.
* **Pipeline de Auditoria:** Documento → Extração MDU → Auditoria Matemática (CoT) → Classificação de Risco → Relatório de Segurança.
* **Técnica Chain-of-Thought (CoT):** O modelo é instruído a processar internamente o cálculo de dosagens diárias cumulativas antes de emitir o veredito de risco, garantindo precisão superior em tarefas aritméticas de toxicidade.

## 4. Caso Demonstrativo: Prevenção de Toxicidade por Paracetamol
Selecionamos a auditoria de Paracetamol (Acetaminofeno) como cenário principal devido ao seu alto risco de hepatotoxicidade em doses superiores a 4000mg/dia. 
* **Demonstração:** O sistema identifica quando um paciente é prescrito com "10 comprimidos de 500mg" e sinaliza um **Risco Crítico**, explicando a lógica: "500mg x 10 = 5000mg (> 4000mg limite)".

## 5. Implementação e Uso do MedGemma
* **Eficiência em Hardware:** Validação do uso do MedGemma 2b com quantização de 4 bits, permitindo execução fluida em dispositivos com apenas 4GB de VRAM.
* **Human-in-the-Loop:** A interface inclui um módulo de **Protocolos de Segurança**, onde o médico pode auditar as regras que a IA está seguindo, garantindo a transparência e a autoridade clínica sobre o algoritmo.

## 6. Ética e Privacidade
* **Privacidade Local:** O processamento offline elimina a necessidade de APIs de terceiros e nuvens públicas para dados de pacientes.
* **IA Responsável:** Segue os princípios da iniciativa Health AI Developer Foundations, focando na explicabilidade e evitando a tomada de decisão autônoma (o sistema sugere riscos para que o médico decida).

## 7. Conclusão
O MedGemma Guardian prova que modelos médicos compactos e abertos podem salvar vidas ao atuar como uma camada de segurança documental inteligente. A solução atende aos pilares do desafio: impacto real, proteção de dados e centralidade no ser humano.

---

## Referências
Fereshteh Mahvar, Yun Liu, Daniel Golden, Fayaz Jamil, Sunny Jansen, Can Kirmizi, Rory Pilgrim, David F. Steiner, Andrew Sellergren, Richa Tiwari, Sunny Virmani, Liron Yatziv, Rebecca Hemenway, Yossi Matias, Ronit Levavi Morad, Avinatan Hassidim, Shravya Shetty e María Cruz. *O Desafio de Impacto MedGemma*. https://kaggle.com/competitions/med-gemma-impact-challenge, 2026. Kaggle.
