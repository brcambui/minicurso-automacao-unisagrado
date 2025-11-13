from ocr_module import analyze_invoice
from llm_module import extract_info
from rpa_module import register_invoice
import json

print("Iniciando o pipeline completo de processamento de faturas...")
text = analyze_invoice("invoice_sample.jpg")
print("Texto extraído da imagem da fatura")
data_json = extract_info(text)
data = json.loads(data_json)
print("Dados extraídos e validados da fatura")
print(data)
register_invoice(data)
print("Dados registrados no formulário de pagamento.")