import { useState } from 'react'
import './styles/App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="app">
      <header className="app-header">
        <h1>Tokyo-IA Web</h1>
        <p>Version 1.0.0 - Ready for Testing</p>
      </header>
      
      <main className="app-main">
        <div className="card">
          <h2>Welcome to Tokyo-IA</h2>
          <p>This is the web interface and admin panel.</p>
          
          <div className="counter">
            <button onClick={() => setCount((count) => count + 1)}>
              count is {count}
            </button>
            <p>Click the button to test interactivity</p>
          </div>
        </div>
      </main>
      
      <footer className="app-footer">
        <p>© 2025 Tokyo-IA - AI Features & MCP Server</p>
      </footer>
    </div>
  )
}

export default App
