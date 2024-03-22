from pycookiecheat import firefox_cookies
#from bardapi import BardCookies
from gemini import Gemini
from dotenv import load_dotenv
import os

# For LLM testing
#COURSE_DIRECTOR_PROMPT = "I want you to assume the paper of a University Course Director that, given the name of a course (in portuguese but this you can translate), its objectives and contents, processes that information. In the next prompt, the information related to that course will be provided, you will be responsible to process the information, you should not answer anything rather than 'information processed'. Is that ok?"
#HR_REPRESENTATIVE_PROMPT = "I want you to assume the paper of a company's HR Representative that, given the name and description of a specific job offer, wants the list of ESCO competences associated to that job. You will be responsible to return that list. Is that ok?"
#BARD_URL = "https://gemini.google.com/app"
load_dotenv()

TAGGING_POSTGRES_DB = os.getenv('TAGGING_POSTGRES_DB')
TAGGING_POSTGRES_USER = os.getenv('TAGGING_POSTGRES_USER')
TAGGING_POSTGRES_PASSWORD = os.getenv('TAGGING_POSTGRES_PASSWORD')

ESCO_API_ENDPOINT = "http://esco_api:8080/search"
ESCO_API_LANG = "en"
FLOWISE_MATCHER_API_URL = "http://flowise:5000/api/v1/prediction/e9aaf512-9142-4a9a-b357-70b69f84731f"
FLOWISE_SHORTER_API_URL = "http://flowise:5000/api/v1/prediction/eb6d81f6-95ab-44e2-b970-71d514198f3a"
TAGGING_UI_URL = "http://tagging-ui:3000/"

#bard_cookies = firefox_cookies(BARD_URL)
#cookies = {'__Secure-1PSID': bard_cookies['__Secure-1PSID'], '__Secure-1PSIDTS': bard_cookies['__Secure-1PSIDTS']}
#bard = BardCookies(cookie_dict=cookies, token_from_browser=True)
#GeminiClient = Gemini(cookies=bard_cookies)
#prompt = "Hello, Gemini. What's the weather like in Seoul today?"
#response = GeminiClient.generate_content(prompt)
#print(response)

# For fetching DPUC information
COLUMNS_TO_EXTRACT = ['TextoEN']
FIELDS_TO_EXTRACT = ['Conteudos', 'Objetivos'] # There are not Learning Outcomes