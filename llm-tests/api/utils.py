import pandas as pd
import nltk
from bs4 import BeautifulSoup
import unicodedata
import re
import json

##############################################################################
##   This utils file contains code to process the information coming from   ##
##        Pedagogical Dossiers of University of Aveiro and create an        ##
##                      organized Excel file for it                         ##
##############################################################################

FIELDS_TO_EXTRACT = ['Conteudos', 'Objetivos']
file = "data/DPUCS.xlsx"
df = pd.read_excel(file)

column_names = df.columns.tolist()

#nltk.download('stopwords')
#nltk.download('punkt')
stopwords_en = nltk.corpus.stopwords.words('english')

# Define a function to remove HTML tags from a cell
def remove_html_tags(text):
    if isinstance(text, str):
        soup = BeautifulSoup(text, 'html.parser')
        cleaned_text = soup.get_text()
        cleaned_text = cleaned_text.replace(u'\xa0', u'')
        return cleaned_text
    else:
        return text
    

def normalize_text(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('utf-8')

#df['NomeUC_Normalized'] = df['NomeUC'].apply(normalize_text)
latest_years = df.groupby('NomeUC')['Ano'].max().to_dict()
dpucs = {}

# Construct dpucs dictionary with desired fields
for index, row in df.iterrows():
    course_name = row['NomeUC']
    if row['Ano'] == latest_years[course_name] and row['Campo'] in FIELDS_TO_EXTRACT:
        if course_name not in dpucs:
            dpucs[course_name] = {}
        dpucs[course_name][row['Campo']] = remove_html_tags(row['TextoEN'])
print(len(dpucs.keys()))
# Tokenize the content of the dictionary dpucs
for course_name, info in dpucs.items():
    for field, field_info in info.items():
        if isinstance(field_info, float): # When the cell is empty, the remove_html_tags method returns nan and transforms the value in float
            field_info = ""
        tokenized_text = nltk.word_tokenize(field_info)
        sentence = ' '.join([re.sub(r'[^a-zA-Z\s]', '', str(s)) for s in tokenized_text])
        dpucs[course_name][field] = ' '.join(dict.fromkeys(sentence.split()))

# Convert the dictionary to json
dpucs_json = json.dumps(dpucs, indent=4)

data = json.loads(dpucs_json)

# Transform the JSON data into a suitable format for pandas
transformed_data = []
for key in data:
    row = {'Name': key}
    row.update(data[key])
    transformed_data.append(row)

# Create a DataFrame
df = pd.DataFrame(transformed_data)

# Rename columns
df = df.rename(columns={'Conteudos': 'Contents', 'Objetivos': 'Objectives'})

# Export to Excel
df.to_excel('data/organized_DPUCS.xlsx', index=False)