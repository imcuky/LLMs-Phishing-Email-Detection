import pandas as pd
import json
import os
import html2text
import glob

RAW_DATA_DIRECTORY = 'data\\raw'

def generate_data(directory):
    data_list = []
  
    json_files = glob.glob(os.path.join(directory, '*.json'))

    data_list = [json.load(open(json_file)) for json_file in json_files]

    df = pd.DataFrame(data_list)

    df['Class'] = 1

    df.to_csv(f'{directory}.csv', index=False)


if __name__ == '__main__':
    
    directory1 = f'{RAW_DATA_DIRECTORY}\\spear_phishing'
    directory2 = f'{RAW_DATA_DIRECTORY}\\traditional_phishing'

    
    if os.path.isfile(f"{directory1}.csv"):
        os.remove(f"{directory1}.csv")

    if os.path.isfile(f"{directory2}.csv"):
        os.remove(f"{directory2}.csv")

    generate_data(directory1)

    generate_data(directory2)