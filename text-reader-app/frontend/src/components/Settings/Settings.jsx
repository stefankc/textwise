import React, { useState, useEffect } from 'react';
import './Settings.css';

function Settings() {
  // State variables to store API keys and messages
  const [openaiKey, setOpenaiKey] = useState('');
  const [llamaKey, setLlamaKey] = useState('');
  const [message, setMessage] = useState('');
  const [keysExist, setKeysExist] = useState(false);

  useEffect(() => {
    // Check if API keys are already set
    const fetchApiKeys = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/api_keys/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'x-token': process.env.REACT_APP_SECRET_TOKEN,
          },
        });

        if (response.ok) {
          const data = await response.json();
          if (data.OPENAI_API_KEY && data.LLAMA_CLOUD_API_KEY) {
            setKeysExist(true);
          }
        }
      } catch (error) {
        console.error('Error fetching API keys:', error);
      }
    };

    fetchApiKeys();
  }, []);

  // Handle form submission to save API keys
  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    if (!openaiKey || !llamaKey) {
      setMessage('Both API keys are required.');
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/api_keys/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-token': process.env.REACT_APP_SECRET_TOKEN,
        },
        body: JSON.stringify({
          OPENAI_API_KEY: openaiKey,
          LLAMA_CLOUD_API_KEY: llamaKey,
        }),
      });

      if (response.ok) {
        setMessage('API keys saved successfully.');
        setOpenaiKey('');
        setLlamaKey('');
        setKeysExist(true);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error saving API keys.');
      }
    } catch (error) {
      console.error('Error saving API keys:', error);
      setMessage(`Error: ${error.message}`);
    }
  };

  // Handle updating existing API keys
  const handleUpdate = () => {
    setKeysExist(false);
  };

  return (
    <div className="settings-container">
      <h2>Settings</h2>
      {keysExist ? (
        <div className="keys-exist-message">
          <p>API keys are already set.</p>
          {/* Option to update the keys */}
          <button onClick={handleUpdate}>Update Keys</button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="settings-form">
          <div className="form-group">
            <label htmlFor="openaiKey">OpenAI API Key:</label>
            <p>
              Get OpenAI Key here:
              <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer">
                https://platform.openai.com/api-keys
              </a>
            </p>
            <input
              type="password"
              id="openaiKey"
              value={openaiKey}
              onChange={(e) => setOpenaiKey(e.target.value)}
              placeholder="Enter your OpenAI API key"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="llamaKey">LLAMA Cloud API Key:</label>
            <p>
              Get LLAMAParse API Key here:
              <a href="https://cloud.llamaindex.ai/api-key" target="_blank" rel="noopener noreferrer">
                https://cloud.llamaindex.ai/api-key
              </a>
            </p>
            <input
              type="password"
              id="llamaKey"
              value={llamaKey}
              onChange={(e) => setLlamaKey(e.target.value)}
              placeholder="Enter your LLAMA Cloud API key"
              required
            />
          </div>
          <button type="submit" className="save-button">Save</button>
        </form>
      )}
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default Settings;