from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file: str) -> list[str]:

    with open(pdf_file, 'rb') as pdf:
        reader = PdfReader(pdf, strict = False)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()

            pdf_text.append(content)

        return pdf_text
    
def main() -> None:
    text_pdf = extract_text_from_pdf('Sample.pdf')

    for page in text_pdf:
        text = page.split('  ')
        cleaned_text = [line.strip() for line in text if line != '']

        for line in cleaned_text:
            print(line)
    
if __name__ == '__main__':
    main()