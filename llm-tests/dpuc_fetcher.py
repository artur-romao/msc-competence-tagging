import pandas as pd
import nltk
import re
from bs4 import BeautifulSoup
import unicodedata
import json
import requests
from config import FIELDS_TO_EXTRACT, bard, COURSE_DIRECTOR_PROMPT

file = "DPUCS.xlsx"
df = pd.read_excel(file)

column_names = df.columns.tolist()

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


ucs = []


def fetch_ucs(input_file):
    with open(input_file) as f:
        for line in f.readlines():
            ucs.append(line.replace("\n",""))

fetch_ucs("input.txt")
print(ucs, len(ucs))

dpucs = {}

# Construct dpucs dictionary with desired fields
for index, row in df.iterrows():
    if row['Ano'] != 2021 or row['Campo'] not in FIELDS_TO_EXTRACT:
        continue
    elif normalize_text(row['NomeUC']) not in dpucs.keys():
        dpucs[normalize_text(row['NomeUC'])] = {}
    dpucs[normalize_text(row['NomeUC'])][row['Campo']] = remove_html_tags(row['TextoEN'])


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

#print(dpucs_json)

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
df.to_excel('organized_DPUCS.xlsx', index=False)

# Questions
# Should I tokenize? Maybe only after answering we will know... 
# Used a normalizing function to remove accents from words, but should instead translate?

ESCO_API_ENDPOINT = "http://localhost:8080/search"
ESCO_API_LANG = "en"

for nome in ucs:
    tokenized_text = dpucs[nome]["Conteudos"] + " " + dpucs[nome]["Objetivos"]
    skills = []
    print(f"{nome}: {tokenized_text}\n")

    print(COURSE_DIRECTOR_PROMPT)
    print(bard.get_answer(COURSE_DIRECTOR_PROMPT)['content'])

    contents = dpucs[nome]["Conteudos"]
    objectives = dpucs[nome]["Objetivos"]
    query = "Name: " + nome + "\nObjectives: " + objectives + "\nContents: " + contents
    print(query)
    print(bard.get_answer(query)['content'])

    response = requests.get(ESCO_API_ENDPOINT + "?text=" + tokenized_text + "&language=" + ESCO_API_LANG +  "&type=skill&facet=type&facet=isInScheme&full=true&q=computer%20engineering")

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching data from API for {nome}")
    else:
        # Extract the data from the response
        data = response.json()
        # Print the matches and their positions in the text
        for match in data["_embedded"]["results"]:
            skill = match['preferredLabel'][ESCO_API_LANG]
            skills.append(skill)

        query = "Below is a list of ESCO competences for the course " + nome + ", you should take off the ones you consider that don't fit the information you processed in the previous prompt and keep the ones you think that are adequate, return me simply the skills, I don't need descriptions for them:\n\n"
        for skill in skills:
            query = query + skill + "\n"
        print(query)
        print(bard.get_answer(query)['content'])
        # Save skills to a file with a name corresponding to the Nome_EN
        with open(f"1st_semester/{nome}_skills.txt", "w") as f:
            f.write(nome + "\n\n")
            f.write('\n'.join(skills))
            f.write("\n\n-------------------------------------------------")