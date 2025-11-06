import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Header.css";

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  const closeMenu = () => setIsMenuOpen(false);

  return (
    <header className="header">
      <div className="container">
        <nav className="navbar">
          <Link to="/" className="logo" onClick={closeMenu}>
            <span className="logo-icon">🏅</span>
            <span className="logo-text">Olympics Analytics</span>
          </Link>

          {/* Menu burger (mobile) */}
          <button
            className={`menu-toggle ${isMenuOpen ? "active" : ""}`}
            onClick={toggleMenu}
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>

          {/* Liens du menu */}
          <ul className={`nav-menu ${isMenuOpen ? "active" : ""}`}>
            <li><Link to="/" onClick={closeMenu}>Accueil</Link></li>
            <li><Link to="/statistics" onClick={closeMenu}>Statistiques</Link></li>
            <li><Link to="/predictions" onClick={closeMenu}>Prédictions</Link></li>
            <li><Link to="/athletes" onClick={closeMenu}>Athlètes</Link></li>
            <li><Link to="/games" onClick={closeMenu}>Jeux & Hôtes</Link></li>
            <li><Link to="/results" onClick={closeMenu}>Résultats</Link></li>
            <li><Link to="/about" onClick={closeMenu}>À propos</Link></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
