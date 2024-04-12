import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
import re

def select_file(title: str, filetypes: list[tuple[str, str]]) -> str:
    root = tk.Tk()
    root.withdraw()

    print(f'Select a {title}')
    file_path: str = filedialog.askopenfilename(title = f'Select a {title} file', filetypes = filetypes)
    if not file_path:
        print("No file selected")
        return ''
    
    return file_path

def extract_text_from_pdf(pdf_file: str) -> list[str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PdfReader(pdf, strict = False)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content.strip())

    return pdf_text

def create_dictionary(pdf_text: list[str]) -> dict[str, int]:
    phrases = {}

    for content in pdf_text:
        cleaned_content = re.sub(r'[^\w\s.,:;%]', '', content)

        content_more_spaces = re.sub(r'(?<=\d)(\s*)([A-Z])', r'\1 \2', cleaned_content)

        text_lines = re.split(r'(?<=[.,:;])\s+|\s{2,}', content_more_spaces)

        cleaned_text = [re.sub(r'[.,:;]', '', line.strip()) for line in text_lines if line.strip()]

        for phrase in cleaned_text:
            phrases[phrase.lower()] = 0

    return phrases
    
def count_repetitions(pdf_text: list[str], dict_phrases: dict[str, int]) -> dict[str, int]:
    phrase_repetition = dict_phrases.copy()
    
    for phrase in phrase_repetition:
        for text in pdf_text:
            phrase_repetition[phrase] += text.lower().count(phrase)

    return phrase_repetition

def write_file_txt(phrases_repetitions: dict[str, int], output_file: str) -> None:
    with open(output_file, 'w') as file:
        for phrase, repetitions in phrases_repetitions.items():
            file.write(f'"{phrase}" aparece {repetitions} veces.\n')

def main() -> None:
    pdf_file: str = select_file('PDF', [('PDF Files', '*.pdf')])
    if not pdf_file:
        return
    
    pdf_dictionary: str = select_file('PDF dictionary', [('PDF Files', '*.pdf')])
    if not pdf_dictionary:
        return
    
    pdf_text: list[str] = extract_text_from_pdf(pdf_file)
    dict_text: list[str] = extract_text_from_pdf(pdf_dictionary)

    dict_phrases: dict[str, int] = create_dictionary(dict_text)
    phrases_repetitions: dict[str, int] = count_repetitions(pdf_text, dict_phrases)

    output_file: str = "repeticiones.txt"
    write_file_txt(phrases_repetitions, output_file)
    
if __name__ == '__main__':
    main()