import { useState, useEffect } from 'react'
import axios from 'axios'
import './AdminPanel.css'

const AdminPanel = () => {
  const [agents, setAgents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Get API base URL from environment variables
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'
  const API_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 10000

  // Fetch agents on component mount
  useEffect(() => {
    const fetchAgents = async () => {
      try {
        setLoading(true)
        // Example API call - adjust endpoint as needed
        const response = await axios.get(`${API_BASE_URL}/api/agents`, {
          timeout: API_TIMEOUT
        })
        setAgents(response.data)
        setError(null)
      } catch (err) {
        console.error('Error fetching agents:', err)
        setError('Failed to load agents. Using demo data.')
        // Fallback to demo data
        setAgents([
          { id: 1, name: '侍 Akira', role: 'Code Review Master', status: 'active' },
          { id: 2, name: '❄️ Yuki', role: 'Test Engineer', status: 'active' },
          { id: 3, name: '🛡️ Hiro', role: 'SRE & DevOps', status: 'active' },
          { id: 4, name: '🌸 Sakura', role: 'Documentation', status: 'active' },
          { id: 5, name: '🏗️ Kenji', role: 'Architecture', status: 'active' }
        ])
      } finally {
        setLoading(false)
      }
    }

    fetchAgents()
  }, [API_BASE_URL, API_TIMEOUT])

  const handleStatusToggle = async (agentId) => {
    try {
      await axios.patch(`${API_BASE_URL}/api/agents/${agentId}/status`, {}, {
        timeout: API_TIMEOUT
      })
      // Refetch agents after update
      try {
        const response = await axios.get(`${API_BASE_URL}/api/agents`, {
          timeout: API_TIMEOUT
        })
        setAgents(response.data)
        setError(null)
      } catch (fetchErr) {
        console.error('Error refetching agents:', fetchErr)
        setError('Agent updated but failed to refresh list. Please reload the page.')
      }
    } catch (err) {
      console.error('Error updating agent status:', err)
      setError('Failed to update agent status. Please try again.')
    }
  }

  if (loading) {
    return (
      <div className="admin-panel">
        <div className="loading">Loading agents...</div>
      </div>
    )
  }

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h2>🎛️ Admin Panel</h2>
        <p>Manage Tokyo IA Agents</p>
      </div>

      {error && (
        <div className="alert alert-warning">
          {error}
        </div>
      )}

      <div className="agents-table">
        <table>
          <thead>
            <tr>
              <th>Agent</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((agent) => (
              <tr key={agent.id}>
                <td className="agent-name">{agent.name}</td>
                <td>{agent.role}</td>
                <td>
                  <span className={`status-badge status-${agent.status}`}>
                    {agent.status}
                  </span>
                </td>
                <td>
                  <button
                    className="btn-action"
                    onClick={() => handleStatusToggle(agent.id)}
                  >
                    Toggle
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default AdminPanel
