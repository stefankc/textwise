import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import MarkdownRenderer from '../../components/MarkdownRenderer/MarkdownRenderer';
import './MarkdownPage.css';

function MarkdownPage() {
  // Get filename from URL parameters
  const { filename } = useParams();
  // State for storing file data including content and paragraphs
  const [fileData, setFileData] = useState(null); // { content, paragraphs: [{ id, order, content }] }
  // State for storing notes indexed by paragraph ID
  const [notes, setNotes] = useState({}); // { paragraphId: Note }
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const noteCount = Object.keys(notes).length;

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  useEffect(() => {
    // Fetch file data including paragraphs from the database
    fetch(`${backendUrl}/files/${filename}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Error retrieving file.');
        }
        return response.json();
      })
      .then(data => {
        setFileData(data);
        console.log('File Data:', data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error retrieving file:', error);
        setError('Error loading file.');
        setLoading(false);
      });

    // Fetch existing notes using the notes endpoint
    fetch(`${backendUrl}/notes/file_by_name/${filename}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Error retrieving notes.');
        }
        return response.json();
      })
      .then(data => {
        console.log('Notes Data:', data);
        // Group notes by paragraph ID
        const groupedNotes = data.reduce((acc, note) => {
          acc[note.paragraph_id] = note;
          return acc;
        }, {});
        console.log('Grouped Notes:', groupedNotes);
        setNotes(groupedNotes);
      })
      .catch(error => {
        console.error('Error retrieving notes:', error);
        setError('Error loading notes.');
      });
  }, [filename, backendUrl]);

  // Function to get markdown content up to a specific paragraph
  const getMarkdownUpTo = (paragraphId) => {
    if (!fileData || !fileData.paragraphs) return "";
    const targetParagraph = fileData.paragraphs.find(p => p.id === paragraphId);
    if (!targetParagraph) return "";
    const targetOrder = targetParagraph.order;
    const selectedParagraphs = fileData.paragraphs
      .filter(p => p.order <= targetOrder)
      .sort((a, b) => a.order - b.order);
    const markdownUpTo = selectedParagraphs.map(p => p.content).join("\n\n");
    return markdownUpTo;
  };

  // Handler for adding a new note
  const handleAddNote = (paragraphId, content) => {
    if (!paragraphId) {
      alert('Paragraph ID is undefined. Please ensure each paragraph has a unique ID.');
      return;
    }
    if (content.trim() === '') return;

    const markdownUpTo = getMarkdownUpTo(paragraphId);
    console.log(`Markdown up to paragraph ${paragraphId}:`, markdownUpTo);

    fetch(`${backendUrl}/notes/${filename}/${paragraphId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content }),
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => { throw new Error(err.detail || 'Error saving note'); });
        }
        return response.json();
      })
      .then(data => {
        console.log('New note added:', data);
        setNotes(prevNotes => ({
          ...prevNotes,
          [data.paragraph_id]: data,
        }));
      })
      .catch(error => {
        console.error('Error adding note:', error);
        alert(`Error saving note: ${error.message}`);
      });
  };

  // Handler for updating an existing note
  const handleUpdateNote = (noteId, updatedContent) => {
    fetch(`${backendUrl}/notes/${noteId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: updatedContent }),
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => { throw new Error(err.detail || 'Error updating note'); });
        }
        return response.json();
      })
      .then(updatedNote => {
        console.log('Note updated:', updatedNote);
        setNotes(prevNotes => ({
          ...prevNotes,
          [updatedNote.paragraph_id]: updatedNote,
        }));
      })
      .catch(error => {
        console.error('Error updating note:', error);
        alert(`Error updating note: ${error.message}`);
      });
  };

  // Handler for deleting a note
  const handleDeleteNote = (noteId, paragraphId) => {
    fetch(`${backendUrl}/notes/${noteId}`, {
      method: 'DELETE',
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => { throw new Error(err.detail || 'Error deleting note'); });
        }
        return response.json();
      })
      .then(() => {
        console.log('Note deleted:', noteId);
        setNotes(prevNotes => {
          const updatedNotes = { ...prevNotes };
          delete updatedNotes[paragraphId];
          return updatedNotes;
        });
      })
      .catch(error => {
        console.error('Error deleting note:', error);
        alert(`Error deleting note: ${error.message}`);
      });
  };

  // Render loading state
  if (loading) {
    return (
      <div className="markdown-page">
        <h1>{filename}</h1>
        <p>Loading...</p>
      </div>
    );
  }

  // Render error state
  if (error) {
    return (
      <div className="markdown-page">
        <h1>{filename}</h1>
        <p>{error}</p>
      </div>
    );
  }

  // Render main content
  return (
    <div className="markdown-page">
      <h1>{filename}</h1>
      <MarkdownRenderer 
        paragraphs={fileData.paragraphs} 
        notes={notes} 
        noteCount={noteCount}
        onAddNote={handleAddNote}
        onUpdateNote={handleUpdateNote}
        onDeleteNote={handleDeleteNote}
        getMarkdownUpTo={getMarkdownUpTo}
      />
    </div>
  );
}

export default MarkdownPage;