import sys
import io
import os
import pandas as pd
from email import policy
from email.parser import BytesParser
import html2text
import re
from urllib.parse import urlparse
import quopri



def extract_subject_and_body(eml_path):

    with open(eml_path, 'rb') as f:
        #msg = email.message_from_binary_file(f) # for all error eml
        msg = BytesParser(policy=policy.default).parse(f)
        
    subject = msg['subject']
    from_email = msg['From']
    content = ''
    
    for part in msg.walk():
        
        if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
            
            if part['Content-Transfer-Encoding'] == 'quoted-printable':
                payload = part.get_payload()
                charset = part.get_content_charset() if part.get_content_charset() else 'utf-8'
                try:
                    payload = quopri.decodestring(payload.encode('ascii', errors='ignore')).decode(charset, errors='ignore')
                except ValueError:
                    payload = quopri.decodestring(payload.encode('ascii', errors='ignore')).decode('utf-8', errors='ignore')

                content = payload
             
            else:
                content = part.get_content()
       


    return subject, from_email, content



if __name__ == "__main__":

 
    # '''EXCEPTIONS
    # 
    # Email structure not support with BytesParser(policy=policy.default).parse(f)
    # LookupError file: email\sample-2391.eml 
    # LookupError file: email\sample-2428.eml 
    # LookupError file: email\sample-2505.eml 
    # LookupError file: email\sample-2511.eml 
    # LookupError file: email\sample-2541.eml 
    # LookupError file: email\sample-2542.eml
    # LookupError file: email\sample-2551.eml 
    # LookupError file: email\sample-2552.eml
    # LookupError file: email\sample-2554.eml
    # LookupError file: email\sample-2555.eml 
    # # eml: 1024; 1061 attachment


    directory = 'data\\raw\email' 
    if os.path.isfile("data\\raw\output_from_eml.csv"):
        os.remove('data\\raw\output_from_eml.csv')


    def generate_data(directory):
        for filename in os.listdir(directory):
            if filename.endswith('.eml'):
                eml_path = os.path.join(directory, filename)
                subject, from_email, body = extract_subject_and_body(eml_path)
                body = body.strip()
                if body: # don't consider the one that has a empty body
                    yield {'fileName':filename,'subject': subject,'from': from_email ,'body': body, 'Class': 1}

    df = pd.DataFrame(generate_data(directory))
    df.to_csv('data\\raw\output_from_eml.csv', errors='replace')





