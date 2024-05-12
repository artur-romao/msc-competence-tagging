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

file = "data/LastDadosUC.xlsx"
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

dpucs = {}

# Construct dpucs dictionary with desired fields
for index, row in df.iterrows():
    course_id = row['CodigoPACO']
    if course_id not in dpucs.keys():
        dpucs[course_id] = {}
    dpucs[course_id]['Name'] = row['Title']
    dpucs[course_id]['Url'] = row['Url']
    dpucs[course_id]['Objectives'] = remove_html_tags(row['Objectivos'])
    dpucs[course_id]['Contents'] = remove_html_tags(row['Programa'])

# For now we'll try without tokenizing, afterwards we'll see

""" for course_name, info in dpucs.items():
    for field, field_info in info.items():
        if isinstance(field_info, float): # When the cell is empty, the remove_html_tags method returns nan and transforms the value in float
            field_info = ""
        tokenized_text = nltk.word_tokenize(field_info)
        sentence = ' '.join([re.sub(r'[^a-zA-Z\s]', '', str(s)) for s in tokenized_text])
        dpucs[course_name][field] = ' '.join(dict.fromkeys(sentence.split())) """

dpucs_json = json.dumps(dpucs, indent=4)

data = json.loads(dpucs_json)

# Transform the JSON data into a suitable format for pandas
transformed_data = []
for key in data:
    row = {'ID': key}
    row.update(data[key])
    transformed_data.append(row)

# Create a DataFrame
df = pd.DataFrame(transformed_data)

# Export to Excel
df.to_excel('data/dpucs_for_tagging.xlsx', index=False)