import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

/**
 * Main webpage component for the video processing application at the edge
 * @returns {JSX.Element} The rendered component
 */
function App() {
  /**
   * State variables to manage file selection, processed video, loading state, and backend availability
   */
  const [selectedFile, setSelectedFile] = useState(null);
  const [processedVideo, setProcessedVideo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [backendAvailable, setBackendAvailable] = useState(true);
  const fileInputRef = useRef(null);

  /**
   * Check the availability of the backend service via the edge API
   */
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await axios.get('http://localhost:4000/check-signal');
        setBackendAvailable(response.status === 200 && response.data === "Connection Successful");
      } catch (error) {
        console.error('Backend check failed:', error);
        setBackendAvailable(false);
      }
    };

    // Check backend availability every 60 seconds
    const intervalId = setInterval(checkBackend, 60000);
    checkBackend(); // Initial check

    return () => clearInterval(intervalId); // Cleanup on component unmount
  }, []);

  /**
   * Handle file input change
   * @param {Event} event - The file input change event
   */
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

  /**
   * Async Method handles file upload to the backend service.
   */
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

  /**
   * Clear the selected file and processed video.
   */
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
        {!backendAvailable && (
          <div className="error-message">
            Backend service is unavailable. Please try again later.
          </div>
        )}
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
          disabled={!backendAvailable}
        />
        <button onClick={handleUpload} disabled={!selectedFile || loading || !backendAvailable}>
          {loading ? 'Uploading...' : 'Upload Video'}
        </button>
      </header>
    </div>
  );
}

export default App;