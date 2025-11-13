# MÓDULO 4: INTEGRAÇÃO COMPLETA - ORQUESTRAÇÃO DE LLM, OCR E RPA
import os
from typing import Dict, Any

# Importa as funções dos módulos anteriores
from ocr_module import perform_ocr 
from llm_module import analyze_invoice
from rpa_module import fill_form_rpa

# --- CONFIGURAÇÕES DO PIPELINE ---
INVOICE_IMAGE_PATH = 'invoice_sample.jpg'  # Caminho da imagem da invoice (para o OCR)
FORM_HTML_PATH = 'payment_form.html'      # Caminho do formulário HTML (para o RPA)

def run_intelligent_automation_pipeline():
    """
    Executa o pipeline de Automação Inteligente de Processos:
    1. OCR (Extrai texto bruto da imagem)
    2. LLM (Estrutura, classifica e valida o texto)
    3. RPA (Preenche e submete o formulário com os dados validados)
    """
    print("="*60)
    print("          PIPELINE DE AUTOMAÇÃO INTELIGENTE INICIADO          ")
    print("  LLM + OCR + RPA: Registro de Pagamentos de Fatura (End-to-End)  ")
    print("="*60)
    
    validated_data: Dict[str, Any] = {}
    
    # 1. Módulo 1: OCR - Extração
    raw_text = perform_ocr(INVOICE_IMAGE_PATH)
    if not raw_text:
        print("\n[FLUXO INTERROMPIDO] Falha na extração OCR. Verifique as configurações do Tesseract.")
        return

    # 2. Módulo 2: LLM - Estruturação e Validação
    validated_data = analyze_invoice(raw_text)
    
    if 'error' in validated_data:
        print(f"\n[FLUXO INTERROMPIDO] Erro no processamento do LLM: {validated_data['error']}")
        return

    # Checagem de Validação (Política de Reembolso)
    if not validated_data.get('status_validacao', False):
        print("\n" + "#"*60)
        print(f"        [FLUXO INTERROMPIDO] - INVOICE REJEITADA!        ")
        print(f" Motivo da Rejeição: {validated_data.get('motivo_rejeicao', 'Motivo não especificado.')}")
        print(" O robô RPA NÃO prosseguirá com o preenchimento.")
        print("#"*60)
        return
    else:
        print("\n" + "-"*60)
        print("        [SUCESSO] - INVOICE APROVADA PELO LLM!        ")
        print(" O robô RPA prosseguirá com o preenchimento no sistema.")
        print("-"*60)
        
    # 3. Módulo 3: RPA - Preenchimento do Formulário
    rpa_input = {
        "fornecedor": validated_data.get('fornecedor', 'N/A'), 
        "numero_invoice": validated_data.get('numero_invoice', 'N/A'), 
        "valor_total": validated_data.get('valor_total', 0.0)
    }
    
    # Somente executa se o HTML existir (para evitar erro fatal)
    if os.path.exists(FORM_HTML_PATH):
        fill_form_rpa(rpa_input, FORM_HTML_PATH)
    else:
        print(f"\n[FLUXO INTERROMPIDO] Arquivo HTML '{FORM_HTML_PATH}' não encontrado para o RPA.")

    print("\n="*60)
    print("          PIPELINE DE AUTOMAÇÃO CONCLUÍDO          ")
    print("="*60)


if __name__ == '__main__':
    # ATENÇÃO: Verifique se todos os arquivos (HTML e Python) estão na mesma pasta 
    # e se as dependências (pytesseract, selenium, Tesseract, ChromeDriver) 
    # estão instaladas e configuradas.
    
    # Para rodar, use: python full_pipeline.py
    run_intelligent_automation_pipeline()