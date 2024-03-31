import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(pdf_file: str) -> list[str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PdfReader(pdf, strict = False)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()

            cleaned_content = re.sub(r'[^\w\s.,:;%]', '', content)

            content_more_spaces = re.sub(r'(?<=\d)(\s*)([A-Z])', r'\1 \2', cleaned_content)

            text_lines = re.split(r'(?<=[.,:;])\s+|\s{2,}', content_more_spaces)
            
            cleaned_text = [re.sub(r'[.,:;]', '', line.strip()) for line in text_lines if line.strip()]

            pdf_text.extend(cleaned_text)

        return pdf_text
    
def count_repetitions(pdf_text: list[str], dict_phrases: list[str]) -> dict[str, int]:
    repeated_phrase: dict[str, int] = {phrase: 0 for phrase in dict_phrases}
    
    for phrase in repeated_phrase:
        for text in pdf_text:
            repeated_phrase[phrase] += text.lower().count(phrase.lower())

    return repeated_phrase

def write_file_txt(phrases_repetitions: dict[str, int], output_file: str) -> None:
    with open(output_file, 'w') as file:
        for phrase, repetitions in phrases_repetitions.items():
            file.write(f'"{phrase}" aparece {repetitions} veces.\n')

def main() -> None:
    root = tk.Tk()
    root.withdraw()

    print("Select a PDF file")
    pdf_file: str = filedialog.askopenfilename(title="Select a PDF file", filetypes = [("PDF Files", "*.pdf")])
    if not pdf_file:
        print("No file selected")
        return

    print("Select a PDF file as dictionary")
    pdf_dictionary: str = filedialog.askopenfilename(title="Select a PDF file", filetypes = [("PDF Files", "*.pdf")])
    if not pdf_dictionary:
        print("No file selected")
        return
    
    pdf_text: list[str] = extract_text_from_pdf(pdf_file)
    dict_phrases: list[str] = extract_text_from_pdf(pdf_dictionary)

    phrases_repetitions: dict[str, int] = count_repetitions(pdf_text, dict_phrases)

    output_file: str = "repeticiones.txt"
    write_file_txt(phrases_repetitions, output_file)
    
if __name__ == '__main__':
    main()