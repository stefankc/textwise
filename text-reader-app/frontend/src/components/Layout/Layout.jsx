import React from 'react';
import './Layout.css';

const Layout = ({ children }) => (
  <div className="layout-container">
    <main className="layout-main">{children}</main>
    <footer className="layout-footer">
      <p>&copy; {new Date().getFullYear()} Text Reader App</p>
    </footer>
  </div>
);

export default Layout;
