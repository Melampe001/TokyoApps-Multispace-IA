import { useState, useEffect } from 'react'

function AdminPanel() {
  const [stats, setStats] = useState({
    totalUsers: 0,
    activeChats: 0,
    aiRequests: 0,
    serverStatus: 'online'
  })

  useEffect(() => {
    // Simulate loading stats
    setStats({
      totalUsers: 127,
      activeChats: 23,
      aiRequests: 1543,
      serverStatus: 'online'
    })
  }, [])

  return (
    <div className="admin-panel">
      <h2>Admin Dashboard</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Users</h3>
          <p className="stat-value">{stats.totalUsers}</p>
        </div>
        
        <div className="stat-card">
          <h3>Active Chats</h3>
          <p className="stat-value">{stats.activeChats}</p>
        </div>
        
        <div className="stat-card">
          <h3>AI Requests</h3>
          <p className="stat-value">{stats.aiRequests}</p>
        </div>
        
        <div className="stat-card">
          <h3>Server Status</h3>
          <p className={`stat-value status-${stats.serverStatus}`}>
            {stats.serverStatus}
          </p>
        </div>
      </div>
      
      <div className="admin-actions">
        <h3>Quick Actions</h3>
        <button className="admin-btn">View Logs</button>
        <button className="admin-btn">Manage Users</button>
        <button className="admin-btn">System Settings</button>
      </div>
    </div>
  )
}

export default AdminPanel
