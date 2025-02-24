# AI-Powered Phishing Email Detection System

This project provides an automated system for detecting phishing attempts in emails using multiple AI language models. It processes raw email data through comprehensive preprocessing steps and leverages advanced language models like LLaMA and Mistral to analyze emails for phishing indicators, providing detailed risk assessments and explanations.

The system excels at identifying social engineering elements and assessing risk levels in email communications. It supports multiple email formats (EML, JSON, CSV) and implements robust data cleaning and preprocessing to ensure high-quality analysis. The system uses a multi-model approach with LLaMA 3.1 70B, Gemma 2 9B, LLaMA 3 8B, and Mistral Large for comprehensive phishing detection.

The complete analysis and discussion can be found in the paper:  
https://doi.org/10.48550/arXiv.2502.04759

## Repository Structure
```
.
├── data
│   ├── processed      # The final, canonical data sets for modeling
│   └── raw            # The original, immutable data dump
└── src
    ├── evaluation/
    │   └── evaluation.py          # Core analysis logic using AI models
    ├── generate_dataset/
    │   ├── convert_eml_to_csv.py  # Converts email files to CSV format
    │   └── json_to_csv.py         # Converts JSON data to CSV format
    └── preprocessing/
        ├── custom.py              # Custom HTML processing utilities
        ├── format_dataset.py      # Dataset formatting and standardization
        └── preprocessing.py       # Email cleaning and preprocessing pipeline
```

## Usage Instructions
### Prerequisites
- Python 3.8 or above
- API keys for:
  - Groq (LLaMA and Gemma models)
  - Mistral AI
- Environment variables configured in `.env` file

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install required packages
pip install pandas numpy tqdm openai instructor python-dotenv html2text pydantic seaborn

# Set up environment variables
echo "groq_api=<your-groq-api-url>" > .env
echo "groq_api_key=<your-groq-api-key>" >> .env
echo "mistral_api=<your-mistral-api-url>" >> .env
echo "mistral_api_key=<your-mistral-api-key>" >> .env
```

### Quick Start
1. Prepare your email data in one of the supported formats (EML, JSON, or CSV)
2. Convert and preprocess the data:
```python
# Convert EML files to CSV
python generate_dataset/convert_eml_to_csv.py

# Preprocess the data
python preprocessing/preprocessing.py
```

3. Run the phishing analysis:
```python
# Analyze emails using multiple models
python evaluation/evaluation.py
```

### More Detailed Examples
#### Processing Raw Email Files
```python
from generate_dataset.convert_eml_to_csv import extract_subject_and_body

# Process a single email file
subject, from_email, content = extract_subject_and_body('path/to/email.eml')
```

#### Custom Preprocessing
```python
from preprocessing.preprocessing import clean_email_body

# Clean email content
cleaned_email = clean_email_body(email_content)
```

### Troubleshooting
#### Common Issues
1. API Authentication Errors
   - Error: "Authentication failed for API endpoint"
   - Solution: Verify API keys in `.env` file
   - Check environment variable loading: `print(os.getenv('groq_api_key'))`

2. Email Processing Errors
   - Error: "UnicodeDecodeError" during email parsing
   - Solution: Use the safe processing method:
   ```python
   from preprocessing.preprocessing import clean_email_body_safe
   cleaned_content = clean_email_body_safe(problematic_email)
   ```

3. Memory Issues with Large Datasets
   - Error: "MemoryError" when processing large files
   - Solution: Process data in chunks:
   ```python
   import pandas as pd
   for chunk in pd.read_csv('large_file.csv', chunksize=1000):
       process_chunk(chunk)
   ```

## Data Flow
The system processes emails through a pipeline of preprocessing, cleaning, and AI analysis to detect phishing attempts.

```ascii
Raw Email Data (EML/JSON/CSV)
         ↓
Data Conversion & Standardization
         ↓
Preprocessing & Cleaning
    → Remove HTML
    → Decode MIME/Base64
    → Clean text
         ↓
AI Model Analysis
    → LLaMA/Gemma/Mistral
         ↓
Phishing Detection Results
```

Key component interactions:
1. Data ingestion supports multiple formats through dedicated converters
2. Preprocessing pipeline applies multiple cleaning steps sequentially
3. AI models run in parallel for comprehensive analysis
4. Results are aggregated and stored in CSV format
5. Error handling and progress tracking throughout the pipeline
6. Automatic checkpointing every 100 emails processed
7. Support for resuming interrupted analysis sessions