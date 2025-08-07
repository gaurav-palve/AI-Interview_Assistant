import React, { useState } from 'react';
import axios from 'axios';

export default function UploadForm() {
  const [jd, setJd] = useState(null);
  const [resume, setResume] = useState(null);
  const [mcqs, setMcqs] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("jd", jd);
    formData.append("resume", resume);

    const response = await axios.post("http://localhost:8000/upload/", formData);
    setMcqs(response.data.mcqs);
  };

  return (
    <div>
      <h2>Upload JD and Resume</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={(e) => setJd(e.target.files[0])} required />
        <input type="file" onChange={(e) => setResume(e.target.files[0])} required />
        <button type="submit">Generate MCQs</button>
      </form>
      <div>
        <h3>Generated MCQs:</h3>
        <pre>{mcqs}</pre>
      </div>
    </div>
  );
}
