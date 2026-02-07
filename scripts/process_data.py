import os
import re
import unicodedata
from num2words import num2words

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "inputs", "speaker1")

ABBREVIATIONS = {
    "S.J.C.": "S J C",
    "U.S.": "U S",
    "MR.": "MISTER",
    "DR.": "DOCTOR",
    "MRS.": "MISSUS"
}

def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

def expand_numbers_and_years(text):
    def replace_match(match):
        number_str = match.group()
        try:
            val = int(number_str)
            if 1900 <= val <= 2099:
                return num2words(val, to='year')
            return num2words(val)
        except ValueError:
            return number_str

    return re.sub(r'\d+', replace_match, text)

def clean_punctuation(text):
    for abbr, expanded in ABBREVIATIONS.items():
        pattern = re.compile(re.escape(abbr), re.IGNORECASE)
        text = pattern.sub(expanded, text)

    text = re.sub(r'[^\w\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def process_pipeline(text):
    text = normalize_text(text)
    text = expand_numbers_and_years(text)
    text = clean_punctuation(text)
    return text.upper()

def main():
    print(f"Starting data processing in: {INPUT_DIR}")

    if not os.path.exists(INPUT_DIR):
        print(f"Error: Directory not found: {INPUT_DIR}")
        return

    files_processed = 0
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".txt"):
            file_path = os.path.join(INPUT_DIR, filename)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    original = f.read()

                cleaned = process_pipeline(original)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)

                print(f"Processed: {filename}")
                files_processed += 1
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    print(f"Completed. Total files processed: {files_processed}")

if __name__ == "__main__":
    main()
