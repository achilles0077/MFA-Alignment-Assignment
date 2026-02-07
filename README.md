# Speech & AIML: Forced Alignment Pipeline

## 1. Project Overview
In this project, I built a forced alignment pipeline using the **Montreal Forced Aligner (MFA)**. The main challenge with the dataset was "messy" text—specifically raw numbers and proper names that don't exist in standard dictionaries. To fix this, I wrote a custom pre-processing script to handle the numbers and used a G2P (Grapheme-to-Phoneme) model to generate pronunciations for unknown names (OOVs). This ensures the alignment is actually accurate rather than just skipping difficult words.

## 2. Environment Setup & Installation
MFA relies on some heavy dependencies (like Kaldi and OpenFST) that often break if you install them alongside other system libraries. To avoid headaches, I highly recommend using a fresh Conda environment with Python 3.9.

```bash
# 1. Create and activate a clean environment
conda create -n ltrc_aligner python=3.9 -y
conda activate ltrc_aligner

# 2. Install core MFA and pre-processing dependencies
# I used conda-forge here to make sure the non-python binaries link correctly
conda install -c conda-forge montreal-forced-aligner num2words -y

# 3. Download the required acoustic model, dictionary, and G2P model
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
mfa model download g2p english_us_arpa

```

## 3. Data Preparation & Pre-processing

Standard aligners struggle with raw text because they don't know how to pronounce digits like "1976" or abbreviations like "Dr." unless they are converted to words first.

I wrote a sanitization script (`scripts/process_data.py`) to clean up the text before feeding it to MFA. Here is what it does:

* **Standardization**: Cleans up the text to ASCII and removes weird symbols.
* **Smart Number Conversion**: Uses `num2words` to convert digits into spoken words.
* **Years (1900-2099)**: Reads them as years (e.g., `1976` becomes `nineteen seventy six`).
* **Counts**: Reads them as normal numbers (e.g., `300` becomes `three hundred`).


* **Abbreviations**: Expands common shorthands (e.g., converts `S.J.C.` to `S J C` and `Dr.` to `Doctor`).
* **Formatting**: Strips punctuation and converts everything to uppercase so it matches the dictionary format.

**To run the cleanup:**

```bash
python scripts/process_data.py

```

## 4. Execution Pipeline

To demonstrate the improvements, I ran the alignment in two stages: a baseline run (without fixes) and the final run (with fixes).

### Step 1: Baseline Run (The "Before" State)

First, I ran the aligner on the raw text *without* the G2P model. This generates the `outputs_before` folder, where you can see the initial failures (gaps and `<unk>` labels).

```bash
# Run without G2P and pointing to the raw inputs
mfa align inputs english_us_arpa english_us_arpa outputs_before --clean

```

### Step 2: Final Run (The "After" State)

Next, I ran the full pipeline using the cleaned text and the G2P model. This generates the `outputs_after` folder with the correct, high-quality TextGrids.

```bash
# Run WITH G2P model to handle names like "Dukakis"
mfa align inputs english_us_arpa english_us_arpa outputs_after --g2p_model_path english_us_arpa --clean

```

## 5. Comparative Analysis (Key Observations)

After running the alignment, I manually checked the results in Praat to verify boundary accuracy for difficult cases.

### A. OOV Handling Success

* **Baseline**: Without the G2P model, proper names were just marked as `<unk>` or `spn` (spoken noise), leaving big gaps in the alignment.
* **Improved**: With G2P enabled, the model successfully broke down "Dukakis" into its phonemes: `D UW K AA1 K IH0 S`.


## 6. Repository Structure

* `inputs/`: Contains the original audio files and transcripts organized by speaker.
* `outputs_before/`: Baseline results—this folder holds the TextGrids generated *without* the G2P model.
* `outputs_after/`: Final results—this contains the accurate TextGrids generated *after* applying the G2P model.
* `scripts/`: The Python code used to fix numbers and abbreviations.
* `requirements.txt`: The list of libraries needed to run the project.

