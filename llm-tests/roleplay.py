from config import bard, COURSE_DIRECTOR_PROMPT, HR_REPRESENTATIVE_PROMPT


def pick_role():
    role = ""
    while (role != "CD" and role != "HR"):
        role = input("Which role do you want me to assume?\n[Course director (CD)]\n[HR representative (HR)]\n").strip().upper()
    return role

def course_director_path():
    print(COURSE_DIRECTOR_PROMPT)
    print(bard.get_answer(COURSE_DIRECTOR_PROMPT)['content'])
    # Below fields hardcoded, change this a posteriori with the code from the other repository
    name = "Metrology 3D"
    objectives = "At the end of the microcredential students should reveal knowledge, skills and competences capable of solving real problems. The microcredential is aimed at students and trainees who are looking for knowledge in the area of metrology of functional parts or associated with the component manufacturing process."
    contents = "Understanding GD & T tolerance and 3D Metrology, Coordinate measuring systems, Calibration, measurement errors and their propagation, Normalization, Reading of the project, Measurement plan, Post-processing of functional parts CNC machines Automatic tool calibration systems Centering systems Positioning systems Dimensional control systems Geometric control systems Finishing techniques for CNC machining , Effective 3D metrology techniques Fundamentals of 3D measurement Control systems Contact measuring systems Non-contact measuring systems Coordinate measuring machines Preparation of measuring systems Alignment methods Parts measurement techniques CMM operation and programming Treatment of results"
    learning_outcomes = "Tolerance GD & T, Design of parts, Manufacture of parts, Finishing of functional parts, Principles of tolerance GD & T, 3D measurement, Coordinate measuring machines, Solution proposal, Non-contact techniques, Functional parts"
    query = "Name: " + name + "\nObjectives: " + objectives + "\nContents: " + contents + "\nLearning outcomes: " + learning_outcomes
    print(query)
    print(bard.get_answer(query)['content'])
    query = "I think you are missing the point. Those are not ESCO skills. An example of an ESCO skill would be 'interpret geometric dimensions and tolerances', can you find them or not really?"
    print(query)
    print(bard.get_answer(query)['content'])

def hr_representative_path():
    print(HR_REPRESENTATIVE_PROMPT)
    print(bard.get_answer(HR_REPRESENTATIVE_PROMPT)['content'])
    name = "Software developer"
    description = "Design, develop, and implement software solutions in collaboration with a cross-functional team.; Write clean, scalable, and well-documented code.; Participate in all phases of the software development lifecycle, including analysis, design, testing, and integration.; Troubleshoot, debug, and upgrade existing software.; Engage with stakeholders to understand their requirements and provide technical solutions.; Stay abreast of new technology trends and incorporate them into our software practices."
    query = "Name: " + name + "\nDescription: " + description
    print(query)
    print(bard.get_answer(query)['content'])

role = pick_role()

if role == "CD":
    course_director_path()
elif role == "HR":
    hr_representative_path()