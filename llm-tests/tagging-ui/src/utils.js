import React, { useState, } from 'react';
import styled, { keyframes } from 'styled-components';

// STATES

export const useChatLogic = () => {

  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [courses, setCourses] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedSkills, setSelectedSkills] = useState({});
  const [latestMessageIndex, setLatestMessageIndex] = useState();

  // API CALLS

  const apiUrl = process.env.REACT_APP_API_URL || 'http://web:8000'; // Fallback URL

  const fetchSkills = async (courseName) => {
      try {
        const response = await fetch(`${apiUrl}/query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          body: JSON.stringify({ course_name: courseName }),
        });
    
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
    
        const data = await response.json();
        return data;
      } catch (error) {
        console.error("Failed to fetch skills:", error);
        return null;
      }
  };

  const fetchCourses = async (substring) => {
      try {
        if (substring.length >= 4) {
          const response = await fetch(`${apiUrl}/search-courses?query=${encodeURIComponent(substring)}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });
    
          if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
          }
    
          const data = await response.json();
          setCourses(data);
          setShowDropdown(true);
        } else {
          setShowDropdown(false);
        }
      } catch (error) {
        console.error("Failed to fetch courses:", error);
        setShowDropdown(false);
      }
  };

  // UTILS FUNCTIONS

  const handleSend = async () => {
    setLatestMessageIndex(messages.length);
    setSelectedSkills({});
    setIsLoading(true);
    const courseName = query
    setQuery('');
    if (!courseName.trim()) return;

    setMessages([...messages, { from: 'user', text: courseName }]);
    const skillsResponse = await fetchSkills(courseName);
    setIsLoading(false);

    if (skillsResponse) {
      const skillsList = skillsResponse.text.split("\n");
      let skillsDict = skillsList.reduce((acc, skill) => ({
        ...acc,
        [skill]: true,
      }), {});
      setSelectedSkills(JSON.parse(JSON.stringify(skillsDict)));
      setMessages(currentMessages => [...currentMessages, {
        from: 'system',
        text: 'Please select the relevant skills:\n', // Added \n for new line
        skills: skillsDict,
      }]);
    }
    else {
      setMessages(messages => [...messages, { from: 'system', text: "No skills are available for the provided course." }]);
    }
    setShowDropdown(false);
  };

  const handleDropdownSelect = (courseName) => {
    setQuery(courseName);
    setShowDropdown(false);
  };

  const handleSaveSkills = () => {
    console.log('Selected Skills:', selectedSkills);
    // Save the selected skills as needed, then clear selections
    // setSelectedSkills({});
    // Optionally send the selected skills to an API or backend service
  };

  const updateMessageSkills = (messageIndex, newSkills) => {
    setMessages(currentMessages => 
      currentMessages.map((msg, index) => 
        index === messageIndex ? { ...msg, skills: newSkills } : msg
      )
    );
  };  

  const handleSkillChange = (skillName, isSelected) => {
    setSelectedSkills(prevSkills => {
      const updatedSkills = { ...prevSkills, [skillName]: isSelected };
      console.log(updatedSkills);
      let messageIndex = latestMessageIndex + 1;
      updateMessageSkills(messageIndex, updatedSkills);
      return updatedSkills;
    });
  };

  const wave = keyframes`
    0%, 60%, 100% {
      transform: initial;
    }
    30% {
      transform: translateY(-15px);
    }
  `;

  const Dot = styled.div`
    background-color: ${props => props.color};
    border-radius: 50%;
    width: 10px;
    height: 10px;
    margin: 0 5px;
    /* Animation */
    animation: ${wave} 1.3s linear infinite;
    
    &:nth-child(2) {
      animation-delay: -1.1s;
    }
    
    &:nth-child(3) {
      animation-delay: -0.9s;
    }
  `;

  const LoadingDots = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
  `;

  const LoadingAnimation = () => (
    <LoadingDots>
      <Dot color="#e74c3c" />
      <Dot color="#3498db" />
      <Dot color="#f1c40f" />
    </LoadingDots>
  );
  
  return {
    messages,
    setMessages,
    query,
    setQuery,
    courses,
    setCourses,
    showDropdown,
    setShowDropdown,
    isLoading,
    setIsLoading,
    selectedSkills,
    setSelectedSkills,
    latestMessageIndex,
    setLatestMessageIndex,
    fetchSkills,
    fetchCourses,
    handleSend,
    handleDropdownSelect,
    handleSaveSkills,
    updateMessageSkills,
    handleSkillChange,
    LoadingAnimation,
  };
};
