import React from 'react';
import './Instructions.css';
import demoVideo from './Readly.mp4';


function Instructions() {
  return (
    <div className="instructions-container">
      <nav className="sidebar">

        <ul>
          <li><a href="#getting-started">Getting Started</a></li>
          <li>
            <a href="#using-the-reader">Using the Reader</a>
            <ul>
              <li><a href="#upload-a-file">1. Upload a File</a></li>
              <li><a href="#manage-processed-files">2. Manage Processed Files</a></li>
              <li><a href="#annotate-the-text">3. Annotate the Text</a></li>
              <li><a href="#request-feedback">4. Request Feedback</a></li>
              <li><a href="#continue-with-summarization">5. Continue with Summarization</a></li>
            </ul>
          </li>
          <li><a href="#summarization-technique">The Summarization Technique</a></li>
          <li><a href="#limitations-and-tips">Limitations and Tips</a></li>
        </ul>
      </nav>
      <div className="instructions">
        <h1>Reader Application User Guide</h1>
        <div className="video-container">
          <video
            controls
            width="100%"
            className="demo-video"
          >
            <source src={demoVideo} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <p className="video-caption">Demo: Overview of the Reader Application</p>
        </div>
        <p>Welcome to the <strong>Reader Application</strong>! This guide will walk you through using the application, explain the summarization technique, and highlight potential limitations to ensure you have the best experience.</p>

        <h2 id="getting-started">Getting Started</h2>
        <ol>
          <li><strong>Install and Set Up:</strong> Ensure all necessary API keys are installed and imported to enable the application’s features.</li>
          <li><strong>Access the Reader:</strong> Open the application and navigate to the <strong>Homepage</strong>.</li>
        </ol>

        <h2 id="using-the-reader">Using the Reader</h2>

        <h3 id="upload-a-file">1. Upload a File</h3>
        <ul>
          <li><strong>Drag & Drop:</strong> Select or drag a PDF file into the processing box on the homepage.</li>
          <li><strong>Note:</strong> Other file types may work but haven’t been fully tested. For more details on supported file types, visit
            <a href="https://docs.cloud.llamaindex.ai/llamaparse/features/supported_document_types" target="_blank" rel="noopener noreferrer"> LlamaIndex Documentation</a>.
          </li>
        </ul>

        <h3 id="manage-processed-files">2. Manage Processed Files</h3>
        <ul>
          <li>Click on a processed file to open it.</li>
          <li>Use the <strong>Edit</strong> button to:
            <ul>
              <li>Rename the file.</li>
              <li>Delete the file.</li>
              <li>Make changes to the filename.</li>
            </ul>
          </li>
        </ul>

        <h3 id="annotate-the-text">3. Annotate the Text</h3>
        <ul>
          <li>Hover over the text to see annotation options.</li>
          <li>Add notes in the margin (right side) for specific paragraphs following the summarization technique.</li>
        </ul>

        <h3 id="request-feedback">4. Request Feedback</h3>
        <ul>
          <li>After summarizing a paragraph:
            <ul>
              <li>Click the <strong>Feedback</strong> button to receive input from a Large Language Model (LLM).</li>
              <li>Modify your summary based on the feedback or request new feedback if needed.</li>
            </ul>
          </li>
        </ul>

        <h3 id="continue-with-summarization">5. Continue with Summarization</h3>
        <ul>
          <li>After completing a paragraph, proceed with the next using the structured summarization technique (explained below).</li>
        </ul>

        <h2 id="summarization-technique">The Summarization Technique</h2>
        <p>This technique uses a structured, cumulative approach:</p>
        <ol>
          <li><strong>Start with the Basics:</strong>
            <ul>
              <li>For the first and second paragraphs, write a <strong>one-sentence summary</strong> in the margin.</li>
            </ul>
          </li>
          <li><strong>Cumulative Summarization:</strong>
            <ul>
              <li>From the third paragraph onward:
                <ul>
                  <li>Write <strong>two sentences</strong>:</li>
                  <li>The first sentence summarizes <strong>all previous paragraphs</strong>.</li>
                  <li>The second sentence summarizes the <strong>current paragraph</strong>.</li>
                </ul>
              </li>
            </ul>
          </li>
          <li><strong>Repeat:</strong> Continue this pattern for the entire text to create a concise yet comprehensive summary.</li>
        </ol>

        <h2 id="limitations-and-tips">Limitations and Tips</h2>
        <ul>
          <li><strong>Paragraph Recognition:</strong>
            <ul>
              <li>Most paragraphs will be extracted correctly. However, due to the limitations of PDF parsing:</li>
              <li>Some text might not be recognized as complete paragraphs.</li>
              <li>Use your judgment to decide whether to annotate such text or skip it.</li>
            </ul>
          </li>
          <li><strong>File Types:</strong> While PDFs are the primary focus, unsupported or untested file types may yield inconsistent results.</li>
          <li><strong>Feedback Iterations:</strong> Feedback from the LLM might not always align with your expectations. Feel free to revise and refine summaries iteratively.</li>
        </ul>

        <p>This guide should help you efficiently navigate and use the application. If you encounter any issues or have questions, feel free to consult additional resources or contact support.</p>
      </div>
    </div>
  );
}

export default Instructions;