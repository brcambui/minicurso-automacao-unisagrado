# MÓDULO 3: RPA - PREENCHIMENTO AUTOMÁTICO DE FORMULÁRIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import WebDriverException
import time
import os
from typing import Dict, Any

# CONFIGURAÇÃO IMPORTANTE:
# Para rodar localmente, você precisa ter o Chrome (ou outro navegador) e o 
# seu respectivo driver (Ex: ChromeDriver) instalados e no PATH ou especificados.
# Instalação: pip install selenium webdriver_manager (opcional, para gerenciar o driver)

# Use 'webdriver_manager' para gerenciar o driver automaticamente (mais fácil para os alunos)
try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_DRIVER_MANAGER = True
except ImportError:
    USE_DRIVER_MANAGER = False
    print("AVISO: 'webdriver_manager' não instalado. Certifique-se de que o 'chromedriver' está no PATH.")

def fill_form_rpa(data: Dict[str, Any], html_file_path: str):
    """
    Inicia o RPA (navegador), preenche o formulário com os dados validados 
    e submete.
    """
    print("\n--- 3. INICIANDO RPA: Preenchendo o sistema de pagamento ---")
    
    if not os.path.exists(html_file_path):
        print(f"ERRO RPA: O arquivo do formulário '{html_file_path}' não foi encontrado. Execute o script na mesma pasta do arquivo HTML.")
        return

    # Define o caminho do arquivo HTML como URL local
    file_url = 'file:///' + os.path.abspath(html_file_path).replace('\\', '/')
    
    # Configura o driver (com ou sem manager)
    try:
        if USE_DRIVER_MANAGER:
            # Opção mais fácil para os alunos
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        else:
            # Opção se o driver estiver no PATH
            driver = webdriver.Chrome() 

        driver.get(file_url)
        print(f"Navegador aberto na URL: {file_url}")
        time.sleep(2) # Espera carregar

        # 1. Preenche o Nome do Fornecedor (ID: supplierName)
        print(f"Preenchendo Nome do Fornecedor: {data['fornecedor']}")
        driver.find_element(By.ID, "supplierName").send_keys(data['fornecedor'])
        
        # 2. Preenche o Número da Invoice (ID: invoiceNumber)
        print(f"Preenchendo Número da Invoice: {data['numero_invoice']}")
        driver.find_element(By.ID, "invoiceNumber").send_keys(data['numero_invoice'])
        
        # 3. Preenche o Valor Total (ID: totalValue)
        # Formata o valor para o padrão de exibição (pode ser necessário no sistema real)
        valor_str = f"R$ {data['valor_total']:.2f}".replace('.', ',')
        print(f"Preenchendo Valor Total: {valor_str}")
        driver.find_element(By.ID, "totalValue").send_keys(valor_str)
        
        time.sleep(1) 
        
        # 4. Clica no botão de Registrar (ID: submitButton)
        print("Clicando no botão 'Registrar Pagamento'...")
        driver.find_element(By.ID, "submitButton").click()

        time.sleep(3) # Espera o resultado da submissão no formulário
        
        print("RPA CONCLUÍDO: O formulário foi submetido com sucesso.")

    except WebDriverException as e:
        print(f"ERRO NO SELENIUM: Verifique se o Google Chrome está instalado e se o ChromeDriver está configurado corretamente. Detalhes: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado no RPA: {e}")
    finally:
        if 'driver' in locals():
            time.sleep(1)
            driver.quit() # Fecha o navegador

if __name__ == '__main__':
    # Este bloco é apenas para testar o módulo individualmente
    sample_data = {
        "fornecedor": "Teste RPA Simples", 
        "numero_invoice": "TEST0001", 
        "valor_total": 1250.50
    }
    fill_form_rpa(sample_data, 'payment_form.html')
    print("\n--- Fim do Módulo 3 ---")