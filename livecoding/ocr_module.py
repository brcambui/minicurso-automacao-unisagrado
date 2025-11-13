import easyocr


def analyze_invoice(image_path):
    reader = easyocr.Reader(['en', 'pt'], gpu=True)
    result = reader.readtext(image_path, detail=0)
    text = "\n".join(result)
    return text


if __name__ == "__main__":  # Vai ser executado apenas se rodar este arquivo diretamente
    extracted_text = analyze_invoice("invoice_sample.jpg")
    print("Texto extraído da imagem da fatura:")
    print(extracted_text)
