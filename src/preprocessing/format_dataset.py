import pandas as pd

RAW_DATA_DIRECTORY = 'data\\raw'

def load_and_process_data(file_path, rename_dict, replace_dict, drop_cols, concat_cols):
    df = pd.read_csv(file_path)
    df = df.rename(columns=rename_dict)
    for col, replace_values in replace_dict.items():
        df[col] = df[col].map(replace_values)
    if concat_cols:
        df[concat_cols['new_col']] = df[concat_cols['cols']].apply(lambda row: ' '.join([f"{col.upper()}:{val}" for col, val in zip(row.index, row.values)]), axis=1)
    
    df = df[df['Class'].isin(['Legit', 'Phishing'])]
    df = df.drop(columns=drop_cols)
    return df



def get_data():

    data_files = {
        'fraud': {
            'file_path': f"{RAW_DATA_DIRECTORY}/fraud_email_.csv",
            'rename_dict': {'Text': "Email"},
            'replace_dict': {'Class': {0:'Legit', 1:'Phishing'}},
            'drop_cols': [],
            'concat_cols': None
        },
        'human_generated_phishing': {
            'file_path': f"{RAW_DATA_DIRECTORY}/human-generated-phishing.csv",
            'rename_dict': {'body': 'Email', 'label':'Class'},
            'replace_dict': {'Class': {1:'Phishing'}},
            'drop_cols': ['date', 'urls', 'sender', 'receiver', 'subject'],
            'concat_cols': {'new_col': 'Email', 'cols': ['sender', 'subject', 'Email']}
        },
        'human_generated_legit': {
            'file_path': f"{RAW_DATA_DIRECTORY}/human-generated-legit.csv",
            'rename_dict': {'body':'Email', 'label':'Class'},
            'replace_dict': {'Class': {0:'Legit'}},
            'drop_cols': ['date', 'urls', 'sender', 'receiver', 'subject'],
            'concat_cols': {'new_col': 'Email', 'cols': ['sender', 'subject', 'Email']}
        },
        'phishing_data_by_type': {
            'file_path': f"{RAW_DATA_DIRECTORY}/phishing_data_by_type.csv",
            'rename_dict': {'Text': 'Email', 'Type': 'Class'},
            'replace_dict': {'Class': {'Fraud': 'Phishing', "False Positives ": 'Legit'}},
            'drop_cols': ['Subject'],
            'concat_cols': {'new_col': 'Email', 'cols': ['Subject', 'Email']}
        },
        'from_eml': {
            'file_path': f"{RAW_DATA_DIRECTORY}/output_from_eml.csv",
            'rename_dict': {'body':'Email'},
            'replace_dict': {'Class': {1: 'Phishing'}},
            'drop_cols': ['Unnamed: 0', 'fileName', 'subject', 'from'],
            'concat_cols': {'new_col': 'Email', 'cols': ['subject', 'from', 'Email']}
        },
        'traditional_phishing': {
            'file_path': f"{RAW_DATA_DIRECTORY}/traditional_phishing.csv",
            'rename_dict': {'email_body':'Email'},
            'replace_dict': {'Class': {1: 'Phishing'}},
            'drop_cols': ['email_subject', 'id'],
            'concat_cols': {'new_col': 'Email', 'cols': ['email_subject', 'Email']}
        },
        'spear_phishing': {
            'file_path': f"{RAW_DATA_DIRECTORY}/spear_phishing.csv",
            'rename_dict': {'email_body':'Email'},
            'replace_dict': {'Class': {1: 'Phishing'}},
            'drop_cols': ['email_subject', 'sender_name'],
            'concat_cols': {'new_col': 'Email', 'cols': ['email_subject', 'Email']}
        },
        'spam_nonspam': {
            'file_path': f"{RAW_DATA_DIRECTORY}/dataset_spam_nonspam.csv",
            'rename_dict': {'email':'Email', 'category':'Class'},
            'replace_dict': {'Class': {'not-spam':'Legit'}},
            'drop_cols': [],
            'concat_cols': None
        }
    }

    dataframes = {name: load_and_process_data(**params) for name, params in data_files.items()}


    return dataframes


