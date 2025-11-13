# MÓDULO 1: OCR (EASYOCR) - EXTRAÇÃO DE TEXTO BRUTO
import easyocr
import os
from typing import List

# CONFIGURAÇÃO IMPORTANTE:
# Instalação: pip install easyocr pillow
# O EasyOCR baixa o modelo (cerca de 50MB) na primeira execução.

# Inicializa o leitor do EasyOCR. 
# Usamos ['en'] e ['pt'] para garantir boa leitura, pois o texto da fatura
# contém inglês (INVOICE, NO.) e português (Fornecedor, Valor Total).
try:
    READER = easyocr.Reader(['en', 'pt'], gpu=False) 
    print("Módulo OCR local (EasyOCR) carregado com sucesso.")
except Exception as e:
    READER = None
    print(f"AVISO: Falha ao carregar o EasyOCR. Certifique-se de que 'easyocr' e 'torch' estão instalados. Detalhes: {e}")

def perform_ocr(image_path: str) -> str:
    """
    Executa o OCR em um arquivo de imagem e retorna o texto bruto extraído.
    """
    print("\n--- 1. INICIANDO OCR: Extraindo texto bruto da imagem ---")
    
    if not READER:
        print("ERRO OCR: O leitor EasyOCR não foi inicializado. Retornando texto MOCKADO.")
        return """
        FORNECEDOR: Soluções em Automação Inteligente S.A.
        INVOICE NO. ABC-123-DE
        DATA: 01/11/2025
        DETALHES: Serviços de Consultoria em TI
        VALOR TOTAL: R$ 4.500,00 
        """

    if not os.path.exists(image_path):
        print(f"ERRO OCR: Imagem não encontrada no caminho: {image_path}. Retornando texto MOCKADO.")
        return """
        FORNECEDOR: Logística Rápida Ltda.
        INVOICE NO. 9999
        DATA: 01/12/2025
        DETALHES: Serviços de Frete
        VALOR TOTAL: R$ 5.000,01 
        """

    try:
        # Lê o texto da imagem. detail=0 retorna apenas o texto, simplificando o output.
        results: List[str] = READER.readtext(image_path, detail=0)
        
        # Concatena os resultados em uma única string
        raw_text = "\n".join(results)
        
        print("EXTRAÇÃO OCR CONCLUÍDA:")
        print("---------------------------------")
        print(raw_text.strip())
        print("---------------------------------")
        
        return raw_text
    
    except Exception as e:
        print(f"ERRO INESPERADO no EasyOCR: {e}")
        return ""


if __name__ == '__main__':
    # Este bloco de teste requer a criação de um arquivo 'invoice_sample.jpg' 
    # na mesma pasta.
    
    # Exemplo de chamada direta (retorna texto mockado se o arquivo não existir)
    ocr_output = perform_ocr('invoice_sample.jpg')
    
    if ocr_output:
        print(f"\nOCR finalizado. Total de caracteres extraídos: {len(ocr_output)}")
    else:
        print("\nOCR falhou completamente.")
    print("\n--- Fim do Módulo 1 ---")