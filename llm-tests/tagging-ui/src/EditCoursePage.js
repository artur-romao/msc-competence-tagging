import React from 'react';
import styled from 'styled-components';
import "./App.css"
import { useEditCourseLogic } from './editCourseUtils.js'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Link } from 'react-router-dom'; 

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

const DropdownContainer = styled.div`
  position: absolute;
  top: 100%; // Position the dropdown right below the input field
  left: 50%;
  transform: translateX(-50%); // This will center the dropdown
  overflow-y: auto;
  text-align: left;
  max-height: 20rem;
  width: 50%;
  background: white;
  border: 1px solid #ccc;
  z-index: 10;
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2); // Optional: adds a shadow for better separation from content below
`;

const DropdownItem = styled.div`
  padding: 10px;
  cursor: pointer;
  &:hover {
    background-color: #f0f0f0;
  }
  font-family: "Open Sans", sans-serif;
`;

const SearchArea = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  position: relative; // This will be the anchor for the absolute positioning of the dropdown
`;

const InputContainer = styled.div`
  display: flex;  
  text-align: center;
  flex-direction: column;
  align-items: center;
`;

const FieldHeader = styled.div`
  margin: 2rem 45rem 1rem 0rem;
  color: black;
  font-family: "Open Sans", sans-serif;
  font-weight: bold;
`;

const Input = styled.input`
  width: 50%;
  margin: 2rem 2rem 0rem 2rem;
  height: 1.5rem;
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  padding-left: 0.5rem;
`;

const LargeInput = styled.textarea`
  width: 50%;
  height: 8rem;
  margin: 0 2rem 2rem 2rem;
  resize: none;
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  padding-left: 0.5rem;
`;

const SaveButtonContainer = styled.div`
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
  margin-right: 18rem;
`;

const SaveButton = styled.button`
  padding: 1rem;
  background-color: #0eb4bd;
  color: white;
  border: none;
  cursor: pointer;
  width: 8%;
  font-family: "Open Sans", sans-serif;
  font-weight: bold;
`;

const NavLink = styled(Link)`
  color: white;
  text-decoration: none;
  padding: 0 15px;

  &:hover {
    text-decoration: underline;
  }
`;

function EditCoursePage() {

  const {
    courseName,
        setCourseName,
        contents,
        setContents,
        objectives,
        setObjectives,
        courses,
        showDropdown,
        fetchCourses,
        handleDropdownSelect,
        handleSave,
  } = useEditCourseLogic();

  return (
    <AppContainer>
        <ToastContainer style={{width: "40rem"}}/>
        <AppHeader>
          <h1>Edit Course Information (DPUC)</h1>
          <NavLink to="/">Home</NavLink>
          <NavLink to="/chat">Chat Interface</NavLink>
          <NavLink to="/edit-course">Edit Course</NavLink>
        </AppHeader>
        <InputContainer>
            <SearchArea>
                <Input
                    type="text"
                    placeholder="Search course by name or id..."
                    value={courseName}
                    onChange={(e) => {
                        setCourseName(e.target.value);
                        fetchCourses(e.target.value);
                    }}
                    // You might want to integrate your dropdown selection logic here
                />
                {showDropdown && (
                    <DropdownContainer>
                    {courses.map((course, index) => (
                        <DropdownItem key={index} onClick={() => handleDropdownSelect(course)}>
                            {course}
                        </DropdownItem>
                    ))}
                    </DropdownContainer>
                )}
            </SearchArea>
            <FieldHeader>Contents</FieldHeader>
            <LargeInput
                value={contents}
                onChange={(e) => setContents(e.target.value)}
                placeholder="Course contents..."
            />
            <FieldHeader>Objectives</FieldHeader>
            <LargeInput
                value={objectives}
                onChange={(e) => setObjectives(e.target.value)}
                placeholder="Course objectives..."
            />
        </InputContainer>
        <SaveButtonContainer>
            <SaveButton onClick={handleSave}>Save</SaveButton>
        </SaveButtonContainer>
    </AppContainer>
  );
}

export default EditCoursePage;
