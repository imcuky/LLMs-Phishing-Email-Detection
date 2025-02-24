import instructor
import os
import pandas as pd
import dotenv

from pydantic import BaseModel, Field
from enum import Enum
from typing import List
from openai import OpenAI
from tqdm import tqdm

project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv_path = os.path.join(project_dir, '.env')
dotenv.load_dotenv(dotenv_path)

GROQ_API = os.getenv('groq_api')
MISTRIAL_API = os.getenv('mistral_api')

GROQ_KEY = os.getenv('groq_api_key')
MISTRIAL_KEY = os.getenv('mistral_api_key')

SAVE_DATA_DIRECTORY = r'data\processed'


class risk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Element(BaseModel):
    element: str
    reason: str

class PhishingAnalysis(BaseModel):
    is_phishing: bool
    risk: risk
    social_engineering_elements: List[Element]
    actions: List[str]
    explanation: str


def analyze_email(email_content: str, model: str) -> PhishingAnalysis:

    url = ""
    key = ""
    if model in ["llama-3.1-70b-versatile", 'gemma2-9b-it', 'llama3-8b-8192']:

        url = GROQ_API
        key = GROQ_KEY
    elif model in ["mistral-large-latest"]:
        url = MISTRIAL_API
        key = MISTRIAL_KEY

    client = instructor.from_openai(
      OpenAI(
          base_url=url,
          api_key=key,
      ),
      mode=instructor.Mode.JSON,
    )

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": '''You are a cybersecurity expert specialized in detecting 
                                and analyzing phishing emails. Analyze the provided 
                                email (including subject line, body text, sender 
                                information, and links) to determine whether it is a 
                                phishing email or a legitimate email. Your result must 
                                follow the provided function call.''',
            },
            {
                "role": "user",
                "content": email_content,
            },
        ],
        response_model=PhishingAnalysis,
    )

    return resp


def eval(model:str, testdf_phishing: pd.DataFrame):
    print(f"Analyzing emails using {model}")

    
    results = []
    final_results_file = f'{SAVE_DATA_DIRECTORY}\\final_results_{model}.csv'

    start_index = 0
    df_existing_results = pd.DataFrame()
    # Load existing results if final results file exists
    if os.path.isfile(final_results_file):
        try:
            df_existing_results = pd.read_csv(final_results_file)
            #results = df_existing_results.to_dict('records')
            start_index = len(df_existing_results)
        except Exception as e:
            os.remove(final_results_file)
    else:
        start_index = 0

    for i, email_content in enumerate(tqdm(testdf_phishing['Email'][start_index:], desc="Analyzing emails", initial=start_index)):

        try:
            analysis = analyze_email(email_content, model)
            results.append(analysis)
        except Exception as e:
            print(f"Error analyzing email: {str(e)}")

            # Save progress at intervals if there's an error
            df_results = pd.DataFrame([result.model_dump() for result in results])
            df_results = pd.concat([df_existing_results, df_results], axis=0)
            df_results.to_csv(final_results_file, index=False)
            print(f"Checkpoint saved at {i + 1} emails")
            break

        if (i+1) % 100 == 0:
            df_results = pd.DataFrame([result.model_dump() for result in results])
            df_results = pd.concat([df_existing_results, df_results], axis=0)
            df_results.to_csv(final_results_file, index=False)
            print(f"Checkpoint saved at {i + 1} emails")


    # Save final results
    df_results = pd.DataFrame([result.model_dump() for result in results])
    df_results = pd.concat([df_existing_results, df_results], axis=0)
    df_results.to_csv(final_results_file, index=False)
    print(f"Completed analysis of {len(results)} emails")



if __name__ == '__main__':
    
  testdf_phishing = pd.read_csv(f'{SAVE_DATA_DIRECTORY}\\df_email.csv')

  MODEL1 = "llama-3.1-70b-versatile" # DONE
  eval(MODEL1, testdf_phishing)

  MODEL2 = 'gemma2-9b-it' #DONE
  eval(MODEL2, testdf_phishing)

  MODEL3 = 'llama3-8b-8192'
  eval(MODEL3, testdf_phishing)

  MODEL4 = "mistral-large-latest"
  eval(MODEL4, testdf_phishing)