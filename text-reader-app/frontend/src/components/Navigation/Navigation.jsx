import React from 'react';
import { Link } from 'react-router-dom';
import './Navigation.css';

function Navigation() {
  return (
    <nav>
      <ul>
        <li className="left">Textwise</li>
        <div className="right">
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/settings">Settings</Link>
          </li>
          <li>
            <Link to="/instructions">Instructions</Link>
          </li>
        </div>
      </ul>
    </nav>
  );
}

export default Navigation;
