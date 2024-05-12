import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom'; 
import { createGlobalStyle } from 'styled-components';

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
`;

const Header = styled.header`
  background-color: #0eb4bd;
  color: white;
  width: 100%;
  padding: 20px 0;
  text-align: center;
  font-family: 'Open Sans', sans-serif;
`;

const ContentArea = styled.div`
  width: 85%;
  padding: 20px;
  margin-top: 20px;
  background-color: white;
  border-radius: 8px;
`;

const Section = styled.section`
  margin: 20px 0;
  font-family: "Open Sans", sans-serif;
`;

const Footer = styled.footer`
  background-color: #0eb4bd;
  color: white;
  width: 100%;
  padding: 10px;
  position: relative;
  bottom: 0;
  text-align: center;
`;

const NavLink = styled(Link)`
  color: white;
  text-decoration: none;
  padding: 0 15px;

  &:hover {
    text-decoration: underline;
  }
`;

const GlobalStyle = createGlobalStyle`
  * {
    box-sizing: border-box;
  }

  html, body {
    width: 100%;
  }
`;

function LandingPage() {
  return (
    <>
        <GlobalStyle />
        <PageContainer>
            <Header>
                <h1>University of Aveiro's Educational Offer Competence Tagging</h1>
                <NavLink to="/">Home</NavLink>
                <NavLink to="/chat">Chat Interface</NavLink>
                <NavLink to="/edit-course">Edit Course</NavLink>
            </Header>
            <ContentArea>
                <Section>
                    <h2>Introduction</h2>
                    <p>This web portal was developed following the dissertation <b>Development of a computational system for determining ESCO competences associated with training offers</b>, to fulfill the requirements of Master's degree in Informatics Engineering.</p>
                </Section>
                <Section>
                    <h2>What is ESCO?</h2>
                    <p>The acronym <b>ESCO</b> stands for <b>European Skills, Competences, Qualifications and Occupations</b> and functions as a dictionary that describes, identifies and classifies professional occupations and skills relevant to the EU labor market and the education and training sectors.</p>
                    <p>ESCO was developed by the European Union and its major objective is to support job mobility across Europe by offering a "common language" to describe occupations and skills that can be used by different stakeholders on employment, education and lifelong learning. <a href="https://esco.ec.europa.eu/en/about-esco/what-esco" target="_blank" rel="noopener noreferrer" style={{textDecoration: 'none', color: 'black'}}><b>Learn more</b></a></p>
                    <p>The team responsible for ESCO also developed an <a href="https://esco.ec.europa.eu/en/use-esco/use-esco-services-api" target="_blank" rel="noopener noreferrer" style={{textDecoration: 'none', color: 'black'}}><b>Application Programming Interface (API)</b></a> that facilitates the integration in computational systems.
                    However, this API is not capable, by itself, of accurately returning a list of ESCO skills for texts related to training or educational offers, often suggesting unrelated skills.
                    </p>
                </Section>
                <Section>
                    <h2>Objective</h2>
                    <p>The main objective of this dissertation is to obtain an accurate list of ESCO competences that represent the learning outcomes of each course lectured in University of Aveiro (UA).
                    <br></br>
                    This will help current and future students to have a better understanding of the University’s educational offer and companies’ Human Resources representatives to acknowledge and recognize UA’s former students skills upon hiring them.</p>
                </Section>
                <Section>
                    <h2>Approach</h2>
                    <p>In order to accurately map the University of Aveiro's educational offer to ESCO skills, an interactive system featuring a <i>chatbot</i> was developed. Here is how it works:</p>
                    <p><b>Input and data fetching - </b>In the chat interface, professors input the name and code of a course. Then, the system will fetch the data related to that course, which was previously gathered from the Pedagogical Dossiers (DPUCs).</p>
                    <b>ESCO API Query -</b> The system queries the ESCO API using the course's name and description to retrieve a list of relevant skills.                    
                    <p><b>Skill Filtering -</b> This list and the course data are then processed by the <a href="https://www.cloudflare.com/learning/ai/what-is-large-language-model/" target="_blank" rel="noopener noreferrer" style={{textDecoration: 'none', color: 'black'}}><b>Large Language Model (LLM)</b></a> <i>GPT-4</i>, which will filter out the skills that are not applicable, trusting in <a href="https://www.promptingguide.ai/techniques/zeroshot" target="_blank" rel="noopener noreferrer" style={{textDecoration: 'none', color: 'black'}}><b>Zero-Shot Prompting</b></a> technique for that effect.</p>
                    <p><b>Manual Validation -</b> The refined list of skills is presented to the professor, who should manually select the skills that accurately reflect the course contents and align with their learning outcomes. It is also possible for the professors to insert new skills via text.</p>
                    <p><b>Course Editing -</b> Professors also have the option to consult and edit the course contents and objectives through the "Edit Course" page.</p>
                </Section>
                <Section>
                    <h2>Results</h2>
                    <p>The tool has successfully tagged over 500 courses with relevant skills, enhancing educational planning and student guidance.</p>
                </Section>
                <Section>
                    <h2>Contact</h2>
                    <p>For more information or to contribute to the project, please contact us via email at example@ua.pt.</p>
                </Section>
            </ContentArea>
            <Footer>
                © 2024 University of Aveiro - All rights reserved.
            </Footer>
        </PageContainer>
    </>
    );
}

export default LandingPage;