import os
import json
from typing import Dict, Any
from google import genai
from google.genai import types

# --- 1. Definições do Schema e Prompt ---

# Definição do Schema JSON para forçar a saída estruturada
# O SDK utiliza o formato JSON Schema/OpenAPI 3.0 para estruturar as saídas
JSON_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "fornecedor": {"type": "STRING", "description": "Nome completo do fornecedor."},
        "numero_invoice": {"type": "STRING", "description": "Número da fatura ou invoice."},
        "valor_total": {"type": "NUMBER", "description": "Valor total da fatura como um número (float ou int)."},
        "status_validacao": {"type": "BOOLEAN", "description": "True se a invoice está dentro da política (valor <= 5000), False caso contrário."},
        "motivo_rejeicao": {"type": "STRING", "description": "Motivo da rejeição se status_validacao for False, ou string vazia se aprovado."}
    },
    "propertyOrdering": ["fornecedor", "numero_invoice", "valor_total", "status_validacao", "motivo_rejeicao"]
}

# Prompt de Engenharia (Instrução do Sistema)
SYSTEM_PROMPT = """
Você é um extrator e validador de dados de faturas. Sua tarefa é:
1. Analisar o texto bruto fornecido de uma fatura
2. Extrair: fornecedor, numero_invoice e valor_total
3. Validar: se o valor_total é menor ou igual a R$ 5000,00
4. Retornar status_validacao=True se aprovado (valor <= 5000), False se rejeitado (valor > 5000)
5. Se rejeitado, preencher motivo_rejeicao com "Valor acima do limite de R$ 5000,00"
6. Se aprovado, deixar motivo_rejeicao como string vazia

Retorne apenas o JSON estruturado, sem texto adicional.
"""

# --- 2. Configuração do Cliente ---

# Recomenda-se carregar a chave de uma variável de ambiente (GEMINI_API_KEY)
# Caso contrário, você pode inicializar com genai.Client(api_key="SUA_CHAVE_AQUI")
client = genai.Client(api_key="SUA_CHAVE_AQUI")

# --- 3. Função Principal: analyze_invoice ---

def analyze_invoice(raw_text: str) -> Dict[str, Any]:
    """
    Analisa o texto bruto de uma invoice usando o LLM Gemini.
    
    Args:
        raw_text: Texto extraído da invoice (geralmente vindo do OCR)
    
    Returns:
        Dicionário com os campos:
        - fornecedor (str)
        - numero_invoice (str)
        - valor_total (float)
        - status_validacao (bool)
        - motivo_rejeicao (str)
        - error (str) - presente apenas se houver erro
    """
    print(f"\n[LLM] Analisando invoice com o modelo Gemini...")
    
    # Configuração da Geração
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema=JSON_SCHEMA,
        temperature=0.0 
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"Extraia e valide os dados desta fatura:\n\n{raw_text}",
            config=config
        )
        
        # Parse do JSON retornado
        validated_data = json.loads(response.text)
        
        print(f"[LLM] Extração concluída:")
        print(f"  - Fornecedor: {validated_data.get('fornecedor', 'N/A')}")
        print(f"  - Número Invoice: {validated_data.get('numero_invoice', 'N/A')}")
        print(f"  - Valor Total: R$ {validated_data.get('valor_total', 0.0)}")
        print(f"  - Status Validação: {'✅ APROVADO' if validated_data.get('status_validacao') else '❌ REJEITADO'}")
        
        if not validated_data.get('status_validacao'):
            print(f"  - Motivo Rejeição: {validated_data.get('motivo_rejeicao', 'N/A')}")
        
        return validated_data
        
    except Exception as e:
        print(f"[LLM] Erro ao processar invoice: {e}")
        return {"error": str(e)}

# --- 4. Exemplo de Uso (quando executado diretamente) ---

if __name__ == '__main__':
    print("="*60)
    print("     TESTE DO MÓDULO LLM - analyze_invoice()     ")
    print("="*60)
    
    # Texto de exemplo que simula o conteúdo de uma fatura
    invoice_text_example = """
    Detalhes da Transação
    Empresa: Soluções Digitais Ltda.
    Referência da Fatura: INV-2025-4590
    Data: 12/11/2025
    Total Devido: R$ 1250.75
    """
    
    print("\n[TESTE] Texto da Invoice:")
    print(invoice_text_example)
    
    # Chama a função analyze_invoice
    result = analyze_invoice(invoice_text_example)
    
    print("\n" + "="*60)
    print("     RESULTADO DA ANÁLISE     ")
    print("="*60)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    
    # Teste com valor acima do limite
    print("\n\n" + "="*60)
    print("     TESTE 2: Invoice com Valor Acima do Limite     ")
    print("="*60)
    
    invoice_text_high_value = """
    Nota Fiscal
    Fornecedor: Tech Solutions Corp.
    NF: 2025-9876
    Valor Total: R$ 7.500,00
    """
    
    print("\n[TESTE 2] Texto da Invoice:")
    print(invoice_text_high_value)
    
    result2 = analyze_invoice(invoice_text_high_value)
    
    print("\n" + "="*60)
    print("     RESULTADO DA ANÁLISE     ")
    print("="*60)
    print(json.dumps(result2, indent=4, ensure_ascii=False))