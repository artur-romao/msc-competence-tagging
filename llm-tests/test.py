from pycookiecheat import chrome_cookies
from bardapi import BardCookies

bard_cookies = chrome_cookies("https://bard.google.com/")
cookies = {'__Secure-1PSID': bard_cookies['__Secure-1PSID'], '__Secure-1PSIDTS': bard_cookies['__Secure-1PSIDTS']}
bard = BardCookies(cookie_dict=cookies, token_from_browser=True)

#print(bard.get_answer("What is the capital of France?")['content'])
#print(bard.get_answer("the length of a rectangle is twice its width. Given the length of the diagonal is 5(sqrt(5)), find the area of the rectangle. - a. 2500, b. 2, c. 50, d. 25")['content'])
#print(bard.get_answer("Olá! Como é que estás? Consegues falar em Português de Portugal?")['content'])

query = "Having the following text in consideration, return me a list of keywords that could represent it." \
"At the end of the microcredential students should reveal knowledge, skills and competences capable of solving real problems. The microcredential is aimed at students and trainees who are looking for knowledge in the area of metrology of functional parts or associated with the component manufacturing process.\
3D metrology" \
"GD & T tolerance Coordinate measuring systems Calibration Measurement errors Propagation of errors Normalization Reading project Measurement plan Post-processing of functional parts CNC machines Automatic tool calibration systems Centering systems Positioning systems Dimensional control systems Geometric control systems Finishing techniques for CNC machining  Effective 3D metrology techniques Fundamentals of 3D measurement Control systems Contact measuring systems Non-contact measuring systems Coordinate measuring machines Preparation of measuring systems Alignment methods Parts measurement techniques CMM operation and programming Treatment of results" \
"At the end of the course students should reveal knowledge, skills and competences capable of solving real problems, showing themselves capable of:Know, master and apply the concepts of tolerance GD & T in the design and manufacture of parts.2. Know and master the principles of tolerance GD & T and know how to apply them in the finishing of functional parts3. Know and master the principles of tolerance GD & T and know how to apply them in 3D measurement of functional parts using coordinate measuring machines. Creatively communicate a solution proposal.Know and master the principles of 3D measurement of functional parts using non- contact techniques."

print(bard.get_answer(query)['content'])
print(bard.get_answer("Do you remember what I just asked you? What was the question about?")['content'])
print(bard.get_answer("From the following list of competences, remove the ones that you think that don't fit, having in mind the initial text that I sent you:" \
"manage periodic calibration plans write calibration report log transmitter readings interpret geometric dimensions and tolerances metrology measure parts of manufactured products adjust measuring machines revise quality control systems documentation maintain additive manufacturing systems operate precision measuring equipment program a CNC controller functionalities of machinery power plant instrumentation calibrate waste incinerator use measurement instruments operate paper bag machine control panel components manage railway construction projects tend CNC laser cutting machine calibrate electronic instruments")['content'])