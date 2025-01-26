import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation/Navigation.jsx'; // Navigation component
import MarkdownPage from './pages/MarkdownPage/MarkdownPage.jsx'; // MarkdownPage component
import Home from './pages/Home/Home.jsx'; // Home component
import NotFound from './pages/NotFound/NotFound.jsx'; // NotFound component
import Layout from './components/Layout/Layout.jsx'; // Layout component
import Settings from './components/Settings/Settings.jsx';
import Instructions from './components/Instructions/Instructions.jsx'; // Instructions component
import './App.css'; // App-specific styles
import './styles/variables.css'; // Import the global stylesheet
import '@fortawesome/fontawesome-free/css/all.min.css';

function App() {
  return (
    <div className="App">
      <Navigation />
      <div className="main-content">
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/files/markdown/:filename" element={<MarkdownPage />} />
            <Route path="/instructions" element={<Instructions />} /> {/* New Instructions route */}
            <Route path="*" element={<NotFound />} /> {/* Catch-all route */}
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
      </div>
    </div>
  );
}
export default App;