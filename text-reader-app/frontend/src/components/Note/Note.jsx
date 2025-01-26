import React, { useState, useRef, useEffect } from 'react';
import './Note.css';
import Modal from 'react-modal';
import ReactMarkdown from 'react-markdown';
import rehypeSanitize from 'rehype-sanitize';
import remarkGfm from 'remark-gfm';

// Set the root element for accessibility
Modal.setAppElement('#root'); 

function Note({ note, onUpdate, onDelete, getMarkdownUpTo }) {
  // State to manage edit mode
  const [isEditing, setIsEditing] = useState(false);
  // State to manage note content
  const [content, setContent] = useState(note.content);
  const textareaRef = useRef(null);
  
  // State for feedback and loading status
  const [feedback, setFeedback] = useState('');
  const [isFeedbackModalOpen, setIsFeedbackModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Check if feedback exists
  const hasFeedback = feedback !== '';

  // Focus the textarea when editing starts
  useEffect(() => {
    if (isEditing && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [isEditing]);

  // Save the edited content
  const handleSave = () => {
    const trimmedContent = content.trim();
    if (trimmedContent && trimmedContent !== note.content) {
      onUpdate(note.id, trimmedContent);
      setFeedback(''); // Reset feedback if content changes
    }
    setIsEditing(false);
  };

  // Handle key press events in the textarea
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSave();
    }
  };

  // Generate feedback using OpenAI API
  const handleGenerateFeedback = async () => {
    if (!getMarkdownUpTo || typeof getMarkdownUpTo !== 'function') {
      alert("Context function is not available.");
      return;
    }

    const context = getMarkdownUpTo(note.paragraph_id);
    if (!context || context.trim() === '') {
      alert("No context available for this note.");
      return;
    }

    setIsLoading(true); // Start loading

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/openai/get_feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          paragraph_id: note.paragraph_id,
          context: context,
          note_content: content,
          // 'instruction' will be created in the backend
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error with the OpenAI request.');
      }

      const data = await response.json();
      setFeedback(data.feedback); // Set the received feedback
      setIsFeedbackModalOpen(true); // Open the feedback modal
    } catch (error) {
      console.error('Error requesting feedback:', error);
      alert(`Error: ${error.message}`);
    } finally {
      setIsLoading(false); // Stop loading
    }
  };

  // Open the feedback modal
  const handleViewFeedback = () => {
    setIsFeedbackModalOpen(true);
  };

  return (
    <div className="note">
      {/* Delete button */}
      <button
        className="delete-button"
        onClick={onDelete}
        title="Delete Note"
        aria-label="Delete Note"
        style={{ color: 'black', background: 'none', border: 'none', padding: '5px', fontSize: '0.8rem', cursor: 'pointer' }}
      >
        ✕
      </button>

      {/* Editable textarea or static content */}
      {isEditing ? (
        <textarea
          ref={textareaRef}
          className="note-input"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onBlur={handleSave}
          onKeyDown={handleKeyDown}
          rows="4"
        />
      ) : (
        <div
          className="note-content"
          onClick={() => setIsEditing(true)}
          title="Click to edit"
        >
          {/* Render markdown content */}
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeSanitize]}
            className="markdown-content"
            components={{
              p: ({node, ...props}) => <p style={{ margin: '0.5em 0' }} {...props} />,
              a: ({node, ...props}) => <a {...props} style={{ color: '#3498db' }} />,
              h1: ({node, ...props}) => <h1 style={{ fontSize: '1.5em', margin: '0.5em 0' }} {...props} />,
              h2: ({node, ...props}) => <h2 style={{ fontSize: '1.3em', margin: '0.5em 0' }} {...props} />,
              ul: ({node, ...props}) => <ul style={{ margin: '0.5em 0', paddingLeft: '1.5em' }} {...props} />,
              ol: ({node, ...props}) => <ol style={{ margin: '0.5em 0', paddingLeft: '1.5em' }} {...props} />,
              li: ({node, ...props}) => <li style={{ margin: '0.3em 0' }} {...props} />,
            }}
          >
            {note.content}
          </ReactMarkdown>
        </div>
      )}
      
      {/* Buttons for feedback and regenerating feedback */}
      <div className="buttons-container">
        {!hasFeedback ? (
          <button
            className="feedback-button"
            onClick={handleGenerateFeedback}
            disabled={isLoading}
            title="Request Feedback for Summary"
          >
            {isLoading ? <span className="loading-spinner"></span> : <i className="fas fa-comment-dots"></i>} 
          </button>
        ) : (
          <>
            {/* Button to view existing feedback */}
            <button
              className="feedback-button"
              onClick={handleViewFeedback}
              title="View Feedback"
            >
              <i className="fas fa-eye"></i> 
            </button>
            {/* Button to regenerate feedback */}
            <button
              className="regenerate-button"
              onClick={handleGenerateFeedback}
              disabled={isLoading}
              title="Regenerate Feedback"
            >
              {isLoading ? <span className="loading-spinner"></span> : <i className="fas fa-redo"></i>} 
            </button>
          </>
        )}
      </div>

      {/* Modal to display feedback */}
      <Modal
        isOpen={isFeedbackModalOpen}
        onRequestClose={() => setIsFeedbackModalOpen(false)}
        contentLabel="Feedback from OpenAI"
        className="modal"
        overlayClassName="overlay"
        style={{
          content: {
            width: '1400px',
            maxWidth: '95%',
            margin: 'auto',
            padding: '2.5rem',
            inset: 'auto', 
          },
          overlay: {
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }
        }}
      >
        <h2>Feedback for Summary</h2>
        <div className="modal-content">
          {/* Render feedback markdown */}
          <ReactMarkdown
            className="markdown-content"
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeSanitize]}
          >
            {feedback}
          </ReactMarkdown>
        </div>
        {/* Button to close the modal */}
        <button className="close-button" onClick={() => setIsFeedbackModalOpen(false)}>X</button>
      </Modal>
    </div>
  );
}

export default Note;