import React, { useState, } from 'react';

export const useEditCourseLogic = () => {

    // STATES
    const [courseName, setCourseName] = useState('');
    const [lastCourseName, setLastCourseName] = useState('');
    const [objectives, setObjectives] = useState('');
    const [contents, setContents] = useState('');
    const [courses, setCourses] = useState([]);
    const [showDropdown, setShowDropdown] = useState(false);

    // API CALLS

    const apiUrl = process.env.REACT_APP_API_URL || 'http://web:8000'; // Fallback URL

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

    const fetchCourseInfo = async (courseName) => {
      try {
        const response = await fetch(`${apiUrl}/query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          body: JSON.stringify({ course_name: courseName, get_skills: false }),
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

    const updateCourseInfo = async (courseName, contents, objectives) => {
      try {
        const response = await fetch(`${apiUrl}/update-course`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          body: JSON.stringify({ course_name: courseName, contents: contents, objectives: objectives }),
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

    // UTILS FUNCTIONS

    const handleDropdownSelect = (courseName) => {
      setCourseName(courseName);
      setLastCourseName(courseName);
      setShowDropdown(false);
      fillCourseInfo(courseName);
    };
    
    const fillCourseInfo = async(courseName) => {
      const data = await fetchCourseInfo(courseName);
      setContents(data.contents);
      setObjectives(data.objectives);
    }

    const handleSave = async() => {
      const response = await updateCourseInfo(lastCourseName, contents, objectives);
      console.log(response);
    };

    return {
        courseName,
        setCourseName,
        lastCourseName,
        setLastCourseName,
        contents,
        setContents,
        objectives,
        setObjectives,
        courses,
        setCourses,
        showDropdown,
        setShowDropdown,
        fetchCourses,
        fetchCourseInfo,
        handleDropdownSelect,
        fillCourseInfo,
        handleSave
      };
}