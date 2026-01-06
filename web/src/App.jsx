import { Link } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🏛️ Tokyo IA</h1>
        <p>AI Agent Orchestration Platform</p>
        <div className="nav-buttons">
          <Link to="/admin" className="admin-link">
            🎛️ Admin Panel
          </Link>
        </div>
        <div className="agents-grid">
          <div className="agent-card">
            <h2>侍 Akira</h2>
            <p>Code Review Master</p>
          </div>
          <div className="agent-card">
            <h2>❄️ Yuki</h2>
            <p>Test Engineer</p>
          </div>
          <div className="agent-card">
            <h2>🛡️ Hiro</h2>
            <p>SRE & DevOps</p>
          </div>
          <div className="agent-card">
            <h2>🌸 Sakura</h2>
            <p>Documentation</p>
          </div>
          <div className="agent-card">
            <h2>🏗️ Kenji</h2>
            <p>Architecture</p>
          </div>
        </div>
      </header>
    </div>
  )
}

export default App
