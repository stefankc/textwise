import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom'; // Import BrowserRouter for routing
import './index.css'; // Global styles
import App from './App'; // Main App component

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter> {/* Wrap App with BrowserRouter for routing */}
      <App />
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

