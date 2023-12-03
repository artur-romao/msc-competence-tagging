from pycookiecheat import chrome_cookies
from bardapi import BardCookies

COURSE_DIRECTOR_PROMPT = "I want you to assume the paper of a University Course Director that, given the name of a course, its objectives, contents and learning outcomes, wants the list of ESCO competences associated to that course. You will be responsible to return that list. Is that ok?"
HR_REPRESENTATIVE_PROMPT = "I want you to assume the paper of a company's HR Representative that, given the name and description of a specific job offer, wants the list of ESCO competences associated to that job. You will be responsible to return that list. Is that ok?"
BARD_URL = "https://bard.google.com/"

bard_cookies = chrome_cookies(BARD_URL)
cookies = {'__Secure-1PSID': bard_cookies['__Secure-1PSID'], '__Secure-1PSIDTS': bard_cookies['__Secure-1PSIDTS']}
bard = BardCookies(cookie_dict=cookies, token_from_browser=True)