import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [processedVideo, setProcessedVideo] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('video/')) {
      setSelectedFile(file);
    } else {
      alert('Please select a valid video file.');
      if (fileInputRef.current) {
        fileInputRef.current.value = null;
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:4000/process-video', formData, {
        responseType: 'blob',
      });
    
      if (response.status === 200) {
        console.log(response.data); // Log the response data
        const videoUrl = URL.createObjectURL(response.data);
        setProcessedVideo(videoUrl);
      } else {
        console.error('Upload failed');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setProcessedVideo(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = null;
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Video Processor</h1>
        {processedVideo && (
          <div className="video-container">
            <video controls src={processedVideo} />
            <div className="video-actions">
              <a href={processedVideo} download="processed_video.mp4">
                Download Processed Video
              </a>
              <button onClick={handleClear}>Clear</button>
            </div>
          </div>
        )}
        <input
          type="file"
          accept="video/*"
          onChange={handleFileChange}
          ref={fileInputRef}
        />
        <button onClick={handleUpload} disabled={!selectedFile || loading}>
          {loading ? 'Uploading...' : 'Upload Video'}
        </button>
      </header>
    </div>
  );
}

export default App;