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
    try:
        with open(pdf_file, 'rb') as pdf:
            reader = PdfReader(pdf, strict = False)
            pdf_text = [page.extract_text().strip() for page in reader.pages]

    except Exception as e: 
        print(f'Error: Failed to extract text form the PDF: {e}')
        return[]
    
    return pdf_text

def create_dictionary(pdf_text: list[str]) -> dict[str, int]:
    phrases = {}
    words = {}

    for content in pdf_text:
        cleaned_content = re.sub(r'[^\w\s.,:;()<>+\-\[\]]', '', content)

        space_inbetween = re.sub(r'(?<=\d|\w|\))(\s+)([A-Z])', r'\1 \2', cleaned_content)

        text_lines = re.split(r'(?<=[.,:;])\s+|\s{2,}|\d\s(?=\d)', space_inbetween)

        for line in text_lines:
            line = re.sub(r'[,:;]|(?<!\d)\.(?![a-z])', '', line.strip())
            
            if line and not re.match(r'^\d', line):
                phrases[line] = 0

            words_in_line = re.findall(r'\b[A-Za-z]{2,}\b', line)
            for word in words_in_line:
                words[word] = 0

    return phrases, words
    
def count_repetitions(pdf_text: list[str], dict_phrases: dict[str, int]) -> dict[str, int]:
    phrase_repetition = dict_phrases.copy()
    
    for phrase in phrase_repetition:
        for text in pdf_text:
            phrase_repetition[phrase] += text.lower().count(phrase.lower())

    return phrase_repetition

def write_file_txt(phrases_repetitions: dict[str, int], output_file: str) -> None:
    try:
        with open(output_file, 'w') as file:
            for phrase, repetitions in phrases_repetitions.items():
                file.write(f'"{phrase}" aparece {repetitions} veces.\n')

        print(f'Results written to {output_file}')
    
    except Exception as e: 
        print(f'Error: Failed to write results to file: {e}')

def main() -> None:
    pdf_file: str = select_file('PDF', [('PDF Files', '*.pdf')])
    if not pdf_file:
        return
    
    pdf_dictionary: str = select_file('PDF dictionary', [('PDF Files', '*.pdf')])
    if not pdf_dictionary:
        return
    
    pdf_text: list[str] = extract_text_from_pdf(pdf_file)
    if not pdf_text:
        print('No text extracted from PDF. Exiting program')
        return
    
    dict_text: list[str] = extract_text_from_pdf(pdf_dictionary)
    if not dict_text:
        print('No text extracted from PDF. Exiting program')
        return

    dict_phrases, dict_words = create_dictionary(dict_text)
    phrases_repetitions: dict[str, int] = count_repetitions(pdf_text, dict_phrases)
    words_repetitions: dict[str, int] = count_repetitions(pdf_text, dict_words)

    phrases_output_file: str = 'phrases_repetitions.txt'
    words_output_file: str = 'words_repetitions.txt'
    write_file_txt(phrases_repetitions, phrases_output_file)
    write_file_txt(words_repetitions, words_output_file)
    
if __name__ == '__main__':
    main()