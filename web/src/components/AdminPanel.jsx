import React, { useState } from 'react'

function AdminPanel() {
  const [config, setConfig] = useState({
    mcpEnabled: true,
    debugMode: false,
  })

  const handleToggle = (key) => {
    setConfig(prev => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  return (
    <div className="admin-panel">
      <h2>Admin Panel</h2>
      <div className="config-section">
        <h3>Configuration</h3>
        <div className="config-item">
          <label>
            <input
              type="checkbox"
              checked={config.mcpEnabled}
              onChange={() => handleToggle('mcpEnabled')}
            />
            MCP Server Enabled
          </label>
        </div>
        <div className="config-item">
          <label>
            <input
              type="checkbox"
              checked={config.debugMode}
              onChange={() => handleToggle('debugMode')}
            />
            Debug Mode
          </label>
        </div>
      </div>
      <div className="actions">
        <button className="btn-primary">Save Configuration</button>
        <button className="btn-secondary">Reset to Defaults</button>
      </div>
    </div>
  )
}

export default AdminPanel
