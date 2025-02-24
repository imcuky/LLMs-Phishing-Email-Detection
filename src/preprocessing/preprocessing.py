from custom import CustomHTML2Text

from format_dataset import get_data

import pandas as pd
import numpy as np
import os
import base64
import re
import sys

SAVE_DATA_DIRECTORY = 'data\\processed'
RAW_DATA_DIRECTORY = 'data\\raw'


def data_cleaning(df_list):
    email_df = pd.DataFrame()

    for name, df in df_list.items():
        email_df = pd.concat([email_df, df], ignore_index=True)

    email_df['Email'] = email_df['Email'].astype('str').apply(clean_email_body_safe)

    email_df = email_df.dropna().drop_duplicates().sample(frac=1).reset_index(drop=True)

    return email_df

def remove_emojis(text: str) -> str:
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"  # dingbats
                               u"\U000024C2-\U0001F251"  # enclosed characters
                               u"\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
                               u"\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
                               u"\U0001F018-\U0001F270"  # various additional symbols
                               u"\U0001F650-\U0001F67F"  # ornately decorated symbols
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def decode_mime(header:str) -> str:
    # Search for the pattern ?xx?B?xx?
    matches = re.findall(r'\?(.*?)\?B\?(.*?)\?', header, re.IGNORECASE)

    for match in matches:
        encoding, encoded_string = match
        # Decode the string using the detected encoding
        decoded_string = decode_base64(encoded_string)
        # Replace the encoded string with the decoded string in the header
        header = header.replace(f'?{encoding}?B?{encoded_string}?', decoded_string)

    return header


def decode_base64(email:str) -> str:
    
    
    if re.fullmatch(r'[A-Za-z0-9+/]+={0,2}', email[:20]):
        
        try:

            length = len(email)
            length -= length % 4
            parts = email[:length]
            email_decoded = base64.b64decode(parts).decode('iso-8859-1')

            return email_decoded
            
        except Exception as e:
            
            #print(f"Error in decoding base64: {e}")
            return email #
    else:
        return email


def clean_html(e:str) -> str:

    h = CustomHTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.images_as_html = True
    h.ignore_tables = True
    h.body_width = 0
    h.ignore_emphasis = True

    clean = h.handle(e)

    return clean

def clean_string(e: str) -> str:
    clean = re.sub(r'[\r\n\t\s]+', ' ', e)
    # clean = re.sub(r'\s+', ' ', clean)
    clean = re.sub(r'[*_=,!<>#-]', '', clean).strip()

    return clean


def clean_email_body_safe(email:str) -> str|None:
    try:
        return clean_email_body(email)
    except Exception as e:
        # print(f"Error processing email: {email}")
        # print(f"Error message: {e}")
        return np.nan
    
def clean_email_body(e: str) -> str:
    
    clean = decode_base64(e)

    clean = decode_mime(clean)
    
    clean = clean_html(clean)

    clean = remove_emojis(clean)

    clean = clean_string(clean)

    if clean.count(" ") == 0:
        clean = np.nan

    return clean

def limit_words(email, word_limit=500):
    words = email.split()
    return ' '.join(words[:word_limit])


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    list_df = get_data()


    if os.path.isfile(f"{SAVE_DATA_DIRECTORY}\\df_email.csv"):
        os.remove(f'{SAVE_DATA_DIRECTORY}\\df_email.csv')

    email_df = data_cleaning(list_df)
    
    email_df = email_df[(email_df["Email"].apply(len) >= 500) & (email_df["Email"].apply(len) <= 2000)].reset_index(drop=True)

    email_df.to_csv(f'{SAVE_DATA_DIRECTORY}\\df_email.csv', index=True, escapechar='\\')




