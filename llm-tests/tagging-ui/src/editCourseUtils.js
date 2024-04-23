import React, { useState, } from 'react';

export const useEditCourseLogic = () => {

    // STATES
    const [courseName, setCourseName] = useState('');
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

    const handleDropdownSelect = (courseName) => {
        setCourseName(courseName);
        setShowDropdown(false);
    };
    
    return {
        courseName,
        setCourseName,
        contents,
        setContents,
        objectives,
        setObjectives,
        courses,
        setCourses,
        showDropdown,
        setShowDropdown,
        fetchCourses,
        handleDropdownSelect,
      };
}