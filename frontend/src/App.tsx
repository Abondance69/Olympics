import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import Home from './pages/Home/Home';
import Statistics from './pages/Statistics/Statistics';
import Predictions from './pages/Predictions/Predictions';
import France from './pages/France/France';
import About from './pages/About/About';
import './App.css';
import Host from 'pages/Host/Host';
import Result from 'pages/Result/Result';
import Athlete from 'pages/Athlete/Athlete';

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/statistics" element={<Statistics />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/france" element={<France />} />
            <Route path="/about" element={<About />} />
            <Route path="/games" element={<Host />} />
            <Route path="/results" element={<Result />} />
            <Route path="/athlete" element={<Athlete />} />
            <Route path="/athletes" element={<Athlete />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
