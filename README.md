# 🚀 Projeto: Automação Inteligente de Processos (LLM, OCR e RPA)

Este projeto de minicurso demonstra a integração de três pilares da automação inteligente: OCR (Reconhecimento Óptico de Caracteres), LLM (Large Language Model) e RPA (Robotic Process Automation), utilizando tecnologias modernas de IA.

# 🎯 Objetivo do Pipeline

O objetivo é simular um processo de negócio de ponta a ponta:

**OCR**: Extrair dados brutos de uma fatura (Invoice) em formato de imagem usando **EasyOCR**.

**LLM**: Estruturar, categorizar e validar os dados extraídos usando **Google Gemini API**, aplicando políticas de reembolso (Ex: limite de valor de R$ 10.000,00).

**RPA**: Preencher e submeter automaticamente os dados validados em um sistema de registro de pagamentos (formulário web simulado) usando **Selenium**.

# 🏗️ Arquitetura do Projeto
```
[Invoice (JPG/PNG)]
       |
       V
[ocr_module.py] (EasyOCR) -> Texto Bruto
       |
       V
[llm_module.py] (Google Gemini API) -> Dados Estruturados e Validados (JSON)
       |
       V (Se Aprovado)
[rpa_module.py] (Selenium) -> Preenchimento do Formulário Web
       |
       V
[payment_form.html] (Sistema de Registro)
```

# 🛠️ Pré-requisitos de Instalação

## 1. Requisitos de Software

É necessário instalar as seguintes ferramentas:

**Python**: Versão 3.8 ou superior.

**Google Chrome/Edge**: Navegador para o RPA.

**Google Gemini API Key**: Você precisará de uma chave de API do Google Gemini. Obtenha gratuitamente em: [Google AI Studio](https://makersuite.google.com/app/apikey)

## 2. Requisitos de Bibliotecas Python

Instale todas as dependências em seu ambiente virtual:

```bash
pip install easyocr pillow selenium webdriver-manager google-genai
```

Ou use o `uv` (gerenciador de pacotes moderno):

```bash
uv pip install easyocr pillow selenium webdriver-manager google-genai
```

# ⚙️ Configuração dos Módulos

> ⚠️ Atenção: Este é o passo mais comum onde os alunos encontram problemas.

## A. Configuração do OCR (ocr_module.py)

O script usa o **EasyOCR**, que baixa automaticamente os modelos de linguagem necessários (`en` e `pt`) na primeira execução. O download pode demorar alguns minutos.

**Nota importante**: O EasyOCR está configurado com `gpu=True` por padrão. Se você não tiver uma GPU NVIDIA com CUDA instalado, altere para `gpu=False` no arquivo `ocr_module.py`:

```python
reader = easyocr.Reader(['en', 'pt'], gpu=False)
```

## B. Configuração do LLM (llm_module.py)

O script usa a **API do Google Gemini** (modelo `gemini-2.0-flash`). 

**Passo obrigatório**: Você precisa adicionar sua chave de API no arquivo `llm_module.py`:

```python
client = genai.Client(api_key="SUA_CHAVE_AQUI")
```

O modelo usa:
- **Structured Output** (JSON Schema) para garantir formato consistente
- **System Instruction** para validação de políticas de negócio
- **Temperature 0.0** para respostas determinísticas

## C. Configuração do RPA (rpa_module.py)

O RPA é configurado para usar o `webdriver_manager`, que baixa e configura o ChromeDriver automaticamente. Certifique-se de que o Chrome está instalado.

# ▶️ Como Rodar o Projeto

**Organização**: Coloque todos os arquivos (`.py` e `.html`) na mesma pasta.

**Invoice**: Certifique-se de ter uma imagem chamada `invoice_sample.jpg` na mesma pasta (ou altere o nome nos scripts).

**Configuração da API**: Adicione sua chave do Google Gemini no arquivo `llm_module.py`.

**Execução**: Execute cada módulo individualmente ou o pipeline completo:

## Testar Módulos Individualmente:

```bash
# Testar OCR
python ocr_module.py

# Testar LLM
python llm_module.py

# Testar RPA
python rpa_module.py
```

## Executar Pipeline Completo:

```bash
python full_pipeline.py
```

## O Que Esperar

Ao rodar o pipeline:

1. O terminal mostrará o **texto extraído pelo OCR** (EasyOCR).

2. O terminal exibirá os **dados estruturados em JSON** e o **resultado da validação** (✅ APROVADO/❌ REJEITADO) pelo LLM.

3. Se a invoice for **APROVADA** (valor <= R$ 10.000,00), o RPA abrirá o navegador automaticamente, preencherá o formulário `payment_form.html` e o submeterá.

4. Se a invoice for **REJEITADA** (valor > R$ 10.000,00), o processo será interrompido e a razão da rejeição será exibida.

# 📁 Detalhes dos Arquivos

## Pasta `/gabarito` (Código Completo Comentado)

| Arquivo | Tecnologia | Função no Pipeline |
| ------- | ---------- | ------------------ |
| `ocr_module.py` | EasyOCR | Extrai texto de imagens de faturas usando modelos de deep learning (suporta inglês e português). |
| `llm_module.py` | Google Gemini API | Usa LLM com structured output (JSON Schema) para extrair campos estruturados e validar políticas de negócio. |
| `rpa_module.py` | Selenium + WebDriver Manager | Automatiza o navegador Chrome para preencher e submeter formulários web. |
| `full_pipeline.py` | Python (Orquestração) | Integra os 3 módulos em um fluxo completo: OCR → LLM → RPA. |

## Pasta `/livecoding` (Código Simplificado para Aula)

Versões mais diretas dos módulos, sem estrutura de funções e tratamento de erros completos, ideal para demonstrações ao vivo.

## Arquivo Auxiliar

| Arquivo | Tecnologia | Função |
| ------- | ---------- | ------ |
| `payment_form.html` | HTML/CSS (Tailwind) | Simula o sistema de pagamento alvo do RPA com validação JavaScript. |

## Estrutura do Projeto

```
📦 minicurso-ia-unisagrado/
├── 📁 gabarito/          # Código completo com documentação
│   ├── full_pipeline.py
│   ├── llm_module.py
│   ├── ocr_module.py
│   └── rpa_module.py
├── 📁 livecoding/        # Código simplificado para demonstrações
│   ├── full_pipeline.py
│   ├── llm_module.py
│   ├── ocr_module.py
│   └── rpa_module.py
├── payment_form.html     # Formulário web de destino
├── invoice_sample.jpg    # Imagem de exemplo (adicionar)
├── pyproject.toml        # Configuração de dependências
└── README.md             # Este arquivo
```