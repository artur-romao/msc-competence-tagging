from pycookiecheat import chrome_cookies
from bardapi import BardCookies

# For LLM testing
COURSE_DIRECTOR_PROMPT = "I want you to assume the paper of a University Course Director that, given the name of a course (in portuguese but this you can translate), its objectives and contents, processes that information. In the next prompt, the information related to that course will be provided, you will be responsible to process the information, you should not answer anything rather than 'information processed'. Is that ok?"
HR_REPRESENTATIVE_PROMPT = "I want you to assume the paper of a company's HR Representative that, given the name and description of a specific job offer, wants the list of ESCO competences associated to that job. You will be responsible to return that list. Is that ok?"
BARD_URL = "https://bard.google.com/"

bard_cookies = chrome_cookies(BARD_URL)
cookies = {'__Secure-1PSID': bard_cookies['__Secure-1PSID'], '__Secure-1PSIDTS': bard_cookies['__Secure-1PSIDTS']}
bard = BardCookies(cookie_dict=cookies, token_from_browser=True)

# For fetching DPUC information
COLUMNS_TO_EXTRACT = ['TextoEN']
FIELDS_TO_EXTRACT = ['Conteudos', 'Objetivos'] # There are not Learning Outcomes