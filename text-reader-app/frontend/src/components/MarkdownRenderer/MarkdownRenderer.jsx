import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import Note from '../Note/Note';
import './MarkdownRenderer.css';

function MarkdownRenderer({
  paragraphs,
  notes,
  onAddNote,
  onUpdateNote,
  onDeleteNote,
  noteCount,
  getMarkdownUpTo

}) {
  // Handler for adding a new note when the user presses Enter
  const handleAddNote = (e, paragraphId) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const content = e.target.value.trim();
      if (content !== '') {
        onAddNote(paragraphId, content); // Call the parent function to add the note
        e.target.value = '';             // Clear the textarea after adding the note
      }
    }
  };
  const getPlaceholder = () => {
    return noteCount <= 1
      ? "Add a one sentence summary for this paragraph"
      : "Write a two-sentence summary: one summarizing the previous paragraphs and one for the current paragraph";

  };

  // Function to check if the content is a markdown header
  const isHeader = (content) => {
    return /^#{1,6}\s/.test(content.trim()); // Matches markdown headers like # Header
  };

  return (
    <div className="markdown-renderer">
      {paragraphs.map(paragraph => (
        <div key={paragraph.id} className="paragraph-container">
          {/* Render the markdown content of the paragraph */}
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]} // Allow raw HTML in the markdown
          >
            {paragraph.content}
          </ReactMarkdown>
          {/* If the paragraph is not a header, display notes or note input */}
          {!isHeader(paragraph.content) && (
            <div className="notes-inline">
              {notes[paragraph.id] ? (
                // Display existing note with options to update or delete
                <Note
                  note={notes[paragraph.id]}
                  onUpdate={(id, content) => onUpdateNote(id, content)}
                  onDelete={() =>
                    onDeleteNote(notes[paragraph.id].id, paragraph.id)
                  }
                  getMarkdownUpTo={getMarkdownUpTo}
                />
              ) : (
                // Provide a textarea to add a new note
                <div className="add-note-container">
                  <textarea
                    id={`textarea-${paragraph.id}`}
                    className="add-note-input"
                    placeholder={getPlaceholder()}
                    onKeyDown={(e) => handleAddNote(e, paragraph.id)} // Handle Enter key press
                    aria-label="Add a note"
                  />
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default MarkdownRenderer;