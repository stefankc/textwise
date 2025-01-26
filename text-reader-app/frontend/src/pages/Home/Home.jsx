import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Home.css';
import Modal from 'react-modal';
import { useDropzone } from 'react-dropzone';

// Set the root element for accessibility
Modal.setAppElement('#root');

function Home() {
  // State variables for managing files, loading state, errors, and modals
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingFile, setEditingFile] = useState(null);
  const [newFilename, setNewFilename] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  // Backend URL from environment variables or default
  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  // Fetch files from the backend when the component mounts
  useEffect(() => {
    fetch(`${backendUrl}/files`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Sort files by the updated_at date in descending order
        const sortedFiles = data.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
        setFiles(sortedFiles);
        setLoading(false);
        console.log('Fetched files:', sortedFiles);
      })
      .catch(error => {
        console.error('Error fetching files:', error);
        setError('Error loading files.');
        setLoading(false);
      });
  }, [backendUrl]);

  // Open the modal for editing a file
  const openModal = (file) => {
    console.log(`Opening modal for file: ${file.filename}`);
    setEditingFile(file);
    setNewFilename(file.filename);
    setIsModalOpen(true);
  };

  // Close the modal and reset editing states
  const closeModal = () => {
    console.log('Closing modal');
    setEditingFile(null);
    setNewFilename('');
    setIsModalOpen(false);
  };

  // Handle renaming a file
  const handleRename = () => {
    if (newFilename.trim() === '') {
      alert('The file name must not be empty.');
      return;
    }

    console.log(`Renaming file from ${editingFile.filename} to ${newFilename}`);

    fetch(`${backendUrl}/files/${encodeURIComponent(editingFile.filename)}/rename`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ new_filename: newFilename }),
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => { throw new Error(err.detail || 'Error renaming the file.'); });
        }
        return response.json();
      })
      .then(updatedFile => {
        console.log('Updated file:', updatedFile);
        // Check if created_at and updated_at are present
        if (!updatedFile.created_at || !updatedFile.updated_at) {
          console.warn('Updated file has missing timestamps:', updatedFile);
        }
        // Update the file list with the renamed file
        setFiles(prevFiles => prevFiles.map(file =>
          file.id === updatedFile.id ? updatedFile : file
        ));
        closeModal();
      })
      .catch(error => {
        console.error('Error renaming:', error);
        const errorMessage = error.message || JSON.stringify(error);
        alert(`Error renaming the file: ${errorMessage}`);
      });
  };

  // Handle deleting a file
  const handleDelete = () => {
    if (!editingFile) return;

    const confirmDelete = window.confirm(`Do you really want to delete the file "${editingFile.filename}"?`);
    if (!confirmDelete) return;

    console.log(`Deleting file: ${editingFile.filename}`);

    fetch(`${backendUrl}/files/${encodeURIComponent(editingFile.filename)}`, {
      method: 'DELETE',
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => { throw new Error(err.detail || 'Error deleting the file.'); });
        }
        return response.json();
      })
      .then(() => {
        console.log(`File ${editingFile.filename} deleted successfully.`);
        // Update the file list after deletion
        setFiles(prevFiles => prevFiles.filter(file => file.id !== editingFile.id));
        closeModal();
      })
      .catch(error => {
        console.error('Error while deleting:', error);
        const errorMessage = error.message || JSON.stringify(error);
        alert(`Error deleting the file: ${errorMessage}`);
      });
  };

  // Handle file uploads using Dropzone
  const onDrop = (acceptedFiles) => {
    setUploading(true);
    setUploadError(null);
    console.log('Files dropped:', acceptedFiles);

    const formData = new FormData();
    acceptedFiles.forEach(file => {
      formData.append('files', file);
    });

    fetch(`${backendUrl}/files/upload`, {
      method: 'POST',
      body: formData,
    })
      .then(async response => {
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText || 'Error uploading the files.');
        }
        return response.json();
      })
      .then(data => {
        console.log('Uploaded files:', data);
        // Add the uploaded files to the existing file list
        setFiles(prevFiles => [...prevFiles, ...data]); 
        setUploading(false);
      })
      .catch(error => {
        console.error('Error while uploading:', error);
        setUploadError(error.message);
        setUploading(false);
      });
  };

  // Initialize Dropzone with the onDrop handler
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  // Render loading state
  if (loading) {
    return (
      <div className="home-page">
        <h1>Reader-Files</h1>
        <p>Loading...</p>
      </div>
    );
  }

  // Render error state
  if (error) {
    return (
      <div className="home-page">
        <h1>Reader-Files</h1>
        <p>{error}</p>
      </div>
    );
  }

  // Render the main content
  return (
    <div className="home-page">
      <h1>Reader-Files</h1>

      {/* Dropzone Area for file uploads */}
      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
        <input {...getInputProps()} />
        {
          isDragActive ?
            <p>Drag files here...</p> :
            <p>Drag files here or click to select files</p>
        }
      </div>
      {uploading && <p>Uploading...</p>}
      {uploadError && <p className="error">{uploadError}</p>}

      {/* List of files */}
      <ul className="files-list">
        {files.map(file => (
          <li key={file.id} className="file-item">
            <Link to={`/files/markdown/${encodeURIComponent(file.filename)}`} className="file-link">
              {file.filename}
            </Link>
            <button className="edit-button" onClick={() => openModal(file)}>
              Edit
            </button>
          </li>
        ))}
      </ul>

      {/* Modal for editing a file */}
      {editingFile && (
        <Modal
          isOpen={isModalOpen}
          onRequestClose={closeModal}
          contentLabel="Edit File"
          className="modal"
          overlayClassName="overlay"
        >
          <h2>Edit the file</h2>
          <div className="modal-content">
            <div className="rename-section">
              <label htmlFor="rename-input">New Filename:</label>
              <input
                type="text"
                id="rename-input"
                value={newFilename}
                onChange={(e) => setNewFilename(e.target.value)}
              />
            </div>
            <div className="delete-section">
              <button className="save-button" onClick={handleRename}>Save</button>
              <button className="delete-button" onClick={handleDelete}>
                Delete File
              </button>
            </div>
          </div>
          <button className="close-button" onClick={closeModal}>X</button>
        </Modal>
      )}
    </div>
  );
}

export default Home;