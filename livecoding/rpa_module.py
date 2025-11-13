# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
# Só pra pegar o caminho do arquivo HTML
import os
# Time para delays entre ações
import time


html_file_path = "payment_form.html"
file_url = 'file:///' + os.path.abspath(html_file_path).replace('\\', '/')


def register_invoice(data):
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(file_url)  # Abre o arquivo HTML local
    time.sleep(2)  # Espera 2 segundos para garantir que a página carregou

    # Preencher o campo de fornecedor
    driver.find_element(By.ID, "supplierName").send_keys(data["fornecedor"])
    time.sleep(2)  # Espera 2 segundos

    # Preencher o campo de número da invoice
    driver.find_element(By.ID, "invoiceNumber").send_keys(
        data["numero_invoice"])
    time.sleep(2)  # Espera 2 segundos

    # Preencher o campo de valor total
    driver.find_element(By.ID, "totalValue").send_keys(
        f"$ {data['valor_total']:.2f}".replace('.', ','))
    time.sleep(2)  # Espera 2 segundos

    # Clicar no botão de enviar
    driver.find_element(By.ID, "submitButton").click()

    time.sleep(5)
    driver.quit()  # Fecha o navegador após 5 segundos


if __name__ == "__main__":
    # Exemplo de dados extraídos e validados
    sample_data = {
        "fornecedor": "Aenean LLC",
        "numero_invoice": "284213",
        "valor_total": 9778.40,
        "status_validacao": True,
        "motivo_rejeicao": ""
    }
    register_invoice(sample_data)
