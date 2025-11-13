from google import genai
from google.genai import types

system_prompt = """
Você é um extrator e validador de dados de faturas. Sua tarefa é:
1. Analisar o texto bruto fornecido de uma fatura
2. Extrair: fornecedor, numero_invoice e valor_total
3. Validar: se o valor_total é menor ou igual a R$ 10000,00
4. Retornar status_validacao=True se aprovado (valor <= 10000), False se rejeitado (valor > 10000)
5. Se rejeitado, preencher motivo_rejeicao com "Valor acima do limite de R$ 10000,00"
6. Se aprovado, deixar motivo_rejeicao como string vazia

JSON a ser extraído:
- fornecedor (string): Nome do fornecedor da fatura.
- numero_invoice (string): Número da fatura ou invoice.
- valor_total (float): Valor total da fatura.
- status_validacao (boolean): True se a invoice está dentro da política (valor <= 10000), False caso contrário.
- motivo_rejeicao (string): Motivo da rejeição se status_validacao for False, ou string vazia se aprovado.

Retorne apenas o JSON estruturado, sem texto adicional.
"""

def extract_info(text):
    client = genai.Client(api_key="AIzaSyAU0Xp91NhRJ_zqdZlX4n130xoLjILRd9g")
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json"
    )
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=f"Extraia e valide os dados desta fatura:\n\n{text}",
        config=config
    )
    return response.text


if __name__ == "__main__":
    sample_text = """
    Fornecedor: Aenean LLC
    Número da Invoice: 284213
    Valor Total: R$ 9778,40
    """
    result = extract_info(sample_text)
    print("Dados extraídos e validados da fatura:")
    print(result)