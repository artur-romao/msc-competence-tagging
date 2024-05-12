import { useState, } from 'react';
import { toast } from "react-toastify";

export const useEditCourseLogic = () => {

    // STATES

    const [courseName, setCourseName] = useState('');
    const [lastCourseId, setLastCourseId] = useState('');
    const [objectives, setObjectives] = useState('');
    const [url, setUrl] = useState('');
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

    const fetchCourseInfo = async (courseId) => {
      try {
        const response = await fetch(`${apiUrl}/query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          body: JSON.stringify({ course_id: courseId, get_skills: false }),
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

    const updateCourseInfo = async (courseId, contents, objectives) => {
      try {
        const response = await fetch(`${apiUrl}/update-course`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          body: JSON.stringify({ course_id: courseId, contents: contents, objectives: objectives }),
        });
    
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
    
        return response;
      } catch (error) {
        console.error("Failed to fetch skills:", error);
        return null;
      }
    };

    // UTILS FUNCTIONS

    const getCourseId = (input) => { // This function keeps leading numbers (which is the course id, for example "12345 SOFTWARE ENGINEERING" -> "12345") 
      const match = input.match(/^\d+/);
      return match ? match[0] : '';
    };

    const handleDropdownSelect = (courseName) => {
      setCourseName(courseName);
      let courseId = getCourseId(courseName);
      setLastCourseId(courseId);
      setShowDropdown(false);
      fillCourseInfo(courseId);
    };
    
    const fillCourseInfo = async(courseId) => {
      const data = await fetchCourseInfo(courseId);
      setUrl(data.url);
      setContents(data.contents);
      setObjectives(data.objectives);
    }

    const handleSave = async() => {
      try {
        const response = await updateCourseInfo(lastCourseId, contents, objectives);    
        if (response.ok) {
          toast.success('Course information updated successfully!', { position: "top-center", hideProgressBar: true });
        } else {
          toast.error('Failed to update the course information.', { position: "top-center", hideProgressBar: true });
        }
      } catch (error) {
        console.error("Failed to update course:", error);
        toast.error('An error occurred while updating the course.', { position: "top-center", hideProgressBar: true });
      }
    };

    return {
        courseName,
        setCourseName,
        lastCourseId,
        setLastCourseId,
        url,
        setUrl,
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