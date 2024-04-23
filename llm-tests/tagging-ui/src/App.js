import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Chat from './Chat';
import EditCoursePage from './EditCoursePage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/edit-course" element={<EditCoursePage />} />
      </Routes>
    </Router>
  );
}

export default App;
