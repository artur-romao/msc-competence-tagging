import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';

const AppContainer = styled.div`
  display: flex;  
  text-align: center;
  height: 100vh;
  position: relative;
  flex-direction: column;
`;

const AppHeader = styled.header`
  background-color: #0eb4bd;
  padding: 20px;
  color: white;
  font-family: sans-serif;
`;

const ChatWindow = styled.div`
  margin: 1rem;
  border: 1px solid #ccc;
  padding: 10px;
  overflow-y: auto;
  margin-bottom: 1rem;
  height: 67%;
  display: flex;
  flex-direction: column;
`;

const DropdownContainer = styled.div`
  overflow-y: auto;
  text-align: left;
  max-height: 20rem;
  position: absolute;
  bottom: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  z-index: 10;
`;

const DropdownItem = styled.div`
  padding: 10px;
  cursor: pointer;
  &:hover {
    background-color: #f0f0f0;
  }
`;

const InputArea = styled.div`
  position: absolute;
  bottom: 0;
  left: 0; 
  right: 0;
  display: flex;
  margin: 20px;
  margin-top: 20px; 
  background: white;
`;

const Input = styled.input`
  flex: 1;
  margin-right: 10px;
  padding: 10px;
`;

const Button = styled.button`
  padding: 10px;
`;

const Message = styled.div`
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 20px;
  color: white;
  max-width: 60%;
  align-self: ${(props) => (props.from === 'user' ? 'flex-end' : 'flex-start')};
  background-color: ${(props) => (props.from === 'user' ? '#007bff' : '#666')};
  display: flex;
  justify-content: ${(props) => (props.from === 'user' ? 'flex-end' : 'flex-start')};
  overflow-wrap: break-word;
`;

const MessageText = ({ text }) => {
  // Split the text into lines based on "\n"
  const lines = text.split('\n');
  
  // Render the lines, adding <br /> elements between them
  return (
    <>
      {lines.map((line, index) => (
        <React.Fragment key={index}>
          {line}
          {index < lines.length - 1 && <br />}
        </React.Fragment>
      ))}
    </>
  );
};

function App() {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [courses, setCourses] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);

  const chatWindowRef = useRef(null);

  const apiUrl = process.env.REACT_APP_API_URL || 'http://web:8000'; // Fallback URL

  useEffect(() => {
    // Scroll to the bottom of the ChatWindow whenever messages change
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]); // Depend on messages

  const handleDropdownSelect = (courseName) => {
    setQuery(courseName);
    setShowDropdown(false);
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
  

  const handleSend = async () => {
    const courseName = query
    setQuery('');
    if (!courseName.trim()) return;

    setMessages([...messages, { from: 'user', text: courseName }]);
    
    const skillsResponse = await fetchSkills(courseName);
    if (skillsResponse) {
      // Assuming the API returns a list of skills directly
      // const skillsText = `Skills: ${skillsResponse.join(', ')}`;
      setMessages(currentMessages => [...currentMessages, { from: 'system', text: skillsResponse.text }]);
    }
    else {
      setMessages(messages => [...messages, { from: 'system', text: "No skills are available for the provided course." }]);
    }
    setShowDropdown(false);
  };

  return (
    <AppContainer>
      <AppHeader>
        <h1>University of Aveiro's Educational Offer Competence Tagging</h1>
      </AppHeader>
      <ChatWindow ref={chatWindowRef}>
        {messages.map((msg, index) => (
          <Message key={index} from={msg.from}>
            <MessageText text={msg.text} />
          </Message>
        ))}
      </ChatWindow>
      <InputArea>
      {showDropdown && (
        <DropdownContainer>
          {courses.map((course, index) => (
            <DropdownItem key={index} onClick={() => handleDropdownSelect(course)}>
              {course}
            </DropdownItem>
          ))}
        </DropdownContainer>
      )}
      <Input
        value={query}
        onChange={e => {
          setQuery(e.target.value);
          fetchCourses(e.target.value);
        }}
        type="text"
        placeholder="Enter course name..."
      />
        <Button onClick={handleSend}>Send</Button>
      </InputArea>
    </AppContainer>
  );
}

export default App;
