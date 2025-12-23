import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './styles/App.css'
import Dashboard from './components/Dashboard'
import AdminPanel from './components/AdminPanel'

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Tokyo-IA</h1>
          <p>Tokyo-themed AI Assistant - Admin Panel</p>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
