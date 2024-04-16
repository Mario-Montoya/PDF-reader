import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
import re
from fpdf import FPDF

def select_file(title: str, filetypes: tuple[str, str]) -> str:
    root = tk.Tk()
    root.withdraw()

    print(f'Select a {title}')
    file_path: str = filedialog.askopenfilename(title = f'Select a {title} file', filetypes = [filetypes])
    
    if not file_path:
        print("No file selected")
        return ''
    
    return file_path

def select_file_output(title: str, filetypes: tuple[str, str]) -> str:
    root = tk.Tk()
    root.withdraw()

    file_path: str = filedialog.asksaveasfilename(initialfile = title, filetypes = [filetypes])

    if not file_path:
        print("No location selected")
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

    all_content = '  '.join(pdf_text)
    
    cleaned_content = re.sub(r'[^\w\s.,:;()<>+\-\[\]]', '', all_content)
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
    
def count_repetitions(pdf_text: list[str], dict_phrases: dict[str, int], dict_words: dict[str, int]) -> dict[str, int]:
    phrase_repetition = dict_phrases.copy()
    word_repetition = dict_words.copy()
    
    for text in pdf_text:
        for phrase in phrase_repetition:
            phrase_repetition[phrase] += text.lower().count(phrase.lower())

        for word in word_repetition:
            word_repetition[word] += text.lower().count(word.lower())

    return phrase_repetition, word_repetition

def write_file_pdf(dictionary: dict[str, int], output_file: str, sort: bool = False) -> None:
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size = 10)

        for key, value in sorted(dictionary.items()) if sort else dictionary.items():
            text = f'"{key}" aparece {value} veces.'
            pdf.multi_cell(0, 5, txt = text)

        pdf.output(output_file)
        print(f'Results written to {output_file}')

    except Exception as e:
        print(f'Error: Failed to write results to PDF file: {e}')

def main() -> None:
    pdf_file: str = select_file('PDF', ('PDF Files', '*.pdf'))
    if not pdf_file:
        return
    
    pdf_dictionary: str = select_file('PDF dictionary', ('PDF Files', '*.pdf'))
    if not pdf_dictionary:
        return
    
    pdf_text: list[str] = extract_text_from_pdf(pdf_file)
    if not pdf_text:
        print('No text extracted from PDF. Exiting program')
        return
    
    dict_text: list[str] = extract_text_from_pdf(pdf_dictionary)
    if not dict_text:
        print('No text extracted from PDF dictionary. Exiting program')
        return

    dict_phrases, dict_words = create_dictionary(dict_text)
    phrases_repetitions, words_repetitions = count_repetitions(pdf_text, dict_phrases, dict_words)

    phrases_output_file: str = select_file_output('phrases_repetitions', ('PDF Files', '*.pdf'))
    if not phrases_output_file:
        return
    
    words_output_file: str = select_file_output('words_repetitions', ('PDF Files', '*.pdf'))
    if not words_output_file:
        return

    write_file_pdf(phrases_repetitions, phrases_output_file)
    write_file_pdf(words_repetitions, words_output_file, True)
    
if __name__ == '__main__':
    main()