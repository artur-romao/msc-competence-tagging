import React, { useEffect, useRef } from 'react';
import styled from 'styled-components';
import "./App.css"
import { useChatLogic } from './utils.js';

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
  font-family: "Open Sans", sans-serif;
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
  font-family: "Open Sans", sans-serif;
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

const SkillItem = styled.div`
  display: flex;
  align-items: center;
  padding: 5px;
`;

const Checkbox = styled.input.attrs({ type: 'checkbox' })`
  margin-right: 10px;
`;

const SystemMessageContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: flex-start; // Aligns to the left
  padding-left: 10px; // Give some space from the left edge
`;

function App() {
  const chatWindowRef = useRef(null);
  const {
    messages,
    query,
    setQuery,
    courses,
    showDropdown,
    isLoading,
    selectedSkills,
    latestMessageIndex,
    fetchCourses,
    handleSend,
    handleDropdownSelect,
    handleSaveSkills,
    handleSkillChange,
    LoadingAnimation
  } = useChatLogic();

  useEffect(() => {
    // Scroll to the bottom of the ChatWindow whenever messages change
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  const Message = ({ from, text, skills, onSkillChange, onSave, isLatest}) => {
    const skillsPart = from === 'system' && skills && (
      <>
        {Object.entries(skills).map(([skillName, isSelected]) => (
          <SkillItem key={skillName}>
            {isLatest && <Checkbox
              checked={selectedSkills[skillName]}
              onChange={(e) => onSkillChange(skillName, e.target.checked)}
              disabled={!isLatest}
            />}
            {!isLatest && <Checkbox
              checked={isSelected}
              onChange={(e) => onSkillChange(skillName, e.target.checked)}
              disabled={true}
            />}
            {skillName}
          </SkillItem>
        ))}
        {isLatest && <Button onClick={onSave} style={{padding:'5px 10px', width:'50%', margin:'0 25%'}}>Save</Button>}
      </>
    );
    return (
      <div style={{
        marginBottom: '10px',
        padding: '10px',
        borderRadius: '20px',
        color: 'white',
        maxWidth: '60%',
        alignSelf: from === 'user' ? 'flex-end' : 'flex-start',
        backgroundColor: from === 'user' ? '#0eb4bd' : '#d3d3d3',
        color: from === 'user' ? '#ffffff' : '#000000',
        display: 'flex',
        justifyContent: from === 'user' ? 'flex-end' : 'flex-start',
        overflowWrap: 'break-word',
        fontFamily: 'Open Sans, sans-serif',
        flexDirection: 'column',
      }}>
        <div>{text}</div>
        {skillsPart}
      </div>
    );
  };

  return (
    <AppContainer>
      <AppHeader>
        <h1>University of Aveiro's Educational Offer Competence Tagging</h1>
      </AppHeader>
      <ChatWindow ref={chatWindowRef}>
        {messages.map((msg, index) => (
          <Message
            key={index}
            from={msg.from}
            text={msg.text}
            skills={msg.skills}
            onSkillChange={handleSkillChange}
            onSave={handleSaveSkills}
            isLatest={index - 1 === latestMessageIndex}
          />
        ))}
        {isLoading && (
          <SystemMessageContainer>
            <LoadingAnimation />
          </SystemMessageContainer>)}
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
